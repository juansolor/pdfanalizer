"""
Full-Text Search (FTS) con SQLite FTS5
Búsquedas ultrarrápidas en todo el contenido de los PDFs
"""
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Any
import re


# ========== INICIALIZACIÓN FTS5 ==========

def init_fts_tables(db: Session):
    """Inicializar tablas FTS5 para búsqueda full-text"""
    
    # Tabla FTS para contenido de PDFs
    db.execute(text("""
        CREATE VIRTUAL TABLE IF NOT EXISTS pdf_fts USING fts5(
            pdf_id UNINDEXED,
            filename,
            page_number UNINDEXED,
            content,
            tokenize='porter unicode61'
        )
    """))
    
    db.commit()
    print("✅ Tablas FTS5 inicializadas")


def index_pdf_for_fts(db: Session, pdf_id: int, filename: str, 
                     text_by_pages: Dict[int, str]):
    """Indexar un PDF completo en FTS5"""
    
    # Limpiar índice existente del PDF
    db.execute(
        text("DELETE FROM pdf_fts WHERE pdf_id = :pdf_id"),
        {"pdf_id": pdf_id}
    )
    
    # Indexar cada página
    for page_num, content in text_by_pages.items():
        if content and content.strip():
            db.execute(
                text("""
                    INSERT INTO pdf_fts(pdf_id, filename, page_number, content)
                    VALUES (:pdf_id, :filename, :page_number, :content)
                """),
                {
                    "pdf_id": pdf_id,
                    "filename": filename,
                    "page_number": page_num,
                    "content": content
                }
            )
    
    db.commit()
    print(f"✅ PDF '{filename}' indexado en FTS ({len(text_by_pages)} páginas)")


def remove_pdf_from_fts(db: Session, pdf_id: int):
    """Eliminar PDF del índice FTS"""
    db.execute(
        text("DELETE FROM pdf_fts WHERE pdf_id = :pdf_id"),
        {"pdf_id": pdf_id}
    )
    db.commit()


# ========== BÚSQUEDAS FTS ==========

def fts_search(db: Session, query: str, filenames: Optional[List[str]] = None,
              limit: int = 50) -> List[Dict]:
    """
    Búsqueda full-text ultrarrápida    Soporta:
    - Palabras simples: "vacaciones"
    - Múltiples palabras: "vacaciones salario"
    - Frases exactas: '"periodo de vacaciones"'
    - OR lógico: "vacaciones OR descanso"
    - AND implícito: "vacaciones salario" (ambas deben estar)
    - Wildcards: "vacac*" (encuentra vacaciones, vacacional, etc.)
    """
    
    # Preparar query FTS5
    fts_query = prepare_fts_query(query)
    
    # Construir SQL
    sql = """
        SELECT 
            pdf_id,
            filename,
            page_number,
            snippet(pdf_fts, 3, '<mark>', '</mark>', '...', 64) as snippet,
            rank
        FROM pdf_fts
        WHERE pdf_fts MATCH :query
    """
    
    params: Dict[str, Any] = {"query": fts_query}
    
    # Filtrar por archivos si se especifica
    if filenames:
        placeholders = ','.join([f":filename{i}" for i in range(len(filenames))])
        sql += f" AND filename IN ({placeholders})"
        for i, fname in enumerate(filenames):
            params[f"filename{i}"] = fname
    
    sql += " ORDER BY rank LIMIT :limit"
    params["limit"] = limit
    
    # Ejecutar búsqueda
    results = db.execute(text(sql), params).fetchall()
    
    # Formatear resultados
    return [
        {
            "pdf_id": row[0],
            "filename": row[1],
            "page_number": row[2],
            "snippet": row[3],
            "relevance": abs(float(row[4]))  # Rank negativo, convertir a positivo
        }
        for row in results
    ]


def fts_search_by_pdf(db: Session, query: str, filename: str, 
                     limit: int = 100) -> List[Dict]:
    """Búsqueda FTS en un PDF específico"""
    return fts_search(db, query, filenames=[filename], limit=limit)


def fts_search_phrase(db: Session, phrase: str, filenames: Optional[List[str]] = None,
                     limit: int = 50) -> List[Dict]:
    """Búsqueda de frase exacta"""
    # Envolver en comillas para búsqueda exacta
    exact_query = f'"{phrase}"'
    return fts_search(db, exact_query, filenames, limit)


def fts_search_advanced(db: Session, must_have: Optional[List[str]] = None,
                       should_have: Optional[List[str]] = None, must_not_have: Optional[List[str]] = None,
                       filenames: Optional[List[str]] = None, limit: int = 50) -> List[Dict]:
    """
    Búsqueda avanzada con lógica booleana
    
    Args:
        must_have: Palabras que DEBEN estar (AND)
        should_have: Palabras que PUEDEN estar (OR)
        must_not_have: Palabras que NO deben estar (NOT)
    """
    query_parts = []
    
    # AND: todas deben estar
    if must_have:
        and_part = " ".join(must_have)
        query_parts.append(f"({and_part})")
    
    # OR: al menos una debe estar
    if should_have:
        or_part = " OR ".join(should_have)
        query_parts.append(f"({or_part})")
    
    # NOT: ninguna debe estar
    if must_not_have:
        for word in must_not_have:
            query_parts.append(f"NOT {word}")
    
    if not query_parts:
        return []
    
    fts_query = " ".join(query_parts)
    return fts_search(db, fts_query, filenames, limit)


# ========== UTILIDADES ==========

