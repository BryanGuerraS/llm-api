"""
Módulo para procesar documentos `.docx` y dividir el texto en fragmentos.

Este módulo contiene:
- Función para leer el contenido de un archivo `.docx` y devolverlo como un texto concatenado.
- Función para dividir el texto en fragmentos (chunks) de un tamaño máximo especificado.
"""

from docx import Document

def read_docx(file_path):
    """
    Lee un archivo .docx y retorna el texto concatenado.

    Esta función abre un archivo .docx, extrae todo su texto (ignorando párrafos vacíos)
    y lo devuelve como una cadena de texto concatenada, separada por espacios.

    Parámetros:
    - file_path (str): Ruta al archivo .docx que se desea leer.

    Retorna:
    - str: El texto completo del documento, con los párrafos no vacíos concatenados.
    """
    doc = Document(file_path)
    text = []
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():  # Ignorar líneas vacías
            text.append(paragraph.text.strip())
    return " ".join(text)

def split_into_chunks(text, max_chunk_size):
    """
    Divide el texto en chunks del tamaño máximo especificado.

    Esta función toma un texto largo y lo divide en fragmentos (chunks) del tamaño máximo especificado.
    Si el texto excede el tamaño máximo, se crea un nuevo chunk. 

    Parámetros:
    - text (str): El texto que se desea dividir.
    - max_chunk_size (int): El tamaño máximo que cada chunk puede tener, en términos de número de caracteres.

    Retorna:
    - list: Una lista de cadenas (chunks) que contienen el texto dividido.
    """
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(" ".join(current_chunk)) >= max_chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:  # Agregar el último chunk si quedó algo
        chunks.append(" ".join(current_chunk))

    return chunks