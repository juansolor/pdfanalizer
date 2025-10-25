"""
Servicios de base de datos - CRUD operations
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from pathlib import Path
import json

from database import PDFDocument, QueryHistory, SearchIndex, UsageStatistics


# ========== PDF DOCUMENTS ==========

def create_pdf_document(db: Session, filename: str, file_path: str, file_size: int, 
                        total_pages: int, full_text: str = "", text_by_pages: Optional[dict] = None) -> PDFDocument:
    """Crear nuevo registro de PDF"""
    pdf_doc = PDFDocument(
        filename=filename,
        original_filename=filename,
        file_path=str(file_path),
        file_size=file_size,
        total_pages=total_pages,
        full_text=full_text,
        text_by_pages=text_by_pages or {},
        word_count=len(full_text.split()) if full_text else 0,
        unique_words=len(set(full_text.lower().split())) if full_text else 0
    )
    db.add(pdf_doc)
    db.commit()
    db.refresh(pdf_doc)
    return pdf_doc


def get_pdf_by_filename(db: Session, filename: str) -> Optional[PDFDocument]:
    """Obtener PDF por nombre de archivo"""
    return db.query(PDFDocument).filter(PDFDocument.filename == filename).first()


def get_all_pdfs(db: Session, skip: int = 0, limit: int = 100) -> List[PDFDocument]:
    """Obtener todos los PDFs"""
    return db.query(PDFDocument).offset(skip).limit(limit).all()


def update_pdf_access(db: Session, filename: str):
    """Actualizar última fecha de acceso y contador"""
    pdf = get_pdf_by_filename(db, filename)
    if pdf:
        pdf.last_accessed = datetime.utcnow()
        pdf.access_count += 1
        db.commit()


def update_pdf_text(db: Session, filename: str, full_text: str, text_by_pages: dict):
    """Actualizar texto extraído del PDF"""
    pdf = get_pdf_by_filename(db, filename)
    if pdf:
        pdf.full_text = full_text
        pdf.text_by_pages = text_by_pages
        pdf.word_count = len(full_text.split())
        pdf.unique_words = len(set(full_text.lower().split()))
        pdf.is_indexed = True
        db.commit()


def add_pdf_tags(db: Session, filename: str, tags: List[str]):
    """Agregar tags a un PDF"""
    pdf = get_pdf_by_filename(db, filename)
    if pdf:
        current_tags = pdf.tags or []
        pdf.tags = list(set(current_tags + tags))
        db.commit()


def set_pdf_category(db: Session, filename: str, category: str):
    """Establecer categoría de un PDF"""
    pdf = get_pdf_by_filename(db, filename)
    if pdf:
        pdf.category = category
        db.commit()


def delete_pdf_document(db: Session, filename: str) -> bool:
    """Eliminar registro de PDF"""
    pdf = get_pdf_by_filename(db, filename)
    if pdf:
        db.delete(pdf)
        db.commit()
        return True
    return False


def search_pdfs(db: Session, query: str = "", category: Optional[str] = None, 
                tags: Optional[List[str]] = None) -> List[PDFDocument]:
    """Buscar PDFs por criterios"""
    q = db.query(PDFDocument)
    
    if query:
        q = q.filter(
            (PDFDocument.filename.contains(query)) |
            (PDFDocument.description.contains(query))
        )
    
    if category:
        q = q.filter(PDFDocument.category == category)
    
    # Tags: buscar PDFs que tengan al menos uno de los tags
    if tags:
        q = q.filter(PDFDocument.tags.op('?|')(tags))  # Operador JSON
    
    return q.all()


# ========== QUERY HISTORY ==========

def create_query_history(db: Session, question: str, pdf_filename: Optional[str] = None,
                        multiple_pdfs: Optional[List[str]] = None, search_type: str = "single",
                        keywords_found: Optional[List[str]] = None, total_matches: int = 0,
                        documents_found: int = 0, execution_time: float = 0,
                        answer: str = "", results: Optional[dict] = None) -> QueryHistory:
    """Crear registro de consulta"""
    query_history = QueryHistory(
        question=question,
        pdf_filename=pdf_filename,
        multiple_pdfs=multiple_pdfs or [],
        search_type=search_type,
        keywords_found=keywords_found or [],
        total_matches=total_matches,
        documents_found=documents_found,
        execution_time=execution_time,
        answer=answer,
        results=results or {}
    )
    db.add(query_history)
    db.commit()
    db.refresh(query_history)
    return query_history


def get_recent_queries(db: Session, limit: int = 20) -> List[QueryHistory]:
    """Obtener consultas recientes"""
    return db.query(QueryHistory)\
        .order_by(QueryHistory.query_date.desc())\
        .limit(limit)\
        .all()


def get_queries_by_pdf(db: Session, filename: str) -> List[QueryHistory]:
    """Obtener consultas de un PDF específico"""
    return db.query(QueryHistory)\
        .filter(QueryHistory.pdf_filename == filename)\
        .order_by(QueryHistory.query_date.desc())\
        .all()


def get_popular_queries(db: Session, limit: int = 10) -> List[Dict]:
    """Obtener consultas más comunes"""
    # Agrupar por pregunta similar y contar
    queries = db.query(QueryHistory.question, QueryHistory.total_matches)\
        .order_by(QueryHistory.query_date.desc())\
        .limit(100)\
        .all()
    
    # Contar preguntas similares (simplificado)
    question_counts = {}
    for q, matches in queries:
        question_lower = q.lower().strip()
        if question_lower in question_counts:
            question_counts[question_lower]["count"] += 1
        else:
            question_counts[question_lower] = {"question": q, "count": 1, "avg_matches": matches}
    
    # Ordenar por frecuencia
    popular = sorted(question_counts.values(), key=lambda x: x["count"], reverse=True)
    return popular[:limit]


def rate_query(db: Session, query_id: int, rating: int, was_helpful: Optional[bool] = None):
    """Calificar una consulta"""
    query = db.query(QueryHistory).filter(QueryHistory.id == query_id).first()
    if query:
        query.user_rating = rating
        if was_helpful is not None:
            query.was_helpful = was_helpful
        db.commit()


# ========== SEARCH INDEX ==========

def create_search_index(db: Session, word: str, pdf_filename: str, pdf_id: int,
                       page_numbers: List[int], occurrences: int, 
                       contexts: List[str]) -> SearchIndex:
    """Crear índice de búsqueda para una palabra"""
    index = SearchIndex(
        word=word.lower(),
        pdf_id=pdf_id,
        pdf_filename=pdf_filename,
        page_numbers=page_numbers,
        occurrences=occurrences,
        contexts=contexts[:3]  # Solo primeros 3 contextos
    )
    db.add(index)
    db.commit()
    db.refresh(index)
    return index


def search_in_index(db: Session, word: str, pdf_filename: Optional[str] = None) -> List[SearchIndex]:
    """Buscar palabra en índice"""
    q = db.query(SearchIndex).filter(SearchIndex.word == word.lower())
    
    if pdf_filename:
        q = q.filter(SearchIndex.pdf_filename == pdf_filename)
    
    return q.all()


def rebuild_index_for_pdf(db: Session, pdf: PDFDocument, word_data: Dict):
    """Reconstruir índice de búsqueda para un PDF"""
    # Eliminar índices viejos
    db.query(SearchIndex).filter(SearchIndex.pdf_id == pdf.id).delete()
    
    # Crear nuevos índices
    for word, data in word_data.items():
        create_search_index(
            db, word, pdf.filename, pdf.id,
            data["pages"], data["count"], data["contexts"]
        )
    
    db.commit()


# ========== USAGE STATISTICS ==========

def get_or_create_today_stats(db: Session) -> UsageStatistics:
    """Obtener o crear estadísticas del día actual"""
    today = datetime.utcnow().date()
    stats = db.query(UsageStatistics)\
        .filter(UsageStatistics.date >= today)\
        .first()
    
    if not stats:
        stats = UsageStatistics(date=datetime.utcnow())
        db.add(stats)
        db.commit()
        db.refresh(stats)
    
    return stats


def increment_query_count(db: Session, query_time: float, matches: int, search_type: str):
    """Incrementar contador de consultas"""
    stats = get_or_create_today_stats(db)
    stats.total_queries += 1
    
    # Actualizar promedios
    if stats.avg_query_time:
        stats.avg_query_time = (stats.avg_query_time * (stats.total_queries - 1) + query_time) / stats.total_queries
    else:
        stats.avg_query_time = query_time
    
    if stats.avg_matches_per_query:
        stats.avg_matches_per_query = (stats.avg_matches_per_query * (stats.total_queries - 1) + matches) / stats.total_queries
    else:
        stats.avg_matches_per_query = matches
    
    # Incrementar tipo de búsqueda
    if search_type == "single":
        stats.single_searches += 1
    elif search_type == "multiple":
        stats.multiple_searches += 1
    elif search_type == "all":
        stats.all_searches += 1
    
    db.commit()


def increment_upload_count(db: Session):
    """Incrementar contador de uploads"""
    stats = get_or_create_today_stats(db)
    stats.total_uploads += 1
    stats.total_pdfs = db.query(PDFDocument).count()
    db.commit()


def update_top_keywords(db: Session, keywords: List[str]):
    """Actualizar keywords más comunes"""
    stats = get_or_create_today_stats(db)
    current_keywords = stats.most_common_keywords or {}
    
    # Incrementar contadores
    for keyword in keywords:
        if keyword in current_keywords:
            current_keywords[keyword] += 1
        else:
            current_keywords[keyword] = 1
    
    # Mantener solo top 20
    sorted_keywords = sorted(current_keywords.items(), key=lambda x: x[1], reverse=True)
    stats.most_common_keywords = dict(sorted_keywords[:20])
    
    db.commit()


def get_statistics_summary(db: Session, days: int = 7) -> Dict:
    """Obtener resumen de estadísticas de últimos N días"""
    start_date = datetime.utcnow() - timedelta(days=days)
    stats = db.query(UsageStatistics)\
        .filter(UsageStatistics.date >= start_date)\
        .all()
    
    if not stats:
        return {
            "total_queries": 0,
            "total_uploads": 0,
            "total_pdfs": 0,
            "avg_query_time": 0,
            "avg_matches": 0
        }
    
    return {
        "total_queries": sum(s.total_queries for s in stats),
        "total_uploads": sum(s.total_uploads for s in stats),
        "total_pdfs": stats[-1].total_pdfs if stats else 0,
        "avg_query_time": sum(s.avg_query_time or 0 for s in stats) / len(stats),
        "avg_matches": sum(s.avg_matches_per_query or 0 for s in stats) / len(stats),
        "single_searches": sum(s.single_searches for s in stats),
        "multiple_searches": sum(s.multiple_searches for s in stats),
        "all_searches": sum(s.all_searches for s in stats),
        "days": days
    }


# ========== UTILIDADES ==========

def get_pdf_statistics(db: Session, filename: str) -> Dict:
    """Obtener estadísticas completas de un PDF"""
    pdf = get_pdf_by_filename(db, filename)
    if not pdf:
        return {}
    
    queries = get_queries_by_pdf(db, filename)
    
    return {
        "filename": pdf.filename,
        "upload_date": pdf.upload_date,
        "last_accessed": pdf.last_accessed,
        "access_count": pdf.access_count,
        "file_size": pdf.file_size,
        "total_pages": pdf.total_pages,
        "word_count": pdf.word_count,
        "unique_words": pdf.unique_words,
        "tags": pdf.tags,
        "category": pdf.category,
        "total_queries": len(queries),
        "is_indexed": pdf.is_indexed
    }


def get_dashboard_data(db: Session) -> Dict:
    """Obtener datos para dashboard"""
    total_pdfs = db.query(PDFDocument).count()
    total_queries = db.query(QueryHistory).count()
    recent_queries = get_recent_queries(db, limit=10)
    stats_7days = get_statistics_summary(db, days=7)
    popular_queries = get_popular_queries(db, limit=5)
    
    # PDFs más consultados
    most_accessed = db.query(PDFDocument)\
        .order_by(PDFDocument.access_count.desc())\
        .limit(5)\
        .all()
    
    return {
        "total_pdfs": total_pdfs,
        "total_queries": total_queries,
        "recent_queries": [
            {
                "id": q.id,
                "question": q.question,
                "date": q.query_date,
                "matches": q.total_matches,
                "type": q.search_type
            }
            for q in recent_queries
        ],
        "stats_7days": stats_7days,
        "popular_queries": popular_queries,
        "most_accessed_pdfs": [
            {
                "filename": pdf.filename,
                "access_count": pdf.access_count,
                "last_accessed": pdf.last_accessed
            }
            for pdf in most_accessed
        ]
    }
