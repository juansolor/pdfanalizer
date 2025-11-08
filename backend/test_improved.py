#!/usr/bin/env python3
"""
Prueba de traducción mejorada con Word
"""

import requests
import json

def test_improved_translation():
    print("🧪 Probando traducción mejorada con formato Word...")
    
    url = "http://localhost:8000/api/translate-pdf"
    data = {
        "filename": "VASS_V6_AutoVR_2021_04_30 (1).pdf",
        "source_lang": "de",
        "target_lang": "en", 
        "pages": [2, 3],  # Páginas que vemos en los attachments
        "save_translated": True,
        "output_format": "docx"
    }
    
    try:
        response = requests.post(url, json=data, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ ¡Traducción exitosa!")
            print(f"📊 Cobertura promedio: {result['statistics']['average_coverage']}%")
            print(f"📄 Páginas: {result['pages_translated']}")
            print(f"📝 Palabras originales: {result['statistics']['total_words_original']}")
            print(f"📝 Palabras traducidas: {result['statistics']['total_words_translated']}")
            print(f"💾 Archivo: {result['translated_file']}")
            
            # Mostrar páginas con baja cobertura
            low_coverage = result['statistics'].get('pages_with_low_coverage', [])
            if low_coverage:
                print(f"⚠️  Páginas con baja cobertura:")
                for page in low_coverage:
                    print(f"   - Página {page['page']}: {page['coverage']}%")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_improved_translation()
    print(f"\n{'✅' if success else '❌'} Resultado: {'Éxito' if success else 'Falló'}")