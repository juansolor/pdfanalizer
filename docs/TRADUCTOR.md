# 🌐 TRADUCTOR ALEMÁN ↔ INGLÉS

## 📋 Descripción

Módulo de traducción integrado para convertir texto y queries del **alemán al inglés** (y viceversa). Útil para trabajar con documentos en alemán o hacer queries en alemán sobre PDFs en inglés.

### Características
✅ **250+ palabras** en diccionario (alemán ↔ inglés)  
✅ **Traducción palabra por palabra** con preservación de puntuación  
✅ **Capitalización inteligente** (mantiene mayúsculas originales)  
✅ **Query translation** con análisis de cobertura  
✅ **Diccionario personalizable** (agregar palabras en runtime)  
✅ **Categorías**: palabras comunes, sustantivos, verbos, adjetivos, técnicos, números, tiempo, preguntas  

---

## 🚀 Uso Básico

### 1. Traducir Texto Simple

**Endpoint**: `POST /api/translate`

```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Das ist ein wichtiges Dokument",
    "source_lang": "de",
    "target_lang": "en"
  }'
```

**Response**:
```json
{
  "translated": "the is a important document",
  "original": "Das ist ein wichtiges Dokument",
  "source_lang": "de",
  "target_lang": "en",
  "translated_words": [
    {"original": "das", "translation": "the"},
    {"original": "ist", "translation": "is"},
    {"original": "ein", "translation": "a"},
    {"original": "wichtiges", "translation": "important"},
    {"original": "dokument", "translation": "document"}
  ],
  "untranslated_words": [],
  "translation_coverage": 100.0
}
```

---

### 2. Traducir una Palabra

**Endpoint**: `GET /api/translate/word`

```bash
# Alemán → Inglés
curl "http://localhost:8000/api/translate/word?word=dokument&source_lang=de&target_lang=en"

# Inglés → Alemán
curl "http://localhost:8000/api/translate/word?word=document&source_lang=en&target_lang=de"
```

**Response**:
```json
{
  "original": "dokument",
  "translation": "document",
  "source_lang": "de",
  "target_lang": "en",
  "found": true
}
```

---

### 3. Query Traducida (Alemán → Inglés → Búsqueda)

**Endpoint**: `POST /api/query-translated`

```bash
curl -X POST "http://localhost:8000/api/query-translated?filename=manual.pdf&question_german=Wie viele Seiten hat das Dokument?&translate_result=true"
```

**Flujo**:
1. Recibe pregunta en alemán: "Wie viele Seiten hat das Dokument?"
2. Traduce al inglés: "how many pages has the document?"
3. Hace búsqueda en el PDF con query en inglés
4. Opcionalmente traduce resultado de vuelta al alemán

**Response**:
```json
{
  "original_question": "Wie viele Seiten hat das Dokument?",
  "translated_question": "how many pages has the document?",
  "translation_info": {
    "translated": "how many pages has the document?",
    "translation_coverage": 100.0,
    "translated_words": [...]
  },
  "query_result": {
    "answer": "The document has 45 pages",
    "locations": [...],
    "cached": false
  },
  "answer_german": "the dokument hat 45 seiten"
}
```

---

### 4. Estadísticas del Diccionario

**Endpoint**: `GET /api/translate/stats`

```bash
curl http://localhost:8000/api/translate/stats
```

**Response**:
```json
{
  "total_german_words": 250,
  "total_english_words": 250,
  "categories": {
    "common_words": "prepositions, articles, conjunctions",
    "nouns": "documents, technical terms, time",
    "verbs": "actions, operations",
    "adjectives": "descriptive words",
    "questions": "interrogative words",
    "numbers": "basic numbers"
  }
}
```

---

### 5. Agregar Traducción Personalizada

**Endpoint**: `POST /api/translate/custom`

```bash
curl -X POST "http://localhost:8000/api/translate/custom?german=beispiel&english=example"
```

**Response**:
```json
{
  "message": "Traducción agregada: beispiel → example",
  "german": "beispiel",
  "english": "example"
}
```

**Nota**: Las traducciones personalizadas se agregan en runtime (memoria) y se pierden al reiniciar el servidor.

---

