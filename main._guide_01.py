from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Modelo para la solicitud
class Numbers(BaseModel):
    num1: float
    num2: float

# Modelo para la solicitud
class FullName(BaseModel):
    first_name: str
    last_name: str

@app.post("/fullname/")
async def get_full_name(name: FullName):
    full_name = f"Tu nombre completo es: {name.first_name} {name.last_name}"
    return full_name


from fastapi import FastAPI
from pydantic import BaseModel
from app.document_processing import read_docx, split_into_chunks
from app.embeddings import generate_embeddings
from app.storage import store_embeddings
from app.search import search_similar_documents
from app.generate_answer import generate_answer

# Inicializar la aplicación FastAPI
app = FastAPI()

# Clave API de Cohere
API_KEY = "fbdkymnccgS3MtUK38jsJ0mVcU1mrqNOKpUBFMsd"

# Definir el esquema del request
class SolicitudConsulta(BaseModel):
    """
    Define el esquema de la solicitud que se enviará al endpoint.

    Atributos:
    - user_name (str): Nombre del usuario que realiza la consulta.
    - question (str): Pregunta o consulta que se desea responder.
    """
    user_name: str
    question: str

def procesar_documento():
    """
    Procesa un archivo `.docx`, lo divide en chunks, genera embeddings y los almacena en ChromaDB.

    Pasos:
    1. Lee el contenido del archivo `documento.docx`.
    2. Divide el texto en fragmentos (chunks) del tamaño especificado.
    3. Genera embeddings para cada fragmento utilizando Cohere.
    4. Almacena los chunks y embeddings en una colección de ChromaDB.
    """
    # Leer el contenido del documento
    content = read_docx('documento.docx')

    # Dividir en chunks
    chunks = split_into_chunks(content, max_chunk_size=400)

    # Generar embeddings
    embeddings = generate_embeddings(chunks, API_KEY)

    # Almacenar embeddings en ChromaDB
    collection = store_embeddings(chunks, embeddings)

@app.post("/question-llm/")
async def question_llm(consulta: SolicitudConsulta):
    """
    Endpoint para responder preguntas utilizando un modelo de lenguaje grande (LLM).

    Pasos:
    1. Procesa un archivo `.docx` y carga sus embeddings en ChromaDB.
    2. Busca los documentos más relevantes en ChromaDB basados en la consulta.
    3. Genera una respuesta utilizando el contexto de los documentos relevantes.

    Parámetros:
    - consulta (SolicitudConsulta): Objeto que contiene el nombre del usuario y la pregunta.

    Retorna:
    - str: Respuesta generada por el modelo LLM.
    """
    # Obtener el nombre del usuario y la consulta desde la solicitud
    user_name = consulta.user_name
    question = consulta.question

    # Cargar documento.docx en la colección de ChromaDB
    procesar_documento()

    # Buscar documentos relevantes
    documents, _ = search_similar_documents(question, API_KEY)

    # Generar una respuesta basada en los documentos relevantes
    answer_llm = generate_answer(question, documents, API_KEY)

    # Formatear la respuesta
    respuesta = f"Respuesta LLM: {answer_llm}"

    # Devolver la respuesta generada
    return respuesta
