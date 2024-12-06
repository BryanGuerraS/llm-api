"""
Módulo principal para inicializar y ejecutar la API de FastAPI.

Este módulo contiene:
- Configuración inicial y manejo del ciclo de vida de la aplicación.
- Endpoint principal para responder preguntas utilizando un LLM.
- Inicialización de embeddings desde un documento .docx, almacenamiento en ChromaDB, y generación de respuestas.
"""
from fastapi import FastAPI
from pydantic import BaseModel
from app.document_processing import read_docx, split_into_chunks
from app.embeddings import generate_embeddings
from app.storage import store_embeddings
from app.search import search_similar_documents
from app.generate_answer import generate_answer
import chromadb

# Inicializar la aplicación FastAPI
app = FastAPI()

# Clave API de Cohere
API_KEY = "fbdkymnccgS3MtUK38jsJ0mVcU1mrqNOKpUBFMsd"

# Nombre de la colección en ChromaDB
COLLECTION_NAME = "documents"

# Inicializar cliente ChromaDB
client = chromadb.Client()

def inicializar_embeddings():
    """
    Procesa el documento y almacena los embeddings en ChromaDB si no existen.
    """
    try:
        # Verificar si la colección ya tiene datos
        collection = client.get_or_create_collection(name=COLLECTION_NAME)
        if collection.count() > 0:
            print("Los embeddings ya están cargados en ChromaDB. No se requiere procesamiento adicional.")
            return

        # Leer y procesar el documento
        print("Procesando el documento por primera vez...")
        # Leer el contenido del documento
        content = read_docx('documento.docx')
        
        # Dividir en chunks
        chunks = split_into_chunks(content, max_chunk_size=400)
        
        # Generar embeddings
        embeddings = generate_embeddings(chunks, API_KEY)

        # Almacenar los embeddings en ChromaDB
        store_embeddings(chunks, embeddings, collection_name=COLLECTION_NAME)
        print("Embeddings generados y almacenados exitosamente.")

    except Exception as e:
        print(f"Error al inicializar los embeddings: {e}")

@app.on_event("startup")
def startup_event():
    """
    Procesar el documento al iniciar la aplicación, si es necesario.
    """
    inicializar_embeddings()

# Definir el esquema del request
class SolicitudConsulta(BaseModel):
    user_name: str
    question: str

@app.post("/question-llm/")
async def question_llm(consulta: SolicitudConsulta):
    """
    Endpoint para responder preguntas utilizando un modelo de lenguaje grande (LLM).

    Parámetros:
    - consulta (SolicitudConsulta): Objeto que contiene el nombre del usuario y la pregunta.

    Retorna:
    - str: Respuesta generada por el modelo LLM.
    """
    try:
        # Buscar documentos relevantes
        documents, _ = search_similar_documents(consulta.question, API_KEY, collection_name=COLLECTION_NAME)

        # Generar una respuesta basada en los documentos relevantes
        answer_llm = generate_answer(consulta.question, documents, API_KEY)

        # Respuesta en formato json
        return {
            "user_name": consulta.user_name,
            "question": consulta.question,
            "answer": answer_llm
        }

    except Exception as e:
        return {"error": f"Error al procesar la consulta: {str(e)}"}