## 📚 Diccionario Incluido

### Categorías de Palabras

#### 1. Palabras Comunes (50+)
```
und → and
oder → or
der/die/das → the
ein/eine → a
ist → is
nicht → not
mit → with
für → for
...
```

#### 2. Sustantivos (70+)
```
dokument → document
datei → file
seite → page
benutzer → user
system → system
netzwerk → network
datenbank → database
...
```

#### 3. Verbos (60+)
```
machen → make
lesen → read
schreiben → write
suchen → search
analysieren → analyze
erstellen → create
speichern → save
...
```

#### 4. Adjetivos (30+)
```
neu → new
wichtig → important
schnell → fast
einfach → simple
sicher → safe
vollständig → complete
...
```

#### 5. Términos Técnicos (40+)
```
software → software
hardware → hardware
algorithmus → algorithm
schnittstelle → interface
konfiguration → configuration
installation → installation
...
```

#### 6. Preguntas
```
was → what
wer → who
wo → where
wann → when
warum → why
wie → how
...
```

#### 7. Tiempo
```
tag → day
woche → week
monat → month
heute → today
jetzt → now
...
```

---

## 🎯 Ejemplos de Uso

### Ejemplo 1: Traducir Pregunta Técnica

```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Wie funktioniert die Installation der Software?",
    "source_lang": "de",
    "target_lang": "en"
  }'
```

**Output**:
```
Original: "Wie funktioniert die Installation der Software?"
Traducido: "how funktioniert the installation the software?"
Cobertura: 60% (algunas palabras no traducidas)
```

### Ejemplo 2: Búsqueda en PDF Alemán

```bash
# Pregunta en alemán sobre PDF en alemán
curl -X POST "http://localhost:8000/api/query-translated?filename=manual_de.pdf&question_german=Was ist das Passwort?&translate_result=false"
```

### Ejemplo 3: Agregar Vocabulario Específico

```bash
# Agregar términos de dominio específico
curl -X POST "http://localhost:8000/api/translate/custom?german=passwort&english=password"
curl -X POST "http://localhost:8000/api/translate/custom?german=anmeldung&english=login"
curl -X POST "http://localhost:8000/api/translate/custom?german=berechtigungen&english=permissions"
```

---

## 🔧 Uso desde Python

### Importar módulo

```python
from translator import (
    translate_word,
    translate_text,
    translate_query,
    get_dictionary_stats,
    add_custom_translation
)
```

### Traducir palabra

```python
# Alemán → Inglés
translation = translate_word("dokument", "de", "en")
print(translation)  # "document"

# Inglés → Alemán
translation = translate_word("file", "en", "de")
print(translation)  # "datei"
```

### Traducir texto

```python
text = "Das ist ein wichtiges Dokument mit vielen Informationen."
result = translate_text(text, "de", "en")
print(result)
# "the is a important document with many information."
```

### Traducir query con análisis

```python
question = "Wie viele Seiten hat das Dokument?"
result = translate_query(question, "de", "en")

print(result["translated"])  # "how many pages has the document?"
print(result["translation_coverage"])  # 100.0
print(result["untranslated_words"])  # []
```

### Agregar vocabulario personalizado

```python
add_custom_translation("beispiel", "example")
add_custom_translation("lösung", "solution")

# Ahora disponibles en traducción
text = "Das ist ein Beispiel für eine Lösung"
result = translate_text(text, "de", "en")
# "the is a example for a solution"
```

---

## ⚙️ Configuración

### Preservar Capitalización

```python
# Con capitalización preservada (default)
translate_text("Das DOKUMENT ist wichtig", "de", "en", preserve_case=True)
# → "the DOCUMENT is important"

# Sin preservar
translate_text("Das DOKUMENT ist wichtig", "de", "en", preserve_case=False)
# → "the document is important"
```

### Extender Diccionario

Para agregar más palabras permanentemente, editar `translator.py`:

```python
GERMAN_TO_ENGLISH = {
    # ... palabras existentes ...
    
    # Agregar aquí
    "ejemplo_aleman": "english_example",
    "otra_palabra": "another_word",
}
```

---

## 📊 Limitaciones

