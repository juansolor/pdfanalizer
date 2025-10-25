"""
Módulo de Traducción Alemán → Inglés
Traducción de palabras comunes y técnicas
"""
from typing import Dict, Optional
import re


# ========== DICCIONARIOS DE TRADUCCIÓN ==========

GERMAN_TO_ENGLISH = {
    # Palabras comunes
    "und": "and",
    "oder": "or",
    "der": "the",
    "die": "the",
    "das": "the",
    "ein": "a",
    "eine": "a",
    "ist": "is",
    "sind": "are",
    "war": "was",
    "waren": "were",
    "haben": "have",
    "hat": "has",
    "hatte": "had",
    "werden": "will",
    "wurde": "was",
    "wurden": "were",
    "sein": "be",
    "nicht": "not",
    "auch": "also",
    "aber": "but",
    "wenn": "if",
    "dann": "then",
    "mit": "with",
    "für": "for",
    "von": "from",
    "zu": "to",
    "bei": "at",
    "auf": "on",
    "in": "in",
    "an": "at",
    "über": "about",
    "unter": "under",
    "nach": "after",
    "vor": "before",
    "durch": "through",
    "gegen": "against",
    
    # Sustantivos comunes
    "dokument": "document",
    "datei": "file",
    "seite": "page",
    "text": "text",
    "inhalt": "content",
    "information": "information",
    "daten": "data",
    "analyse": "analysis",
    "zusammenfassung": "summary",
    "statistik": "statistics",
    "statistiken": "statistics",
    "ergebnis": "result",
    "beispiel": "example",
    "frage": "question",
    "antwort": "answer",
    "problem": "problem",
    "lösung": "solution",
    "methode": "method",
    "prozess": "process",
    "system": "system",
    "systeme": "systems",
    "projekt": "project",
    "aufgabe": "task",
    "ziel": "goal",
    "plan": "plan",
    "bericht": "report",
    "notiz": "note",
    "nachricht": "message",
    "nachrichten": "messages",
    "fehler": "error",
    "warnung": "warning",
    "erfolg": "success",
    "seiten": "pages",
    "seite": "page",
    "dokumente": "documents",
    
    # Términos técnicos
    "benutzer": "user",
    "administrator": "administrator",
    "passwort": "password",
    "konto": "account",
    "einstellung": "setting",
    "einstellungen": "settings",
    "konfiguration": "configuration",
    "konfigurationen": "configurations",
    "installation": "installation",
    "aktualisierung": "update",
    "version": "version",
    "software": "software",
    "hardware": "hardware",
    "netzwerk": "network",
    "internet": "internet",
    "website": "website",
    "email": "email",
    "datenbank": "database",
    "server": "server",
    "client": "client",
    "browser": "browser",
    "anwendung": "application",
    "programm": "program",
    "code": "code",
    "algorithmus": "algorithm",
    "funktion": "function",
    "variable": "variable",
    "parameter": "parameter",
    "schnittstelle": "interface",
    "api": "api",
    
    # Términos de documentos
    "kapitel": "chapter",
    "abschnitt": "section",
    "absatz": "paragraph",
    "zeile": "line",
    "wort": "word",
    "satz": "sentence",
    "titel": "title",
    "überschrift": "heading",
    "inhaltsverzeichnis": "table of contents",
    "index": "index",
    "glossar": "glossary",
    "anhang": "appendix",
    "referenz": "reference",
    "zitat": "quote",
    "fußnote": "footnote",
    "quellenangabe": "citation",
    "literatur": "literature",
    "bibliographie": "bibliography",
    
    # Verbos comunes
    "machen": "make",
    "tun": "do",
    "gehen": "go",
    "kommen": "come",
    "sehen": "see",
    "wissen": "know",
    "denken": "think",
    "nehmen": "take",
    "geben": "give",
    "finden": "find",
    "sagen": "say",
    "sprechen": "speak",
    "arbeiten": "work",
    "spielen": "play",
    "lernen": "learn",
    "lesen": "read",
    "schreiben": "write",
    "hören": "hear",
    "verstehen": "understand",
    "erklären": "explain",
    "beschreiben": "describe",
    "erstellen": "create",
    "entwickeln": "develop",
    "bauen": "build",
    "ändern": "change",
    "aktualisieren": "update",
    "löschen": "delete",
    "speichern": "save",
    "laden": "load",
    "öffnen": "open",
    "schließen": "close",
    "senden": "send",
    "empfangen": "receive",
    "suchen": "search",
    "filtern": "filter",
    "sortieren": "sort",
    "analysieren": "analyze",
    "berechnen": "calculate",
    "messen": "measure",
    "testen": "test",
    "prüfen": "check",
    "validieren": "validate",
    "bestätigen": "confirm",
    
    # Adjetivos comunes
    "neu": "new",
    "alt": "old",
    "groß": "large",
    "klein": "small",
    "viele": "many",
    "wenige": "few",
    "viel": "much",
    "wenig": "little",
    "alle": "all",
    "einige": "some",
    "gut": "good",
    "schlecht": "bad",
    "schnell": "fast",
    "langsam": "slow",
    "einfach": "simple",
    "kompliziert": "complicated",
    "wichtig": "important",
    "notwendig": "necessary",
    "möglich": "possible",
    "unmöglich": "impossible",
    "richtig": "correct",
    "falsch": "wrong",
    "verfügbar": "available",
    "aktiv": "active",
    "inaktiv": "inactive",
    "öffentlich": "public",
    "privat": "private",
    "sicher": "safe",
    "unsicher": "unsafe",
    "vollständig": "complete",
    "unvollständig": "incomplete",
    
    # Números
    "eins": "one",
    "zwei": "two",
    "drei": "three",
    "vier": "four",
    "fünf": "five",
    "sechs": "six",
    "sieben": "seven",
    "acht": "eight",
    "neun": "nine",
    "zehn": "ten",
    "erste": "first",
    "zweite": "second",
    "dritte": "third",
    "letzte": "last",
    
    # Tiempo
    "tag": "day",
    "woche": "week",
    "monat": "month",
    "jahr": "year",
    "stunde": "hour",
    "minute": "minute",
    "sekunde": "second",
    "heute": "today",
    "gestern": "yesterday",
    "morgen": "tomorrow",
    "jetzt": "now",
    "später": "later",
    "früher": "earlier",
    "immer": "always",
    "nie": "never",
    "manchmal": "sometimes",
    
    # Preguntas
    "was": "what",
    "wer": "who",
    "wo": "where",
    "wann": "when",
    "warum": "why",
    "wie": "how",
    "welche": "which",
    "welcher": "which",
    "welches": "which",
}

