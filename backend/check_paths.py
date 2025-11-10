#!/usr/bin/env python3
"""
Verificar configuración de directorios del backend
"""
import os
from pathlib import Path

print("🔍 DIAGNÓSTICO DE DIRECTORIOS")
print("=" * 40)

# Directorio actual de trabajo
cwd = os.getcwd()
print(f"📁 Directorio actual: {cwd}")

# Configuración de paths
upload_folder = os.getenv("UPLOAD_FOLDER", "pdfs")
upload_dir = Path(upload_folder)
print(f"📁 UPLOAD_FOLDER: {upload_folder}")
print(f"📁 UPLOAD_DIR: {upload_dir}")
print(f"📁 UPLOAD_DIR absoluto: {upload_dir.absolute()}")
print(f"📁 ¿UPLOAD_DIR existe? {upload_dir.exists()}")

if upload_dir.exists():
    pdfs = list(upload_dir.glob("*.pdf"))
    print(f"📄 PDFs encontrados: {len(pdfs)}")
    for pdf in pdfs[:3]:
        print(f"   - {pdf.name}")
else:
    print("❌ Directorio de upload no existe")

# Probar path específico
test_file = upload_dir / "VASS_V6_AutoVR_2021_04_30 (1).pdf"
print(f"\n🎯 Archivo de prueba: {test_file}")
print(f"📄 ¿Existe? {test_file.exists()}")

# Probar path alternativo
alt_dir = Path("D:/PDFviewer/pdfs")
alt_test = alt_dir / "VASS_V6_AutoVR_2021_04_30 (1).pdf"
print(f"\n🎯 Path alternativo: {alt_test}")
print(f"📄 ¿Existe? {alt_test.exists()}")