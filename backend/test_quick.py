#!/usr/bin/env python3
"""
Prueba rápida del sistema optimizado
"""

import requests
import json

def test_quick_translation():
    print("🧪 Prueba rápida de traducción (solo 1 página)...")
    
    url = "http://localhost:8000/api/translate-pdf"
    data = {
        "filename": "VASS_V6_AutoVR_2021_04_30 (1).pdf",
        "source_lang": "de",
        "target_lang": "en",
        "pages": [1],  # Solo página 1 para prueba rápida
        "save_translated": True,
        "output_format": "txt",
        "use_ai": False  # Usar diccionario local para ser más rápido
    }
    
    try:
        print("📤 Enviando request...")
        response = requests.post(url, json=data, timeout=60)  # 1 minuto
        
        if response.status_code == 200:
            result = response.json()
            print("✅ ¡Traducción exitosa!")
            print(f"📊 Cobertura: {result['statistics']['average_coverage']}%")
            print(f"📄 Páginas: {result['pages_translated']}")
            print(f"💾 Archivo: {result['translated_file']}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_ai_info():
    print("\n🤖 Probando información de IA...")
    
    try:
        response = requests.get("http://localhost:8000/api/ai-info", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Info de IA obtenida:")
            print(f"   - IA disponible: {result.get('ai_available', False)}")
            print(f"   - Método: {result.get('method', 'unknown')}")
            print(f"   - Gemini: {result.get('gemini_available', False)}")
            print(f"   - OpenAI: {result.get('openai_available', False)}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Prueba básica de conexión
    try:
        response = requests.get("http://localhost:8000/", timeout=10)
        print("✅ Backend está respondiendo")
    except:
        print("❌ Backend no responde. ¿Está corriendo?")
        exit(1)
    
    # Pruebas
    success1 = test_ai_info()
    success2 = test_quick_translation()
    
    print(f"\n📊 Resumen:")
    print(f"   - Info IA: {'✅' if success1 else '❌'}")
    print(f"   - Traducción: {'✅' if success2 else '❌'}")
    
    if success1 and success2:
        print("🎉 ¡Sistema funcionando correctamente!")
    else:
        print("⚠️  Algunos componentes necesitan revisión")