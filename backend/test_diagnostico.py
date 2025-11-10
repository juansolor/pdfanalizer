#!/usr/bin/env python3
"""
Script de diagnóstico para problemas de búsqueda
"""

import requests
import json
import sys
from pathlib import Path

def test_backend_connection():
    """Probar conexión básica al backend"""
    print("🔍 1. Probando conexión al backend...")
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend responde correctamente")
            return True
        else:
            print(f"❌ Backend responde con error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ No se puede conectar al backend: {str(e)}")
        return False

def test_pdf_list():
    """Probar listado de PDFs"""
    print("\n🔍 2. Probando listado de PDFs...")
    try:
        response = requests.get("http://localhost:8000/list-pdfs", timeout=10)
        if response.status_code == 200:
            data = response.json()
            pdfs = data.get('pdfs', [])
            print(f"✅ Encontrados {len(pdfs)} PDFs:")
            for i, pdf in enumerate(pdfs[:3], 1):
                print(f"   {i}. {pdf}")
            return pdfs[0] if pdfs else None
        else:
            print(f"❌ Error obteniendo PDFs: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_simple_query(pdf_filename):
    """Probar consulta simple"""
    print(f"\n🔍 3. Probando consulta simple en: {pdf_filename}")
    
    query_data = {
        "question": "configuration",
        "filename": pdf_filename
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/query",
            json=query_data,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Consulta exitosa!")
            print(f"📝 Respuesta: {result.get('answer', '')[:100]}...")
            print(f"📍 Ubicaciones: {len(result.get('locations', []))}")
            print(f"🔍 Matches: {result.get('total_matches', 0)}")
            print(f"🏷️  Keywords: {result.get('keywords', [])}")
            return True
        else:
            print(f"❌ Error en consulta: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"📋 Detalle: {error_detail}")
            except:
                print(f"📋 Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_frontend_connectivity():
    """Probar si el frontend puede acceder al backend"""
    print("\n🔍 4. Probando conectividad desde perspectiva del frontend...")
    
    # Simular las mismas llamadas que hace el frontend
    try:
        # Verificar estado del API
        response = requests.get("http://localhost:8000/api/status", timeout=5)
        if response.status_code == 200:
            print("✅ API status endpoint funciona")
        else:
            print(f"❌ API status falla: {response.status_code}")
            
        return True
    except Exception as e:
        print(f"❌ Error conectividad frontend: {str(e)}")
        return False

def main():
    print("🔧 DIAGNÓSTICO DE BÚSQUEDAS - PDFViewer")
    print("=" * 50)
    
    # Prueba 1: Conexión
    if not test_backend_connection():
        print("\n❌ FALLO: Backend no disponible")
        return False
    
    # Prueba 2: PDFs
    first_pdf = test_pdf_list()
    if not first_pdf:
        print("\n❌ FALLO: No hay PDFs disponibles")
        return False
    
    # Prueba 3: Consulta
    if not test_simple_query(first_pdf):
        print("\n❌ FALLO: Error en consulta")
        return False
    
    # Prueba 4: Frontend
    if not test_frontend_connectivity():
        print("\n❌ FALLO: Problema de conectividad")
        return False
    
    print("\n🎉 ÉXITO: Todas las pruebas pasaron!")
    print("\n💡 Si el frontend no muestra resultados, el problema podría ser:")
    print("   1. Cache del navegador - presiona Ctrl+F5")
    print("   2. Error en JavaScript - abre DevTools (F12)")
    print("   3. Problema de CORS - revisa consola del navegador")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)