"""
Módulo para generar embeddings utilizando el servicio de Cohere.

Este módulo contiene:
- Función para generar embeddings para una lista de fragmentos de texto utilizando el modelo de Cohere.
- Manejo de excepciones para capturar posibles errores durante el proceso de generación de embeddings.
"""

import cohere

def generate_embeddings(text_chunks, api_key):
    """
    Genera embeddings para una lista de chunks de texto utilizando el servicio de Cohere.

    Esta función toma una lista de fragmentos de texto y utiliza Cohere para generar
    representaciones numéricas (embeddings) de cada fragmento.

    Parámetros:
    - text_chunks (list): Lista de cadenas de texto (chunks) para las que se generarán los embeddings.
    - api_key (str): Clave API de Cohere necesaria para autenticar y acceder al servicio.

    Retorna:
    - list: Una lista de vectores (embeddings), donde cada vector corresponde a un chunk de texto.
    - None: Si ocurre un error durante el proceso.

    Manejo de errores:
    - Captura excepciones relacionadas con la conexión, la API o parámetros inválidos.
    """
    try:
        # Inicializar el cliente Cohere con la clave API
        co = cohere.Client(api_key)

        # Generar embeddings para los chunks de texto
        embeddings = co.embed(
            model='embed-english-v2.0',  # Especifica el modelo de Cohere a utilizar
            texts=text_chunks           # Lista de chunks para los que se generarán embeddings
        ).embeddings  # Extrae los embeddings generados del resultado

        # Retorna la lista de embeddings generados
        return embeddings

    except Exception as e:
        # Captura cualquier excepción y la imprime para facilitar la depuración
        print(f"Error al generar embeddings: {e}")
        return None
