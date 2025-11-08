"""
Módulo de Traducción con IA
Soporte para OpenAI GPT y Google Gemini
"""

import os
import openai
import google.generativeai as genai
from typing import Dict, Optional, List
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AITranslator:
    def __init__(self):
        # Configurar OpenAI
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
            
        # Configurar Gemini
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
            
        # Prioridad de uso: Gemini > OpenAI > Diccionario local
        self.translation_method = self._determine_method()
        
    def _determine_method(self) -> str:
        """Determinar qué método de traducción usar"""
        if self.gemini_api_key:
            return "gemini"
        elif self.openai_api_key:
            return "openai"
        else:
            return "local"
            
    async def translate_with_gemini(self, text: str, source_lang: str, target_lang: str) -> Dict:
        """Traducir usando Google Gemini"""
        try:
            # Limitar longitud del texto para evitar timeouts
            if len(text) > 2000:
                logger.warning(f"Texto muy largo ({len(text)} chars), truncando para Gemini")
                text = text[:2000] + "..."
            
            lang_names = {
                "de": "German",
                "en": "English", 
                "es": "Spanish"
            }
            
            source_name = lang_names.get(source_lang, source_lang)
            target_name = lang_names.get(target_lang, target_lang)
            
            # Prompt más conciso para respuesta más rápida
            prompt = f"""Translate this {source_name} technical text to {target_name}. Keep technical terms like AutoVR, FRG, S7G_Control unchanged. Maintain structure:

{text}

Translation:"""

            # Configurar timeout y parámetros para respuesta rápida
            import asyncio
            response = await asyncio.wait_for(
                asyncio.to_thread(self.gemini_model.generate_content, prompt),
                timeout=30.0  # 30 segundos máximo
            )
            
            translated_text = response.text.strip()
            
            return {
                "translated": translated_text,
                "original": text,
                "method": "gemini",
                "source_lang": source_lang,
                "target_lang": target_lang,
                "coverage_percentage": 95.0  # IA tiene alta cobertura
            }
            
        except asyncio.TimeoutError:
            logger.error("Timeout en Gemini (30s)")
            return None
        except Exception as e:
            logger.error(f"Error en Gemini: {str(e)}")
            return None
            
    async def translate_with_openai(self, text: str, source_lang: str, target_lang: str) -> Dict:
        """Traducir usando OpenAI GPT"""
        try:
            # Limitar longitud del texto
            if len(text) > 2000:
                logger.warning(f"Texto muy largo ({len(text)} chars), truncando para OpenAI")
                text = text[:2000] + "..."
            
            lang_names = {
                "de": "German",
                "en": "English",
                "es": "Spanish"
            }
            
            source_name = lang_names.get(source_lang, source_lang)
            target_name = lang_names.get(target_lang, target_lang)
            
            # Usar asyncio para timeout
            import asyncio
            
            def create_completion():
                return openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": f"Translate {source_name} to {target_name}. Keep technical terms unchanged."
                        },
                        {
                            "role": "user", 
                            "content": text
                        }
                    ],
                    temperature=0.1,
                    max_tokens=1500,
                    timeout=25  # 25 segundos
                )
            
            response = await asyncio.wait_for(
                asyncio.to_thread(create_completion),
                timeout=30.0
            )
            
            translated_text = response.choices[0].message.content.strip()
            
            return {
                "translated": translated_text,
                "original": text,
                "method": "openai",
                "source_lang": source_lang,
                "target_lang": target_lang,
                "coverage_percentage": 95.0  # IA tiene alta cobertura
            }
            
        except asyncio.TimeoutError:
            logger.error("Timeout en OpenAI (30s)")
            return None
        except Exception as e:
            logger.error(f"Error en OpenAI: {str(e)}")
            return None
    
    async def translate_text(self, text: str, source_lang: str = "de", target_lang: str = "en") -> Dict:
        """Traducir texto usando el mejor método disponible"""
        
        # Intentar con IA primero
        if self.translation_method == "gemini":
            result = await self.translate_with_gemini(text, source_lang, target_lang)
            if result:
                return result
                
        elif self.translation_method == "openai":
            result = await self.translate_with_openai(text, source_lang, target_lang)
            if result:
                return result
        
        # Fallback al diccionario local
        logger.info("Usando traducción local como fallback")
        from translator import translate_query
        return translate_query(text, source_lang, target_lang)
    
    def get_translation_info(self) -> Dict:
        """Obtener información sobre el método de traducción disponible"""
        return {
            "method": self.translation_method,
            "gemini_available": bool(self.gemini_api_key),
            "openai_available": bool(self.openai_api_key),
            "local_fallback": True
        }

# Instancia global
ai_translator = AITranslator()

async def translate_with_ai(text: str, source_lang: str = "de", target_lang: str = "en") -> Dict:
    """Función principal para traducir con IA"""
    return await ai_translator.translate_text(text, source_lang, target_lang)

def get_ai_info() -> Dict:
    """Obtener información de IA disponible"""
    return ai_translator.get_translation_info()