# Invertir diccionario para inglés → alemán
ENGLISH_TO_GERMAN = {v: k for k, v in GERMAN_TO_ENGLISH.items()}


# ========== FUNCIONES DE TRADUCCIÓN ==========

def translate_word(word: str, source_lang: str = "de", target_lang: str = "en") -> Optional[str]:
    """
    Traducir una palabra individual
    
    Args:
        word: Palabra a traducir
        source_lang: Idioma origen ("de" = alemán, "en" = inglés)
        target_lang: Idioma destino
        
    Returns:
        Palabra traducida o None si no se encuentra
    """
    word_lower = word.lower()
    
    if source_lang == "de" and target_lang == "en":
        return GERMAN_TO_ENGLISH.get(word_lower)
    elif source_lang == "en" and target_lang == "de":
        return ENGLISH_TO_GERMAN.get(word_lower)
    
    return None


def translate_text(text: str, source_lang: str = "de", target_lang: str = "en", 
                   preserve_case: bool = True) -> str:
    """
    Traducir texto palabra por palabra
    
    Args:
        text: Texto a traducir
        source_lang: Idioma origen ("de" = alemán, "en" = inglés)
        target_lang: Idioma destino
        preserve_case: Preservar mayúsculas/minúsculas originales
        
    Returns:
        Texto traducido (palabras no encontradas quedan en original)
    """
    # Separar en tokens (palabras + espacios + puntuación)
    tokens = re.findall(r'\w+|\s+|[^\w\s]', text)
    
    translated_tokens = []
    for token in tokens:
        if token.strip() and token.replace('_', '').isalpha():
            # Es una palabra
            translated = translate_word(token, source_lang, target_lang)
            
            if translated:
                # Preservar capitalización si está habilitado
                if preserve_case:
                    if token.isupper():
                        translated = translated.upper()
                    elif token[0].isupper():
                        translated = translated.capitalize()
                
                translated_tokens.append(translated)
            else:
                # Palabra no encontrada, mantener original
                translated_tokens.append(token)
        else:
            # Espacio, puntuación, o número - mantener tal cual
            translated_tokens.append(token)
    
    return ''.join(translated_tokens)


