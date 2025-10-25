"""
Script de inicialización para Cache, FTS y Analytics
Ejecutar UNA VEZ después de instalar la versión 2.2
"""
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db, get_db
import fts_search as fts
import db_services as db_svc
from pathlib import Path

def init_all_systems():
    """Inicializar todos los sistemas (DB, FTS, Cache)"""
    print("=" * 60)
    print("🚀 INICIALIZACIÓN DE SISTEMAS v2.2")
    print("=" * 60)
    print()
    
    # 1. Inicializar base de datos
    print("1️⃣ Inicializando base de datos...")
    try:
        init_db()
        print("   ✅ Base de datos inicializada")
    except Exception as e:
        print(f"   ⚠️ DB ya existe o error: {e}")
    print()
    
    # 2. Inicializar FTS
    print("2️⃣ Inicializando Full-Text Search (FTS5)...")
    try:
        db = next(get_db())
        fts.init_fts_tables(db)
        db.close()
        print("   ✅ FTS5 inicializado")
    except Exception as e:
        print(f"   ❌ Error inicializando FTS: {e}")
    print()
    
    # 3. Indexar PDFs existentes
    print("3️⃣ Indexando PDFs existentes en FTS...")
    try:
        db = next(get_db())
        
        # Obtener todos los PDFs con texto extraído
        pdfs = db_svc.get_all_pdfs(db)
        indexed_count = 0
        
        for pdf in pdfs:
            if pdf.text_by_pages and pdf.is_indexed:
                try:
                    fts.index_pdf_for_fts(db, pdf.id, pdf.filename, pdf.text_by_pages)
                    indexed_count += 1
                    print(f"   📄 {pdf.filename} ({len(pdf.text_by_pages)} páginas)")
                except Exception as e:
                    print(f"   ⚠️ Error indexando {pdf.filename}: {e}")
        
        db.close()
        print(f"   ✅ {indexed_count} PDFs indexados en FTS")
    except Exception as e:
        print(f"   ❌ Error indexando PDFs: {e}")
    print()
    
    # 4. Verificar estadísticas
    print("4️⃣ Verificando sistemas...")
    try:
        db = next(get_db())
        
        # Cache stats
        from cache_manager import get_cache_statistics
        cache_stats = get_cache_statistics(db)
        print(f"   💾 Cache: {cache_stats['total_cache_entries']} entradas, {cache_stats['total_hits']} hits")
        
        # FTS stats
        fts_stats = fts.get_fts_statistics(db)
        print(f"   ⚡ FTS: {fts_stats['total_pdfs_indexed']} PDFs, {fts_stats['total_pages_indexed']} páginas")
        
        # DB stats
        all_pdfs = db_svc.get_all_pdfs(db)
        print(f"   📚 Base de datos: {len(all_pdfs)} PDFs registrados")
        
        db.close()
        print("   ✅ Todos los sistemas operativos")
    except Exception as e:
        print(f"   ⚠️ Error verificando: {e}")
    print()
    
    # 5. Resumen
    print("=" * 60)
    print("✅ INICIALIZACIÓN COMPLETADA")
    print("=" * 60)
    print()
    print("📋 Próximos pasos:")
    print("   1. Inicia el servidor: python main.py")
    print("   2. Prueba cache: Repite una consulta y verifica 'cached: true'")
    print("   3. Prueba FTS: GET /api/fts/search?query=tu_keyword")
    print("   4. Revisa analytics: GET /api/analytics/dashboard")
    print()
    print("📚 Documentación: CACHE_FTS_ANALYTICS.md")
    print()

if __name__ == "__main__":
    init_all_systems()
