"""
Analytics Avanzados
Análisis de tendencias, correlaciones y patrones de uso
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import json
import re


# ========== TRENDING KEYWORDS ==========

def get_trending_keywords(db: Session, days: int = 7, limit: int = 20) -> List[Dict]:
    """
    Palabras clave más populares en los últimos N días
    
    Returns:
        Lista de keywords con frecuencia, crecimiento y contexto
    """
    from database import QueryHistory
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # Obtener todas las queries recientes
    queries = db.query(QueryHistory).filter(
        QueryHistory.timestamp >= cutoff_date
    ).all()
    
    # Extraer y contar keywords
    keyword_counter = Counter()
    keyword_contexts = defaultdict(list)
    
    for query in queries:
        if query.keywords_found:
            keywords = json.loads(query.keywords_found) if isinstance(query.keywords_found, str) else query.keywords_found
            for keyword in keywords:
                keyword_lower = keyword.lower()
                keyword_counter[keyword_lower] += 1
                
                # Guardar contexto (pregunta original)
                if len(keyword_contexts[keyword_lower]) < 3:  # Máximo 3 ejemplos
                    keyword_contexts[keyword_lower].append(query.question)
    
    # Calcular tendencias
    results = []
    for keyword, count in keyword_counter.most_common(limit):
        results.append({
            "keyword": keyword,
            "frequency": count,
            "example_questions": keyword_contexts[keyword][:3],
            "trend": "🔥 Hot" if count > 5 else "📈 Rising" if count > 2 else "📊 Stable"
        })
    
    return results


def get_trending_keywords_by_period(db: Session, days: int = 30) -> Dict:
    """
    Análisis de tendencias por períodos (diario, semanal)
    """
    from database import QueryHistory
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    queries = db.query(QueryHistory).filter(
        QueryHistory.timestamp >= cutoff_date
    ).order_by(QueryHistory.timestamp).all()
    
    # Agrupar por semana
    weekly_keywords = defaultdict(Counter)
    
    for query in queries:
        # Obtener semana (lunes como día 1)
        week_start = query.timestamp - timedelta(days=query.timestamp.weekday())
        week_key = week_start.strftime("%Y-%m-%d")
        
        if query.keywords_found:
            keywords = json.loads(query.keywords_found) if isinstance(query.keywords_found, str) else query.keywords_found
            for keyword in keywords:
                weekly_keywords[week_key][keyword.lower()] += 1
    
    # Formato de resultados
    timeline = []
    for week, keywords in sorted(weekly_keywords.items()):
        timeline.append({
            "week": week,
            "top_keywords": [
                {"keyword": k, "count": c} 
                for k, c in keywords.most_common(10)
            ]
        })
    
    return {
        "period_days": days,
        "timeline": timeline,
        "total_weeks": len(timeline)
    }


# ========== QUERY CORRELATIONS ==========

def find_query_correlations(db: Session, days: int = 30, min_support: int = 2) -> List[Dict]:
    """
    Encontrar consultas que frecuentemente aparecen juntas
    (mismo usuario, misma sesión, o PDF)
    """
    from database import QueryHistory
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # Obtener queries agrupadas por PDF
    queries = db.query(QueryHistory).filter(
        QueryHistory.timestamp >= cutoff_date
    ).order_by(QueryHistory.pdf_filename, QueryHistory.timestamp).all()
    
    # Agrupar por PDF y extraer keywords
    pdf_keyword_sets = defaultdict(list)
    
    for query in queries:
        if query.pdf_filename and query.keywords_found:
            keywords = json.loads(query.keywords_found) if isinstance(query.keywords_found, str) else query.keywords_found
            keywords_lower = [k.lower() for k in keywords]
            pdf_keyword_sets[query.pdf_filename].extend(keywords_lower)
    
    # Encontrar pares frecuentes
    pair_counter = Counter()
    
    for pdf, keywords in pdf_keyword_sets.items():
        unique_keywords = list(set(keywords))
        # Generar pares
        for i in range(len(unique_keywords)):
            for j in range(i + 1, len(unique_keywords)):
                pair = tuple(sorted([unique_keywords[i], unique_keywords[j]]))
                pair_counter[pair] += 1
    
    # Filtrar por soporte mínimo
    correlations = []
    for (word1, word2), count in pair_counter.most_common():
        if count >= min_support:
            correlations.append({
                "keyword_1": word1,
                "keyword_2": word2,
                "co_occurrence": count,
                "strength": "Strong" if count > 5 else "Moderate" if count > 3 else "Weak"
            })
    
    return correlations[:20]  # Top 20


def find_query_sequences(db: Session, days: int = 30, limit: int = 10) -> List[Dict]:
    """
    Encontrar secuencias de consultas comunes
    (qué preguntan después de qué)
    """
    from database import QueryHistory
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # Obtener queries ordenadas por PDF y tiempo
    queries = db.query(QueryHistory).filter(
        QueryHistory.timestamp >= cutoff_date
    ).order_by(QueryHistory.pdf_filename, QueryHistory.timestamp).all()
    
    # Agrupar por PDF
    pdf_query_sequences = defaultdict(list)
    
    for query in queries:
        if query.pdf_filename:
            pdf_query_sequences[query.pdf_filename].append(query.question)
    
    # Encontrar pares consecutivos
    sequence_counter = Counter()
    
    for pdf, questions in pdf_query_sequences.items():
        for i in range(len(questions) - 1):
            # Normalizar preguntas (primeras palabras)
            q1 = " ".join(questions[i].split()[:5]).lower()
            q2 = " ".join(questions[i + 1].split()[:5]).lower()
            sequence_counter[(q1, q2)] += 1
    
    # Formatear resultados
    sequences = []
    for (q1, q2), count in sequence_counter.most_common(limit):
        sequences.append({
            "first_query": q1,
            "then_query": q2,
            "frequency": count
        })
    
    return sequences


# ========== DOCUMENT SIMILARITY ==========

def find_similar_documents(db: Session, filename: str, limit: int = 5) -> List[Dict]:
    """
    Encontrar documentos similares basados en:
    - Keywords compartidas
    - Consultas similares
    - Categoría
    """
    from database import PDFDocument, QueryHistory
    
    # Obtener documento objetivo
    target_pdf = db.query(PDFDocument).filter(PDFDocument.filename == filename).first()
    if not target_pdf:
        return []
    
    # Obtener keywords del documento
    target_queries = db.query(QueryHistory).filter(
        QueryHistory.pdf_filename == filename
    ).all()
    
    target_keywords = set()
    for query in target_queries:
        if query.keywords_found:
            keywords = json.loads(query.keywords_found) if isinstance(query.keywords_found, str) else query.keywords_found
            target_keywords.update([k.lower() for k in keywords])
    
    # Comparar con otros documentos
    all_pdfs = db.query(PDFDocument).filter(PDFDocument.filename != filename).all()
    
    similarity_scores = []
    
    for pdf in all_pdfs:
        score = 0
        reasons = []
        
        # Keywords compartidas
        pdf_queries = db.query(QueryHistory).filter(
            QueryHistory.pdf_filename == pdf.filename
        ).all()
        
        pdf_keywords = set()
        for query in pdf_queries:
            if query.keywords_found:
                keywords = json.loads(query.keywords_found) if isinstance(query.keywords_found, str) else query.keywords_found
                pdf_keywords.update([k.lower() for k in keywords])
        
        common_keywords = target_keywords.intersection(pdf_keywords)
        if common_keywords:
            score += len(common_keywords) * 10
            reasons.append(f"{len(common_keywords)} keywords comunes")
        
        # Categoría
        if target_pdf.category and pdf.category == target_pdf.category:
            score += 20
            reasons.append(f"Misma categoría: {pdf.category}")
        
        # Tags compartidas
        if target_pdf.tags and pdf.tags:
            target_tags = set(json.loads(target_pdf.tags) if isinstance(target_pdf.tags, str) else target_pdf.tags or [])
            pdf_tags = set(json.loads(pdf.tags) if isinstance(pdf.tags, str) else pdf.tags or [])
            common_tags = target_tags.intersection(pdf_tags)
            if common_tags:
                score += len(common_tags) * 15
                reasons.append(f"{len(common_tags)} tags comunes")
        
        if score > 0:
            similarity_scores.append({
                "filename": pdf.filename,
                "similarity_score": score,
                "reasons": reasons,
                "common_keywords": list(common_keywords)[:10]
            })
    
    # Ordenar por score
    similarity_scores.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    return similarity_scores[:limit]


# ========== TEMPORAL ANALYSIS ==========

def get_usage_patterns_by_time(db: Session, days: int = 30) -> Dict:
    """
    Análisis de patrones de uso por hora del día y día de la semana
    """
    from database import QueryHistory
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    queries = db.query(QueryHistory).filter(
        QueryHistory.timestamp >= cutoff_date
    ).all()
    
    # Análisis por hora
    hourly_counts = defaultdict(int)
    # Análisis por día de semana
    weekday_counts = defaultdict(int)
    
    for query in queries:
        hour = query.timestamp.hour
        weekday = query.timestamp.strftime("%A")
        
        hourly_counts[hour] += 1
        weekday_counts[weekday] += 1
    
    # Encontrar horas pico
    peak_hours = sorted(hourly_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return {
        "period_days": days,
        "total_queries": len(queries),
        "hourly_distribution": dict(sorted(hourly_counts.items())),
        "weekday_distribution": dict(weekday_counts),
        "peak_hours": [
            {"hour": f"{h}:00", "queries": count}
            for h, count in peak_hours
        ],
        "most_active_day": max(weekday_counts.items(), key=lambda x: x[1])[0] if weekday_counts else None
    }


def get_pdf_usage_trends(db: Session, days: int = 30) -> List[Dict]:
    """
    Tendencias de uso de PDFs (cuáles son más consultados)
    """
    from database import PDFDocument, QueryHistory
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # Contar queries por PDF
    query_counts = db.query(
        QueryHistory.pdf_filename,
        func.count(QueryHistory.id).label("query_count")
    ).filter(
        QueryHistory.timestamp >= cutoff_date,
        QueryHistory.pdf_filename.isnot(None)
    ).group_by(QueryHistory.pdf_filename).all()
    
    # Obtener detalles de PDFs
    trends = []
    for filename, count in query_counts:
        pdf = db.query(PDFDocument).filter(PDFDocument.filename == filename).first()
        
        trends.append({
            "filename": filename,
            "query_count": count,
            "total_access_count": pdf.access_count if pdf else 0,
            "category": pdf.category if pdf else None,
            "trend": "🔥 Very Hot" if count > 20 else "📈 Hot" if count > 10 else "📊 Popular"
        })
    
    # Ordenar por popularidad
    trends.sort(key=lambda x: x["query_count"], reverse=True)
    
    return trends


# ========== PERFORMANCE ANALYTICS ==========

def get_query_performance_stats(db: Session, days: int = 30) -> Dict:
    """
    Estadísticas de rendimiento de queries
    """
    from database import QueryHistory
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    queries = db.query(QueryHistory).filter(
        QueryHistory.timestamp >= cutoff_date,
        QueryHistory.execution_time.isnot(None)
    ).all()
    
    if not queries:
        return {"message": "No hay datos suficientes"}
    
    execution_times = [q.execution_time for q in queries if q.execution_time]
    
    # Queries por tipo
    single_pdf_queries = [q for q in queries if not q.multiple_pdfs]
    multi_pdf_queries = [q for q in queries if q.multiple_pdfs]
    
    return {
        "total_queries": len(queries),
        "avg_execution_time": round(sum(execution_times) / len(execution_times), 3),
        "min_execution_time": round(min(execution_times), 3),
        "max_execution_time": round(max(execution_times), 3),
        "single_pdf_queries": {
            "count": len(single_pdf_queries),
            "avg_time": round(sum(q.execution_time for q in single_pdf_queries if q.execution_time) / len(single_pdf_queries), 3) if single_pdf_queries else 0
        },
        "multi_pdf_queries": {
            "count": len(multi_pdf_queries),
            "avg_time": round(sum(q.execution_time for q in multi_pdf_queries if q.execution_time) / len(multi_pdf_queries), 3) if multi_pdf_queries else 0
        },
        "slowest_queries": [
            {
                "question": q.question[:100],
                "execution_time": round(q.execution_time, 3),
                "pdf": q.pdf_filename
            }
            for q in sorted(queries, key=lambda x: x.execution_time or 0, reverse=True)[:5]
        ]
    }


# ========== USER BEHAVIOR PATTERNS ==========

def detect_user_patterns(db: Session, days: int = 30) -> Dict:
    """
    Detectar patrones de comportamiento del usuario
    """
    from database import QueryHistory, UsageStatistics
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    queries = db.query(QueryHistory).filter(
        QueryHistory.timestamp >= cutoff_date
    ).all()
    
    # Análisis de longitud de preguntas
    question_lengths = [len(q.question.split()) for q in queries]
    avg_question_length = sum(question_lengths) / len(question_lengths) if question_lengths else 0
    
    # Análisis de tipos de búsqueda
    search_types = defaultdict(int)
    for q in queries:
        if q.search_type:
            search_types[q.search_type] += 1
    
    # Patrones de repetición (misma pregunta)
    question_counter = Counter([q.question.lower() for q in queries])
    repeated_queries = [(q, c) for q, c in question_counter.items() if c > 1]
    
    return {
        "period_days": days,
        "total_queries": len(queries),
        "avg_question_length_words": round(avg_question_length, 1),
        "search_type_distribution": dict(search_types),
        "repeated_queries_count": len(repeated_queries),
        "most_repeated_questions": [
            {"question": q, "times_asked": c}
            for q, c in sorted(repeated_queries, key=lambda x: x[1], reverse=True)[:5]
        ],
        "user_style": "Detailed" if avg_question_length > 10 else "Concise" if avg_question_length < 5 else "Moderate"
    }


# ========== CONSOLIDADO ANALYTICS DASHBOARD ==========

def get_complete_analytics_dashboard(db: Session, days: int = 30) -> Dict:
    """
    Dashboard completo con todos los analytics
    """
    return {
        "period_days": days,
        "trending_keywords": get_trending_keywords(db, days, limit=15),
        "query_correlations": find_query_correlations(db, days),
        "usage_patterns": get_usage_patterns_by_time(db, days),
        "pdf_trends": get_pdf_usage_trends(db, days)[:10],
        "performance_stats": get_query_performance_stats(db, days),
        "user_patterns": detect_user_patterns(db, days),
        "generated_at": datetime.now().isoformat()
    }
