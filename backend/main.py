from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
import logging
import re
from pathlib import Path
import PyPDF2
from typing import List, Dict
from collections import Counter
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging para reducir spam
if os.getenv("FILTER_404_LOGS", "False").lower() == "true":
    logging.getLogger("uvicorn.access").setLevel(logging.ERROR)

# Configuración desde variables de entorno
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
RELOAD = os.getenv("RELOAD", "True").lower() == "true"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "50")) * 1024 * 1024  # MB a bytes
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "pdfs")
RESULTS_FOLDER = os.getenv("RESULTS_FOLDER", "results")

app = FastAPI(
    title="PDF Query API", 
    version="1.0.0",
    debug=DEBUG
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Directorios
UPLOAD_DIR = Path(UPLOAD_FOLDER)
RESULTS_DIR = Path(RESULTS_FOLDER)

# Crear directorios si no existen
UPLOAD_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# ========== Funciones de análisis de texto ==========

def extract_pdf_text(file_path: Path) -> str:
    """Extraer todo el texto de un PDF"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error extrayendo texto del PDF: {str(e)}")

def extract_pdf_text_by_pages(file_path: Path) -> Dict[int, str]:
    """Extraer texto de un PDF separado por páginas"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            pages_text = {}
            for page_num, page in enumerate(pdf_reader.pages, start=1):
                pages_text[page_num] = page.extract_text()
        return pages_text
    except Exception as e:
        raise Exception(f"Error extrayendo texto del PDF: {str(e)}")

def search_in_text(text: str, keywords: List[str]) -> List[Dict[str, str]]:
    """Buscar palabras clave en el texto y retornar contexto"""
    results = []
    lines = text.split('\n')
    
    for keyword in keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        for i, line in enumerate(lines):
            if pattern.search(line):
                # Obtener contexto (línea anterior, actual y siguiente)
                context_start = max(0, i - 1)
                context_end = min(len(lines), i + 2)
                context = ' '.join(lines[context_start:context_end])
                
                results.append({
                    "keyword": keyword,
                    "line_number": i + 1,
                    "context": context.strip()
                })
    
    return results

def search_in_pages(pages_text: Dict[int, str], keywords: List[str]) -> List[Dict]:
    """Buscar palabras clave en páginas específicas del PDF"""
    results = []
    
    for page_num, page_text in pages_text.items():
        lines = page_text.split('\n')
        
        for keyword in keywords:
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            for i, line in enumerate(lines):
                if pattern.search(line):
                    # Obtener contexto
                    context_start = max(0, i - 1)
                    context_end = min(len(lines), i + 2)
                    context = ' '.join(lines[context_start:context_end])
                    
                    results.append({
                        "keyword": keyword,
                        "page": page_num,
                        "line_in_page": i + 1,
                        "context": context.strip()[:300]  # Limitar contexto
                    })
    
    return results

def analyze_question(question: str) -> Dict:
    """Analizar la pregunta para extraer palabras clave y tipo de consulta"""
    question_lower = question.lower()
    
    # Identificar tipo de pregunta
    question_type = "general"
    if any(word in question_lower for word in ["qué", "que", "what"]):
        question_type = "definition"
    elif any(word in question_lower for word in ["cómo", "como", "how"]):
        question_type = "process"
    elif any(word in question_lower for word in ["cuándo", "cuando", "when"]):
        question_type = "temporal"
    elif any(word in question_lower for word in ["dónde", "donde", "where"]):
        question_type = "location"
    elif any(word in question_lower for word in ["por qué", "porque", "why"]):
        question_type = "reason"
    elif any(word in question_lower for word in ["cuánto", "cuanto", "how much", "how many"]):
        question_type = "quantity"
    
    # Extraer palabras clave (remover palabras comunes)
    stop_words = {
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
        'de', 'del', 'al', 'a', 'en', 'con', 'por', 'para',
        'qué', 'que', 'cómo', 'como', 'cuándo', 'cuando',
        'dónde', 'donde', 'por', 'es', 'está', 'son', 'están',
        'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for',
        'what', 'how', 'when', 'where', 'why', 'is', 'are'
    }
    
    words = re.findall(r'\w+', question_lower)
    keywords = [word for word in words if len(word) > 3 and word not in stop_words]
    
    return {
        "type": question_type,
        "keywords": keywords[:5]  # Limitar a 5 palabras clave principales
    }

def generate_answer(question: str, pdf_text: str, filename: str) -> str:
    """Generar respuesta basada en el contenido del PDF"""
    # Analizar la pregunta
    analysis = analyze_question(question)
    keywords = analysis["keywords"]
    
    if not keywords:
        return "No pude identificar palabras clave en tu pregunta. Por favor, intenta ser más específico."
    
    # Buscar información relevante
    search_results = search_in_text(pdf_text, keywords)
    
    if not search_results:
        return f"No encontré información relacionada con '{', '.join(keywords)}' en el documento {filename}."
    
    # Construir respuesta basada en los resultados
    answer_parts = [f"Basándome en el documento '{filename}', encontré lo siguiente:\n"]
    
    # Agrupar resultados por keyword
    keyword_contexts = {}
    for result in search_results[:5]:  # Limitar a 5 resultados más relevantes
        keyword = result["keyword"]
        if keyword not in keyword_contexts:
            keyword_contexts[keyword] = []
        keyword_contexts[keyword].append(result["context"])
    
    # Construir respuesta coherente
    for keyword, contexts in keyword_contexts.items():
        answer_parts.append(f"\n📌 Respecto a '{keyword}':")
        for i, context in enumerate(contexts[:2], 1):  # Máximo 2 contextos por keyword
            # Limitar longitud del contexto
            if len(context) > 200:
                context = context[:200] + "..."
            answer_parts.append(f"  {i}. {context}")
    
    # Agregar estadísticas
    total_matches = len(search_results)
    answer_parts.append(f"\n\n💡 Encontré {total_matches} referencia(s) relacionada(s) con tu pregunta.")
    
    return "\n".join(answer_parts)

def generate_answer_with_pages(question: str, file_path: Path, filename: str) -> Dict:
    """Generar respuesta con ubicaciones de página"""
    # Extraer texto por páginas
    pages_text = extract_pdf_text_by_pages(file_path)
    
    # Analizar la pregunta
    analysis = analyze_question(question)
    keywords = analysis["keywords"]
    
    if not keywords:
        return {
            "answer": "No pude identificar palabras clave en tu pregunta. Por favor, intenta ser más específico.",
            "keywords": [],
            "locations": [],
            "total_matches": 0
        }
    
    # Buscar en páginas específicas
    search_results = search_in_pages(pages_text, keywords)
    
    if not search_results:
        return {
            "answer": f"No encontré información relacionada con '{', '.join(keywords)}' en el documento {filename}.",
            "keywords": keywords,
            "locations": [],
            "total_matches": 0
        }
    
    # Construir respuesta
    answer_parts = [f"📄 Basándome en el documento '{filename}', encontré lo siguiente:\n"]
    
    # Agrupar por página
    pages_found = {}
    for result in search_results:
        page = result["page"]
        if page not in pages_found:
            pages_found[page] = []
        pages_found[page].append(result)
    
    # Construir respuesta por página
    locations = []
    for page, results in sorted(pages_found.items())[:5]:  # Máximo 5 páginas
        answer_parts.append(f"\n📍 **Página {page}:**")
        
        # Mostrar contextos únicos
        contexts_shown = set()
        for result in results[:2]:  # Máximo 2 resultados por página
            context = result["context"]
            if context not in contexts_shown:
                contexts_shown.add(context)
                if len(context) > 200:
                    context = context[:200] + "..."
                answer_parts.append(f"   • {context}")
                
        locations.append({
            "page": page,
            "keywords": [r["keyword"] for r in results],
            "preview": results[0]["context"][:150] + "..."
        })
    
    # Estadísticas
    total_pages = len(pages_found)
    total_matches = len(search_results)
    answer_parts.append(f"\n\n📊 **Resumen:**")
    answer_parts.append(f"• Encontré {total_matches} coincidencia(s) en {total_pages} página(s)")
    answer_parts.append(f"• Palabras clave buscadas: {', '.join(keywords)}")
    
    return {
        "answer": "\n".join(answer_parts),
        "keywords": keywords,
        "locations": locations,
        "total_matches": total_matches,
        "pages_found": list(pages_found.keys())
    }

def generate_summary(text: str, max_sentences: int = 5) -> str:
    """Generar un resumen del texto"""
    # Dividir en oraciones
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if not sentences:
        return "No se pudo generar un resumen del documento."
    
    # Tomar las primeras oraciones significativas
    summary_sentences = sentences[:max_sentences]
    
    # Calcular estadísticas básicas
    total_words = len(text.split())
    total_chars = len(text)
    total_lines = len(text.split('\n'))
    
    summary = "📋 RESUMEN DEL DOCUMENTO\n\n"
    summary += "\n".join(f"• {s}." for s in summary_sentences)
    summary += f"\n\n📊 ESTADÍSTICAS:\n"
    summary += f"• Total de palabras: {total_words:,}\n"
    summary += f"• Total de caracteres: {total_chars:,}\n"
    summary += f"• Total de líneas: {total_lines:,}"
    
    return summary

def get_word_frequency(text: str, top_n: int = 20) -> List[Dict]:
    """Obtener las palabras más frecuentes"""
    # Palabras a ignorar (stop words en español e inglés)
    stop_words = {
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
        'de', 'del', 'al', 'a', 'en', 'con', 'por', 'para', 'su', 'sus',
        'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas',
        'y', 'o', 'pero', 'si', 'no', 'ni', 'que', 'como', 'cuando',
        'donde', 'quien', 'cual', 'muy', 'más', 'menos', 'tan', 'tanto',
        'es', 'son', 'está', 'están', 'ser', 'estar', 'ha', 'han',
        'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and',
        'or', 'but', 'if', 'is', 'are', 'was', 'were', 'be', 'been',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'can', 'could', 'may', 'might', 'must', 'shall', 'should'
    }
    
    # Extraer palabras
    words = re.findall(r'\b[a-záéíóúñA-ZÁÉÍÓÚÑ]{4,}\b', text.lower())
    
    # Filtrar stop words
    filtered_words = [word for word in words if word not in stop_words]
    
    # Contar frecuencias
    word_counts = Counter(filtered_words)
    
    # Obtener las top N
    top_words = word_counts.most_common(top_n)
    
    return [{"word": word, "count": count} for word, count in top_words]

def translate_text(text: str, target_lang: str = "en") -> str:
    """Traducción básica de términos comunes (placeholder para API de traducción)"""
    # Esta es una implementación básica
    # En producción, usar Google Translate API, DeepL, etc.
    
    translations = {
        "es_to_en": {
            "documento": "document",
            "archivo": "file",
            "página": "page",
            "texto": "text",
            "contenido": "content",
            "información": "information",
            "datos": "data",
            "análisis": "analysis",
            "resumen": "summary",
            "estadísticas": "statistics"
        },
        "en_to_es": {
            "document": "documento",
            "file": "archivo",
            "page": "página",
            "text": "texto",
            "content": "contenido",
            "information": "información",
            "data": "datos",
            "analysis": "análisis",
            "summary": "resumen",
            "statistics": "estadísticas"
        }
    }
    
    # Nota: Esta es una implementación muy básica
    # Para traducción real, integrar con API de traducción
    return f"⚠️ Traducción completa requiere API externa. Texto original:\n\n{text[:500]}..."

# ========== Endpoints de la API ==========

@app.get("/")
async def root():
    return {
        "message": "PDF Query API está funcionando",
        "version": "1.0.0",
        "status": "online",
        "upload_folder": str(UPLOAD_DIR),
        "max_file_size_mb": MAX_FILE_SIZE // (1024*1024)
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {
        "status": "healthy",
        "timestamp": str(Path.cwd()),
        "upload_dir_exists": UPLOAD_DIR.exists(),
        "results_dir_exists": RESULTS_DIR.exists()
    }

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Subir un archivo PDF"""
    # Validar que se proporcionó un archivo
    if not file.filename:
        raise HTTPException(status_code=400, detail="No se proporcionó ningún archivo")
    
    # Validar extensión
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    # Validar tamaño del archivo
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail=f"El archivo es demasiado grande. Tamaño máximo: {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    # Guardar archivo
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        buffer.write(contents)
    
    return {"message": f"Archivo {file.filename} subido correctamente", "file_path": str(file_path)}

@app.post("/extract-text/{filename}")
async def extract_text(filename: str):
    """Extraer texto de un PDF"""
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        
        # Guardar texto extraído
        text_file = RESULTS_DIR / f"{filename}_extracted.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        return {"message": "Texto extraído correctamente", "text": text[:500] + "..."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar PDF: {str(e)}")

@app.post("/query")
async def query_pdf(query: dict):
    """Realizar consulta sobre el contenido del PDF"""
    question = query.get("question", "")
    filename = query.get("filename", "")
    
    if not question or not filename:
        raise HTTPException(status_code=400, detail="Se requiere pregunta y nombre de archivo")
    
    # Verificar que el archivo existe
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Archivo {filename} no encontrado")
    
    try:
        # Generar respuesta con ubicaciones de página
        result = generate_answer_with_pages(question, file_path, filename)
        
        # Agregar información adicional
        result["question"] = question
        result["filename"] = filename
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando consulta: {str(e)}")

@app.get("/list-pdfs")
async def list_pdfs():
    """Listar todos los PDFs subidos"""
    pdf_files = [f.name for f in UPLOAD_DIR.glob("*.pdf")]
    return {"pdfs": pdf_files}

@app.get("/view-pdf/{filename}")
async def view_pdf(filename: str, page: int = 1):
    """Servir PDF para visualización en el navegador"""
    from fastapi.responses import FileResponse
    
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Archivo {filename} no encontrado")
    
    # Devolver el archivo PDF con headers apropiados
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename={filename}",
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )

@app.post("/analyze/{filename}")
async def analyze_pdf(filename: str, analysis_type: str = "summary"):
    """Realizar análisis avanzado del PDF"""
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Archivo {filename} no encontrado")
    
    try:
        # Extraer texto del PDF
        pdf_text = extract_pdf_text(file_path)
        
        if not pdf_text.strip():
            return {
                "error": f"El archivo {filename} no contiene texto extraíble.",
                "analysis_type": analysis_type
            }
        
        result = {
            "filename": filename,
            "analysis_type": analysis_type
        }
        
        if analysis_type == "summary":
            result["summary"] = generate_summary(pdf_text)
            
        elif analysis_type == "word_frequency":
            result["word_frequency"] = get_word_frequency(pdf_text, top_n=20)
            result["total_unique_words"] = len(set(pdf_text.lower().split()))
            
        elif analysis_type == "statistics":
            words = pdf_text.split()
            lines = pdf_text.split('\n')
            result["statistics"] = {
                "total_words": len(words),
                "total_characters": len(pdf_text),
                "total_characters_no_spaces": len(pdf_text.replace(" ", "")),
                "total_lines": len(lines),
                "total_pages": "N/A",  # PyPDF2 puede obtener esto
                "average_word_length": sum(len(word) for word in words) / len(words) if words else 0
            }
            
        elif analysis_type == "translate":
            # Traducción básica (placeholder)
            result["translated"] = translate_text(pdf_text[:1000])
            result["note"] = "Traducción completa requiere integración con API de traducción"
            
        else:
            raise HTTPException(status_code=400, detail=f"Tipo de análisis no soportado: {analysis_type}")
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando PDF: {str(e)}")

@app.post("/batch-analyze/{filename}")
async def batch_analyze_pdf(filename: str):
    """Realizar todos los análisis de una vez"""
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Archivo {filename} no encontrado")
    
    try:
        pdf_text = extract_pdf_text(file_path)
        
        if not pdf_text.strip():
            return {"error": f"El archivo {filename} no contiene texto extraíble."}
        
        words = pdf_text.split()
        
        return {
            "filename": filename,
            "summary": generate_summary(pdf_text),
            "word_frequency": get_word_frequency(pdf_text, top_n=15),
            "statistics": {
                "total_words": len(words),
                "total_characters": len(pdf_text),
                "total_lines": len(pdf_text.split('\n')),
                "unique_words": len(set(word.lower() for word in words)),
                "average_word_length": round(sum(len(word) for word in words) / len(words) if words else 0, 2)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en análisis batch: {str(e)}")

# Catch-all para peticiones de hot-reload de React (evitar spam de 404)
@app.get("/{path:path}")
async def catch_react_routes(path: str):
    """Manejar rutas de React que no son API"""
    if path.endswith('.hot-update.json') or path.startswith('static/'):
        raise HTTPException(status_code=404, detail="React hot-reload file not found")
    
    # Para otras rutas, devolver info básica
    return {
        "message": "Esta es la API del backend", 
        "path_requested": path,
        "available_endpoints": ["/", "/docs", "/health", "/upload-pdf", "/list-pdfs"]
    }

if __name__ == "__main__":
    import uvicorn
    
    print(f"🚀 Iniciando servidor en http://{HOST}:{PORT}")
    print(f"📁 Directorio de PDFs: {UPLOAD_DIR.absolute()}")
    print(f"📊 Directorio de resultados: {RESULTS_DIR.absolute()}")
    print(f"🌐 CORS habilitado para: {', '.join(CORS_ORIGINS)}")
    
    if RELOAD:
        # Para reload, usar el string del módulo
        uvicorn.run(
            "main:app", 
            host=HOST, 
            port=PORT, 
            reload=True,
            log_level=os.getenv("LOG_LEVEL", "info").lower()
        )
    else:
        # Para producción, usar el objeto app directamente
        uvicorn.run(
            app, 
            host=HOST, 
            port=PORT, 
            log_level=os.getenv("LOG_LEVEL", "info").lower()
        )