"""
Configuración de base de datos SQLite con SQLAlchemy
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from pathlib import Path

# Configuración de la base de datos
DB_PATH = Path("pdfs_database.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Crear engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necesario para SQLite
    echo=False  # Cambiar a True para debug de SQL
)

# Crear session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# ========== MODELOS ==========

class PDFDocument(Base):
    """Modelo para almacenar metadata de PDFs"""
    __tablename__ = "pdf_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), unique=True, index=True, nullable=False)
    original_filename = Column(String(255))
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)  # En bytes
    total_pages = Column(Integer)
    
    # Metadata
    upload_date = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    access_count = Column(Integer, default=0)
    
    # Categorización
    tags = Column(JSON, default=list)  # Lista de tags
    category = Column(String(100))
    description = Column(Text)
    
    # Índice de contenido (texto extraído completo)
    full_text = Column(Text)
    text_by_pages = Column(JSON)  # Dict {page_num: text}
    
    # Estadísticas
    word_count = Column(Integer)
    unique_words = Column(Integer)
    
    # Flags
    is_indexed = Column(Boolean, default=False)
    is_searchable = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<PDFDocument(id={self.id}, filename='{self.filename}')>"


class QueryHistory(Base):
    """Modelo para almacenar historial de consultas"""
    __tablename__ = "query_history"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    
    # Contexto de la consulta
    pdf_filename = Column(String(255))  # NULL si es búsqueda múltiple
    multiple_pdfs = Column(JSON)  # Lista de PDFs si es búsqueda múltiple
    search_type = Column(String(50))  # "single", "multiple", "all"
    
    # Resultados
    keywords_found = Column(JSON)  # Lista de keywords
    total_matches = Column(Integer, default=0)
    documents_found = Column(Integer, default=0)
    execution_time = Column(Float)  # En segundos
    
    # Respuesta
    answer = Column(Text)
    results = Column(JSON)  # Resultados completos
    
    # Timestamp
    query_date = Column(DateTime, default=datetime.utcnow)
    
    # Feedback (opcional)
    user_rating = Column(Integer)  # 1-5 estrellas
    was_helpful = Column(Boolean)
    
    def __repr__(self):
        return f"<QueryHistory(id={self.id}, question='{self.question[:50]}...')>"


class SearchIndex(Base):
    """Modelo para índice invertido de búsqueda"""
    __tablename__ = "search_index"
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), index=True, nullable=False)
    pdf_id = Column(Integer, index=True)  # Foreign key a PDFDocument
    pdf_filename = Column(String(255), index=True)
    
    # Ubicaciones
    page_numbers = Column(JSON)  # Lista de páginas donde aparece
    occurrences = Column(Integer)  # Número de veces que aparece
    contexts = Column(JSON)  # Primeros 3 contextos
    
    # Timestamp
    indexed_date = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<SearchIndex(word='{self.word}', pdf='{self.pdf_filename}')>"


class UsageStatistics(Base):
    """Modelo para estadísticas de uso de la aplicación"""
    __tablename__ = "usage_statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Contadores
    total_queries = Column(Integer, default=0)
    total_uploads = Column(Integer, default=0)
    total_pdfs = Column(Integer, default=0)
    
    # Promedios
    avg_query_time = Column(Float)
    avg_matches_per_query = Column(Float)
    
    # Top items
    most_queried_pdf = Column(String(255))
    most_common_keywords = Column(JSON)  # Top 10 keywords
    
    # Tipos de búsqueda
    single_searches = Column(Integer, default=0)
    multiple_searches = Column(Integer, default=0)
    all_searches = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<UsageStatistics(date='{self.date}', queries={self.total_queries})>"


# ========== FUNCIONES DE UTILIDAD ==========

def get_db():
    """Dependency para obtener sesión de BD"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializar base de datos (crear tablas)"""
    Base.metadata.create_all(bind=engine)
    print(f"✅ Base de datos inicializada en: {DB_PATH.absolute()}")


def drop_all():
    """Eliminar todas las tablas (CUIDADO!)"""
    Base.metadata.drop_all(bind=engine)
    print("⚠️ Todas las tablas eliminadas")


def reset_db():
    """Resetear base de datos (eliminar y recrear)"""
    drop_all()
    init_db()
    print("♻️ Base de datos reseteada")


# Inicializar automáticamente al importar
if __name__ != "__main__":
    init_db()
