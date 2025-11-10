#!/usr/bin/env python3
"""
Script para sincronizar la base de datos con los archivos físicos
"""
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

from database import get_db, init_db
import database_service as db_svc
from sqlalchemy.orm import Session

def sync_database_with_files():
    """Sincronizar base de datos con archivos físicos"""
    print("🔄 Sincronizando base de datos con archivos físicos...")
    
    # Obtener archivos físicos
    pdfs_dir = Path("../pdfs")  # Directorio donde están realmente los PDFs
    physical_files = set()
    
    if pdfs_dir.exists():
        for pdf_file in pdfs_dir.glob("*.pdf"):
            physical_files.add(pdf_file.name)
            print(f"📄 Archivo encontrado: {pdf_file.name}")
    
    print(f"\n📊 Total archivos físicos: {len(physical_files)}")
    
    # Obtener archivos en base de datos
    db = next(get_db())
    db_pdfs = db_svc.get_all_pdfs(db)
    db_files = set(pdf.filename for pdf in db_pdfs)
    
    print(f"📊 Total archivos en BD: {len(db_files)}")
    
    # Encontrar archivos huérfanos (en BD pero no físicos)
    orphaned = db_files - physical_files
    if orphaned:
        print(f"\n🗑️  Archivos huérfanos en BD (serán eliminados):")
        for filename in orphaned:
            print(f"   ❌ {filename}")
            # Eliminar de base de datos
            try:
                db_svc.delete_pdf_by_filename(db, filename)
                print(f"   ✅ Eliminado de BD: {filename}")
            except Exception as e:
                print(f"   ❌ Error eliminando: {e}")
    
    # Encontrar archivos nuevos (físicos pero no en BD)
    new_files = physical_files - db_files
    if new_files:
        print(f"\n➕ Archivos nuevos (serán agregados a BD):")
        for filename in new_files:
            print(f"   ➕ {filename}")
            file_path = pdfs_dir / filename
            
            try:
                # Agregar a base de datos
                file_size = file_path.stat().st_size
                db_svc.create_pdf_record(
                    db=db,
                    filename=filename,
                    original_filename=filename,
                    file_path=str(file_path),
                    file_size=file_size
                )
                print(f"   ✅ Agregado a BD: {filename}")
            except Exception as e:
                print(f"   ❌ Error agregando: {e}")
    
    db.commit()
    db.close()
    
    print(f"\n🎉 Sincronización completada!")
    print(f"📊 Archivos físicos: {len(physical_files)}")
    print(f"📊 Archivos sincronizados: {len(physical_files & db_files) + len(new_files)}")
    
    return len(physical_files)

if __name__ == "__main__":
    try:
        count = sync_database_with_files()
        print(f"\n✅ Proceso completado exitosamente")
        print(f"🔗 Ahora la BD y los archivos están sincronizados")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)