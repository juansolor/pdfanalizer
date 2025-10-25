"""
Sistema de caché inteligente para consultas frecuentes
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
import hashlib
import json
from datetime import datetime, timedelta
from database import Base, engine
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean

# ========== MODELO DE CACHÉ ==========

class QueryCache(Base):
    """Modelo para caché de consultas"""
    __tablename__ = "query_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    query_hash = Column(String(64), unique=True, index=True, nullable=False)
    
    # Consulta original
    question = Column(Text, nullable=False)
    pdf_files = Column(Text)  # JSON string de lista de archivos
    search_type = Column(String(50))
    
    # Resultado cacheado
    cached_result = Column(Text, nullable=False)  # JSON string
    
    # Metadata del caché
    hit_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    execution_time_saved = Column(Float, default=0.0)
    
    # Control
    is_valid = Column(Boolean, default=True)
    expires_at = Column(DateTime)
    
    def __repr__(self):
        return f"<QueryCache(question='{self.question[:50]}...', hits={self.hit_count})>"


# Crear tabla si no existe
Base.metadata.create_all(bind=engine)


# ========== FUNCIONES DE CACHÉ ==========

def generate_query_hash(question: str, pdf_files: Optional[list] = None, search_type: str = "single") -> str:
    """Generar hash único para una consulta"""
    # Normalizar pregunta
    question_normalized = question.lower().strip()
    
    # Ordenar PDFs para consistencia
    pdfs_sorted = sorted(pdf_files) if pdf_files else []
    
    # Crear string único
    cache_key = f"{question_normalized}|{search_type}|{','.join(pdfs_sorted)}"
    
    # Generar hash SHA-256
    return hashlib.sha256(cache_key.encode()).hexdigest()


def get_cached_result(db: Session, question: str, pdf_files: Optional[list] = None, 
                     search_type: str = "single") -> Optional[Dict]:
    """Obtener resultado cacheado si existe"""
    query_hash = generate_query_hash(question, pdf_files, search_type)
    
    cache_entry = db.query(QueryCache)\
        .filter(QueryCache.query_hash == query_hash)\
        .filter(QueryCache.is_valid == True)\
        .first()
    
    if not cache_entry:
        return None
    
    # Verificar si expiró
    if cache_entry.expires_at and cache_entry.expires_at < datetime.utcnow():
        cache_entry.is_valid = False
        db.commit()
        return None
    
    # Actualizar estadísticas de acceso
    cache_entry.hit_count += 1
    cache_entry.last_accessed = datetime.utcnow()
    db.commit()
    
    # Retornar resultado
    return {
        "result": json.loads(cache_entry.cached_result),
        "from_cache": True,
        "cache_hits": cache_entry.hit_count,
        "cached_at": cache_entry.created_at.isoformat()
    }


def cache_query_result(db: Session, question: str, pdf_files: Optional[list] = None,
                      search_type: str = "single", result: Optional[Dict] = None,
                      execution_time: float = 0.0, ttl_hours: int = 24) -> QueryCache:
    """Cachear resultado de una consulta"""
    query_hash = generate_query_hash(question, pdf_files, search_type)
    
    # Verificar si ya existe
    existing = db.query(QueryCache)\
        .filter(QueryCache.query_hash == query_hash)\
        .first()
    
    if existing:
        # Actualizar existente
        existing.cached_result = json.dumps(result)
        existing.last_accessed = datetime.utcnow()
        existing.execution_time_saved = execution_time
        existing.is_valid = True
        existing.expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)
        db.commit()
        db.refresh(existing)
        return existing
    
    # Crear nuevo
    cache_entry = QueryCache(
        query_hash=query_hash,
        question=question,
        pdf_files=json.dumps(pdf_files) if pdf_files else None,
        search_type=search_type,
        cached_result=json.dumps(result),
        execution_time_saved=execution_time,
        expires_at=datetime.utcnow() + timedelta(hours=ttl_hours)
    )
    
    db.add(cache_entry)
    db.commit()
    db.refresh(cache_entry)
    return cache_entry


def invalidate_cache_for_pdf(db: Session, filename: str):
    """Invalidar caché de consultas que involucran un PDF específico"""
    cache_entries = db.query(QueryCache)\
        .filter(QueryCache.pdf_files.contains(filename))\
        .all()
    
    for entry in cache_entries:
        entry.is_valid = False
    
    db.commit()
    return len(cache_entries)


def clear_expired_cache(db: Session) -> int:
    """Limpiar entradas de caché expiradas"""
    now = datetime.utcnow()
    
    expired = db.query(QueryCache)\
        .filter(QueryCache.expires_at < now)\
        .all()
    
    for entry in expired:
        entry.is_valid = False
    
    db.commit()
    return len(expired)


def get_cache_statistics(db: Session) -> Dict:
    """Obtener estadísticas del caché"""
    total_entries = db.query(QueryCache).count()
    active_entries = db.query(QueryCache).filter(QueryCache.is_valid == True).count()
    
    total_hits = db.query(QueryCache).with_entities(
        db.func.sum(QueryCache.hit_count)
    ).scalar() or 0
    
    total_time_saved = db.query(QueryCache).with_entities(
        db.func.sum(QueryCache.execution_time_saved * QueryCache.hit_count)
    ).scalar() or 0.0
    
    # Top consultas cacheadas
    top_cached = db.query(QueryCache)\
        .filter(QueryCache.is_valid == True)\
        .order_by(QueryCache.hit_count.desc())\
        .limit(5)\
        .all()
    
    return {
        "total_entries": total_entries,
        "active_entries": active_entries,
        "inactive_entries": total_entries - active_entries,
        "total_cache_hits": int(total_hits),
        "total_time_saved_seconds": round(total_time_saved, 2),
        "avg_hits_per_entry": round(total_hits / total_entries, 2) if total_entries > 0 else 0,
        "top_cached_queries": [
            {
                "question": entry.question[:100],
                "hits": entry.hit_count,
                "time_saved": round(entry.execution_time_saved * entry.hit_count, 2)
            }
            for entry in top_cached
        ]
    }


def smart_cache_cleanup(db: Session, max_entries: int = 1000, min_hits: int = 2) -> Dict:
    """Limpieza inteligente del caché"""
    # Eliminar expirados
    expired_count = clear_expired_cache(db)
    
    # Contar entradas actuales
    total_count = db.query(QueryCache).filter(QueryCache.is_valid == True).count()
    
    deleted_low_hits = 0
    if total_count > max_entries:
        # Eliminar entradas con pocos hits
        low_hit_entries = db.query(QueryCache)\
            .filter(QueryCache.is_valid == True)\
            .filter(QueryCache.hit_count < min_hits)\
            .order_by(QueryCache.last_accessed.asc())\
            .limit(total_count - max_entries)\
            .all()
        
        for entry in low_hit_entries:
            db.delete(entry)
        
        deleted_low_hits = len(low_hit_entries)
        db.commit()
    
    return {
        "expired_deleted": expired_count,
        "low_hits_deleted": deleted_low_hits,
        "total_cleaned": expired_count + deleted_low_hits,
        "remaining_entries": db.query(QueryCache).filter(QueryCache.is_valid == True).count()
    }


# ========== DECORADOR DE CACHÉ ==========

def cache_query(ttl_hours: int = 24):
    """Decorador para cachear automáticamente consultas"""
    def decorator(func):
        def wrapper(db: Session, question: str, pdf_files: Optional[list] = None, 
                   search_type: str = "single", *args, **kwargs):
            # Intentar obtener de caché
            cached = get_cached_result(db, question, pdf_files, search_type)
            
            if cached:
                print(f"✅ Cache HIT: {cached['cache_hits']} hits")
                return cached["result"]
            
            # Si no está en caché, ejecutar función
            print("❌ Cache MISS: Ejecutando consulta...")
            import time
            start_time = time.time()
            
            result = func(db, question, pdf_files, search_type, *args, **kwargs)
            
            execution_time = time.time() - start_time
            
            # Cachear resultado
            cache_query_result(
                db, question, pdf_files, search_type, 
                result, execution_time, ttl_hours
            )
            
            result["from_cache"] = False
            result["execution_time"] = execution_time
            
            return result
        
        return wrapper
    return decorator
