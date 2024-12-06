"""
Módulo para almacenar embeddings en ChromaDB.

Este módulo contiene:
- Función para almacenar embeddings junto con los documentos originales (chunks) en una colección de ChromaDB.
- Si la colección ya existe, se elimina y se crea nuevamente con los nuevos datos.
"""

import chromadb

def store_embeddings(chunks, embeddings, collection_name="documents"):
    """
    Almacena embeddings en ChromaDB.

    Esta función guarda una lista de embeddings junto con sus textos originales (chunks)
    en una colección de ChromaDB. Si la colección ya existe, se elimina y se vuelve a crear
    para almacenar los nuevos datos.

    Parámetros:
    - chunks (list): Lista de cadenas de texto que se relacionan con los embeddings.
    - embeddings (list): Lista de vectores numéricos que representan los embeddings de cada chunk.
    - collection_name (str): Nombre de la colección donde se almacenarán los datos.
      Por defecto, el nombre de la colección es "documents".

    Retorna:
    - collection (chroma.Collection): Objeto de la colección ChromaDB si el proceso es exitoso.
    - None: Si ocurre un error durante el almacenamiento.
    """
    
    try:
        # Crear la conexión con ChromaDB
        client = chromadb.Client() 
        
        # Verificar si la colección ya existe y eliminarla si es necesario
        existing_collections = [col.name for col in client.list_collections()]
        if collection_name in existing_collections:
            client.delete_collection(name=collection_name)
        
        # Crear la colección o recuperarla si ya existe
        collection = client.get_or_create_collection(name=collection_name)
        
        # Agregar los chunks y sus embeddings a la colección
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            collection.add(
                documents=[chunk],      # Texto asociado al embedding
                embeddings=[embedding], # Embedding numérico
                ids=[f"doc-{i}"]        # Identificador único para cada entrada
            )

        # Mensaje de éxito
        print(f"Se almacenaron {len(chunks)} documentos en la colección '{collection_name}'.")
        return collection

    except Exception as e:
        # Capturar y mostrar cualquier error que ocurra
        print(f"Error al almacenar los embeddings: {e}")
        return None
