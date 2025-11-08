#!/usr/bin/env python3
"""
Script para probar la traducción completa de PDF via API
"""

import requests
import json

def test_pdf_translation_api():
    print("🧪 Probando API de traducción de PDF...")
    
    # URL del endpoint
    url = "http://localhost:8000/api/translate-pdf"
    
    # Datos de prueba
    data = {
        "filename": "VASS_V6_AutoVR_2021_04_30 (1).pdf",
        "source_lang": "de",
        "target_lang": "en",
        "pages": [3],  # Solo página 3 para probar
        "save_translated": True,
        "output_format": "txt"
    }
    
    print(f"📤 Enviando request a: {url}")
    print(f"📋 Datos: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, timeout=60)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ ¡Traducción exitosa!")
            print(f"📄 Archivo: {result.get('filename')}")
            print(f"📈 Páginas traducidas: {result.get('pages_translated')}")
            print(f"📊 Estadísticas:")
            stats = result.get('statistics', {})
            print(f"   - Cobertura promedio: {stats.get('average_coverage', 0)}%")
            print(f"   - Palabras originales: {stats.get('total_words_original', 0)}")
            print(f"   - Palabras traducidas: {stats.get('total_words_translated', 0)}")
            print(f"💾 Archivo guardado: {result.get('translated_file')}")
            print(f"🔗 URL descarga: {result.get('download_url')}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"📋 Detalle: {json.dumps(error_detail, indent=2)}")
            except:
                print(f"📋 Respuesta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al backend. ¿Está corriendo en puerto 8000?")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_pdf_translation_api()
    print(f"\n{'✅' if success else '❌'} Resultado final: {'Éxito' if success else 'Falló'}")