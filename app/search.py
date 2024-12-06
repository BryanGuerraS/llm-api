"""
Módulo para realizar búsquedas en ChromaDB utilizando embeddings generados por Cohere.

Este módulo contiene:
- Función para buscar los documentos más similares a una consulta utilizando el servicio de Cohere y ChromaDB.
- La consulta es transformada en un embedding y luego se comparan los documentos almacenados en ChromaDB.
"""

import chromadb
import cohere

def search_similar_documents(query: str, api_key: str, collection_name="documents", top_k=3):
    """
    Busca los textos más similares a la consulta en ChromaDB y devuelve los más relevantes.

    Esta función utiliza Cohere para generar un embedding de la consulta y ChromaDB para buscar 
    los documentos más similares dentro de una colección específica.

    Parámetros:
    - query (str): La consulta o pregunta que se desea analizar.
    - api_key (str): Clave API de Cohere para acceder a su servicio de embeddings.
    - collection_name (str): Nombre de la colección en ChromaDB donde se almacenan los documentos y embeddings.
      Por defecto es "documents".
    - top_k (int): Número de documentos más similares a devolver. Por defecto es 3.

    Retorna:
    - tuple: Una tupla que contiene:
      - documents (list): Lista de los textos de los documentos más similares.
      - distances (list): Lista de las distancias correspondientes de los documentos respecto al embedding de la consulta.
    """
    
    # Inicializar el cliente ChromaDB
    client = chromadb.Client()

    # Obtener la colección de documentos y embeddings
    collection = client.get_collection(collection_name)

    # Inicializar el cliente Cohere con la clave API proporcionada
    co = cohere.Client(api_key)

    # Generar el embedding para la consulta usando Cohere
    query_embedding = co.embed(
        model="embed-english-v2.0",  # Especifica el modelo de Cohere para embeddings en inglés
        texts=[query]               # La consulta se pasa como una lista de un solo texto
    ).embeddings[0]                # Extrae el primer embedding generado

    # Buscar los documentos más similares en ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],  # Embedding de la consulta
        n_results=top_k                      # Número de resultados más similares
    )

    # Extraer los documentos relevantes y sus distancias
    documents = results["documents"][0]  # Lista de textos de los documentos más relevantes
    distances = results["distances"][0]  # Lista de distancias asociadas a los documentos

    # Devolver los documentos y distancias
    return documents, distances