def prepare_fts_query(query: str) -> str:
    """
    Preparar query para FTS5
    - Normalizar espacios
    - Manejar caracteres especiales
    - Optimizar para FTS5
    """
    # Eliminar espacios extras
    query = " ".join(query.split())
    
    # Si ya tiene comillas, mantener
    if '"' in query:
        return query
    
    # Si tiene OR explícito, mantener
    if " OR " in query.upper():
        return query
    
    # Agregar wildcard a palabras cortas (búsqueda flexible)
    # words = query.split()
    # if len(words) == 1 and len(words[0]) > 3:
    #     return f"{words[0]}*"
    
    return query


def get_fts_statistics(db: Session) -> Dict:
    """Estadísticas del índice FTS"""
    
    # Total de documentos indexados
    total_docs = db.execute(
        text("SELECT COUNT(DISTINCT pdf_id) FROM pdf_fts")
    ).scalar()
    
    # Total de páginas indexadas
    total_pages = db.execute(
        text("SELECT COUNT(*) FROM pdf_fts")
    ).scalar()
    
    # Total de palabras (aproximado)
    total_words = db.execute(
        text("SELECT SUM(LENGTH(content) - LENGTH(REPLACE(content, ' ', '')) + 1) FROM pdf_fts")
    ).scalar()
    
    # PDFs indexados
    pdfs = db.execute(
        text("SELECT DISTINCT filename FROM pdf_fts ORDER BY filename")
    ).fetchall()
    
    return {
        "total_pdfs_indexed": total_docs or 0,
        "total_pages_indexed": total_pages or 0,
        "total_words_approx": int(total_words) if total_words else 0,
        "indexed_pdfs": [row[0] for row in pdfs],
        "avg_pages_per_pdf": round(total_pages / total_docs, 2) if total_docs else 0
    }


def rebuild_fts_index(db: Session):
    """Reconstruir índice FTS desde cero"""
    from database import PDFDocument
    
    # Limpiar índice actual
    db.execute(text("DELETE FROM pdf_fts"))
    db.commit()
    
    # Re-indexar todos los PDFs
    pdfs = db.query(PDFDocument).filter(PDFDocument.is_indexed == True).all()
    
    indexed_count = 0
    for pdf in pdfs:
        if pdf.text_by_pages:
            index_pdf_for_fts(db, pdf.id, pdf.filename, pdf.text_by_pages)
            indexed_count += 1
    
    return {
        "message": "Índice FTS reconstruido",
        "pdfs_reindexed": indexed_count
    }


def optimize_fts_index(db: Session):
    """Optimizar índice FTS5 para mejor rendimiento"""
    db.execute(text("INSERT INTO pdf_fts(pdf_fts) VALUES('optimize')"))
    db.commit()
    return {"message": "Índice FTS optimizado"}


# ========== BÚSQUEDAS ESPECIALES ==========

def fts_find_similar_content(db: Session, page_content: str, 
                            exclude_pdf_id: Optional[int] = None, limit: int = 10) -> List[Dict]:
    """Encontrar páginas con contenido similar"""
    
    # Extraer palabras clave del contenido
    words = re.findall(r'\b\w{4,}\b', page_content.lower())
    keywords = list(set(words))[:10]  # Top 10 palabras únicas
    
    if not keywords:
        return []
    
    # Buscar con OR
    query = " OR ".join(keywords)
    
    sql = """
        SELECT 
            pdf_id,
            filename,
            page_number,
            snippet(pdf_fts, 3, '<mark>', '</mark>', '...', 100) as snippet,
            rank
        FROM pdf_fts
        WHERE pdf_fts MATCH :query
    """
    
    params = {"query": query, "limit": limit}
    
    if exclude_pdf_id:
        sql += " AND pdf_id != :exclude_pdf_id"
        params["exclude_pdf_id"] = exclude_pdf_id
    
    sql += " ORDER BY rank LIMIT :limit"
    
    results = db.execute(text(sql), params).fetchall()
    
    return [
        {
            "pdf_id": row[0],
            "filename": row[1],
            "page_number": row[2],
            "snippet": row[3],
            "similarity": abs(float(row[4]))
        }
        for row in results
    ]


def fts_get_context_around_match(db: Session, pdf_id: int, page_number: int,
                                 keyword: str, context_pages: int = 1) -> Dict:
    """Obtener contexto de páginas alrededor de una coincidencia"""
    
    # Página actual
    current = db.execute(
        text("""
            SELECT content FROM pdf_fts 
            WHERE pdf_id = :pdf_id AND page_number = :page_num
        """),
        {"pdf_id": pdf_id, "page_num": page_number}
    ).fetchone()
    
    # Páginas anteriores
    before = db.execute(
        text("""
            SELECT page_number, content FROM pdf_fts 
            WHERE pdf_id = :pdf_id 
            AND page_number >= :start AND page_number < :page_num
            ORDER BY page_number
        """),
        {
            "pdf_id": pdf_id,
            "start": max(1, page_number - context_pages),
            "page_num": page_number
        }
    ).fetchall()
    
    # Páginas posteriores
    after = db.execute(
        text("""
            SELECT page_number, content FROM pdf_fts 
            WHERE pdf_id = :pdf_id 
            AND page_number > :page_num AND page_number <= :end
            ORDER BY page_number
        """),
        {
            "pdf_id": pdf_id,
            "page_num": page_number,
            "end": page_number + context_pages
        }
    ).fetchall()
    
    return {
        "focus_page": page_number,
        "focus_content": current[0] if current else "",
        "before_pages": [{"page": row[0], "content": row[1]} for row in before],
        "after_pages": [{"page": row[0], "content": row[1]} for row in after]
    }
