"""
Módulo para generar respuestas utilizando Cohere, con soporte para varios idiomas.

Este módulo contiene:
- Función para generar respuestas concisas en uno de los tres idiomas: inglés, español o portugués.
- Traducción automática del prompt si es necesario, usando el servicio de Google Translator.
- Detección del idioma de la consulta utilizando langid.
"""
import cohere
import langid
from deep_translator import GoogleTranslator

def translate_text(text, target_language):
    return GoogleTranslator(source='auto', target=target_language).translate(text)

def generate_answer(query: str, context: list, api_key: str):
    """Genera una respuesta usando Cohere con los documentos más relevantes como contexto."""
    try:
        # Detectar el idioma de la consulta usando langid
        language, _ = langid.classify(query)
        
        # Mapear el idioma detectado a su nombre
        language_map = {
            'en': 'english',
            'es': 'Español',
            'pt': 'portuguese'
        }
        
        # Asegurarse de que el idioma esté en el mapa
        language_name = language_map.get(language, 'spanish')  # Default to inglés if unknown
        print(f"Idioma detectado: {language_name}")

        co = cohere.Client(api_key)
        
        # Concatenamos el contexto relevante
        context_text = " ".join(context)

        # Crear el prompt para Cohere
        prompt = f"Pregunta: {query}\n\nContexto: {context_text}\n\nGenera una respuesta concisa en una sola oración usando el idioma {language_name}, usa tercera persona, la oración debe tener menos de 50 palabras, solo genera la respuesta y agrega emojis relevantes que resuman la respuesta."

        if language_name != 'Español':  # Si el idioma de la consulta no es inglés, traducir
            prompt = translate_text(prompt, language_name.lower())
            #print(f"prompt traducido al {language_name}: {prompt}")

        # Generar la respuesta con Cohere
        response = co.generate(
            model="command-r-plus-04-2024",  # Modelo más actual
            prompt=prompt,
            max_tokens=50,
            temperature=0,  # Eliminamos la probabilidad para obtener siempre un mismo resultado
        )
        
        return response.generations[0].text.strip()

    except Exception as e:
        print(f"Error al generar la respuesta: {e}")
        return None