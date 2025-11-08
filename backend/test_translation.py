#!/usr/bin/env python3
"""
Script de prueba para verificar la traducción de PDFs
"""

import sys
import os
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

from translator import translate_query

def test_basic_translation():
    print("🧪 Probando traducción básica...")
    
    # Texto de prueba del documento adjunto
    test_text = """Function and Einsatz
Function
The Function AutoVR dient zum Herstellen einer gültigen Transition for the Ablaufsteuerung, if the
Anlagenzustand im
Handbetrieb manuell verändert was and beim Umschalten in den Automatikbetrieb keine gültige
Transition gefunden
wird."""
    
    print(f"📝 Texto original:\n{test_text}")
    print("\n" + "="*50)
    
    # Probar traducción
    try:
        result = translate_query(test_text, "de", "en")
        print(f"✅ Traducción exitosa:")
        print(f"📄 Texto traducido:\n{result['translated']}")
        print(f"📊 Cobertura: {result['coverage_percentage']}%")
        print(f"🔍 Palabras no traducidas: {result['untranslated_words']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en traducción: {str(e)}")
        return False

def test_pdf_extraction():
    print("\n🧪 Probando extracción de PDF...")
    
    try:
        # Importar las funciones de main.py
        from main import extract_pdf_text_by_pages
        
        # Probar con un PDF disponible
        pdf_path = Path("pdfs/VASS_V6_AutoVR_2021_04_30 (1).pdf")
        
        if not pdf_path.exists():
            print(f"❌ PDF no encontrado: {pdf_path}")
            return False
            
        print(f"📂 Extrayendo texto de: {pdf_path}")
        text_by_pages = extract_pdf_text_by_pages(pdf_path)
        
        if text_by_pages:
            print(f"✅ Texto extraído exitosamente")
            print(f"📄 Páginas encontradas: {list(text_by_pages.keys())}")
            
            # Mostrar primera página (muestra)
            if 1 in text_by_pages:
                first_page = text_by_pages[1]
                print(f"📝 Muestra página 1 (primeros 200 chars):")
                print(f"{first_page[:200]}...")
                return True
        else:
            print("❌ No se pudo extraer texto del PDF")
            return False
            
    except Exception as e:
        print(f"❌ Error en extracción: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de traducción...")
    
    # Prueba 1: Traducción básica
    success1 = test_basic_translation()
    
    # Prueba 2: Extracción de PDF
    success2 = test_pdf_extraction()
    
    print("\n" + "="*50)
    print(f"📊 Resultados:")
    print(f"   Traducción básica: {'✅' if success1 else '❌'}")
    print(f"   Extracción PDF: {'✅' if success2 else '❌'}")
    
    if success1 and success2:
        print("🎉 ¡Todas las pruebas exitosas!")
    else:
        print("⚠️  Algunos componentes tienen problemas")