def translate_query(question: str, source_lang: str = "de", target_lang: str = "en") -> Dict:
    """
    Traducir una pregunta y proporcionar contexto
    
    Returns:
        Dict con:
        - translated: Texto traducido
        - original: Texto original
        - source_lang: Idioma origen
        - target_lang: Idioma destino
        - translated_words: Lista de palabras traducidas
        - untranslated_words: Palabras que no se pudieron traducir
    """
    words = re.findall(r'\b\w+\b', question.lower())
    
    translated_words = []
    untranslated_words = []
    
    for word in words:
        translation = translate_word(word, source_lang, target_lang)
        if translation:
            translated_words.append({"original": word, "translation": translation})
        else:
            untranslated_words.append(word)
    
    translated_text = translate_text(question, source_lang, target_lang)
    
    return {
        "translated": translated_text,
        "original": question,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "translated_words": translated_words,
        "untranslated_words": untranslated_words,
        "translation_coverage": len(translated_words) / len(words) * 100 if words else 0
    }


def get_dictionary_stats() -> Dict:
    """Obtener estadísticas del diccionario"""
    return {
        "total_german_words": len(GERMAN_TO_ENGLISH),
        "total_english_words": len(ENGLISH_TO_GERMAN),
        "categories": {
            "common_words": "prepositions, articles, conjunctions",
            "nouns": "documents, technical terms, time",
            "verbs": "actions, operations",
            "adjectives": "descriptive words",
            "questions": "interrogative words",
            "numbers": "basic numbers"
        }
    }


def add_custom_translation(german: str, english: str):
    """Agregar traducción personalizada al diccionario"""
    GERMAN_TO_ENGLISH[german.lower()] = english.lower()
    ENGLISH_TO_GERMAN[english.lower()] = german.lower()
    print(f"✅ Agregado: {german} → {english}")


# ========== EJEMPLOS DE USO ==========

if __name__ == "__main__":
    # Pruebas
    print("=" * 60)
    print("TRADUCTOR ALEMÁN → INGLÉS")
    print("=" * 60)
    print()
    
    # Prueba 1: Palabra individual
    print("1. Palabra individual:")
    word = "dokument"
    translated = translate_word(word, "de", "en")
    print(f"   '{word}' → '{translated}'")
    print()
    
    # Prueba 2: Frase simple
    print("2. Frase simple:")
    text = "Das ist ein wichtiges Dokument mit vielen Informationen."
    result = translate_text(text, "de", "en")
    print(f"   Original: {text}")
    print(f"   Traducido: {result}")
    print()
    
    # Prueba 3: Pregunta
    print("3. Pregunta:")
    question = "Wie viele Seiten hat das Dokument?"
    result = translate_query(question, "de", "en")
    print(f"   Original: {result['original']}")
    print(f"   Traducido: {result['translated']}")
    print(f"   Cobertura: {result['translation_coverage']:.1f}%")
    print(f"   Palabras no traducidas: {result['untranslated_words']}")
    print()
    
    # Prueba 4: Estadísticas
    print("4. Estadísticas del diccionario:")
    stats = get_dictionary_stats()
    print(f"   Total palabras alemanas: {stats['total_german_words']}")
    print(f"   Total palabras inglesas: {stats['total_english_words']}")
    print()
    
    # Prueba 5: Texto técnico
    print("5. Texto técnico:")
    tech_text = "Die Konfiguration des Systems ist wichtig für die Installation der Software."
    result = translate_text(tech_text, "de", "en")
    print(f"   Original: {tech_text}")
    print(f"   Traducido: {result}")
    print()
    
    print("=" * 60)
    print("✅ Pruebas completadas")