### 1. Traducción Palabra por Palabra
- No considera gramática compleja
- No maneja declinaciones (der/die/das → all → "the")
- No conjuga verbos

**Ejemplo**:
```
Alemán: "Ich habe das Dokument gelesen"
Traducción literal: "I have the document read"
Correcto en inglés: "I have read the document"
```

### 2. Vocabulario Limitado
- ~250 palabras en diccionario base
- Palabras no encontradas quedan en original
- Requiere vocabulario específico del dominio

**Solución**: Usar `add_custom_translation()` para agregar términos

### 3. No Maneja Contexto
- Palabras con múltiples significados traducen siempre igual
- No considera contexto de la oración

**Ejemplo**: "Bank" puede ser "banco (dinero)" o "banco (asiento)"

---

## 🚀 Mejoras Futuras

### Integración con APIs Externas
Para traducción profesional, considerar:

- **Google Translate API** - Mejor calidad, requiere API key
- **DeepL API** - Excelente para alemán-inglés
- **Azure Translator** - Integración enterprise

### Ejemplo con Google Translate (opcional):

```python
from googletrans import Translator

def translate_with_google(text, source='de', target='en'):
    translator = Translator()
    result = translator.translate(text, src=source, dest=target)
    return result.text
```

### Modelo de ML Local
- **MarianMT** (Hugging Face) - Traducción offline
- **OpusMT** - Modelos pre-entrenados

```python
from transformers import MarianMTModel, MarianTokenizer

model_name = "Helsinki-NLP/opus-mt-de-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate_ml(text):
    translated = model.generate(**tokenizer(text, return_tensors="pt", padding=True))
    return tokenizer.decode(translated[0], skip_special_tokens=True)
```

---

## 🧪 Testing

### Probar módulo standalone

```bash
cd backend
python translator.py
```

**Output esperado**:
```
============================================================
TRADUCTOR ALEMÁN → INGLÉS
============================================================

1. Palabra individual:
   'dokument' → 'document'

2. Frase simple:
   Original: Das ist ein wichtiges Dokument mit vielen Informationen.
   Traducido: the is a important document with many information.

3. Pregunta:
   Original: Wie viele Seiten hat das Dokument?
   Traducido: how many pages has the document?
   Cobertura: 100.0%
   Palabras no traducidas: []

4. Estadísticas del diccionario:
   Total palabras alemanas: 250
   Total palabras inglesas: 250

5. Texto técnico:
   Original: Die Konfiguration des Systems ist wichtig für die Installation der Software.
   Traducido: the configuration the system is important for the installation the software.

============================================================
✅ Pruebas completadas
```

---

## 📞 Casos de Uso Reales

### 1. Empresa con Documentos en Alemán
**Problema**: PDFs en alemán, usuarios hablan inglés  
**Solución**: Traducir queries en inglés → buscar en alemán

```bash
curl -X POST "http://localhost:8000/api/query-translated?filename=handbuch.pdf&question_german=Wie installiere ich die Software?&translate_result=true"
```

### 2. Soporte Multilingüe
**Problema**: FAQ en múltiples idiomas  
**Solución**: Query en cualquier idioma → traducir → buscar

### 3. Análisis de Documentos Técnicos
**Problema**: Manuales técnicos en alemán  
**Solución**: Extraer términos técnicos + traducir

---

## 📚 Referencias

- **Diccionario Base**: 250+ palabras comunes alemán-inglés
- **Porter Stemming**: Para FTS (vacaciones = vacación)
- **Unicode Support**: Caracteres especiales (ä, ö, ü, ß)

---

## ✅ Checklist de Integración

- [x] Módulo `translator.py` creado
- [x] 5 endpoints agregados a `main.py`
- [x] Diccionario con 250+ palabras
- [x] Función de traducción palabra por palabra
- [x] Query translation con análisis
- [x] Diccionario personalizable
- [x] Documentación completa
- [ ] Testing con PDFs reales en alemán
- [ ] Frontend UI para traducción
- [ ] Integración opcional con Google Translate

---

**Versión**: 2.2.1  
**Fecha**: 2025-10-23  
**Módulo**: `translator.py`  
**Endpoints**: 5 nuevos  
**Palabras**: 250+ en diccionario base
