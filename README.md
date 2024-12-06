# 🚀 LLM API con FastAPI y Docker 🌟
¡Bienvenido al proyecto LLM API! 🎉 Este repositorio contiene una implementación de una API que utiliza FastAPI para procesar preguntas, buscar texto relevante y generar respuestas utilizando un modelo de lenguaje grande (LLM). La aplicación se integra con Cohere para la generación de embeddings y ChromaDB para la búsqueda de similitudes.


## 🌟 Características principales
- 🔍 Procesa documentos .docx, dividiéndolos en fragmentos (chunks) y almacenando sus embeddings.  
- 🤖 Genera respuestas concisas y relevantes a preguntas del usuario.  
- 🗄️ Utiliza ChromaDB para buscar documentos similares.  
- 📦 Se puede ejecutar en un contenedor Docker para facilitar su despliegue


## 📂 Estructura del proyecto
```console
📁 app  
├── document_processing.py  # Procesa documentos y los divide en chunks.  
├── embeddings.py           # Genera embeddings utilizando Cohere.  
├── storage.py              # Almacena chunks y embeddings en ChromaDB.  
├── search.py               # Busca documentos relevantes en ChromaDB.  
├── generate_answer.py      # Genera respuestas basadas en documentos relevantes.  
📁 postman                  # Contiene la colección de Postman para probar la API.  
├── LLM_API.postman_collection.json  # Colección de Postman exportada.  
Dockerfile                  # Configuración para construir la imagen Docker.  
main.py                     # Archivo principal de la API.  
requirements.txt            # Librerías necesarias para el proyecto.
```

## 🚀 Cómo ejecutar el proyecto
### 1️⃣ Requisitos previos
- 🐍 Python 3.9+  
- 🐳 Docker instalado.  
- 🧪 Postman o cualquier cliente HTTP para probar la API.

### 2️⃣ Ejecución local
1. Clona el repositorio:
```console
git clone https://github.com/tu_usuario/llm-api.git
cd llm-api
```
2. Crea un entorno virtual e instala las dependencias:
```console
python -m venv env
source env/bin/activate  # En Windows: .\env\Scripts\activate
pip install -r requirements.txt
```
3. Ejecuta la aplicación
```console
uvicorn main:app --reload
```
4. Prueba la API
Prueba la API:
- Visita: http://127.0.0.1:8000 para comprobar que la API está activa.
- Usa Postman para probar el endpoint principal /question-llm/.
### 3️⃣ Ejecución con Docker
1. Construye la imagen Docker:
```console
docker build -t llm-api .
```
2. Ejecuta el contenedor:
```console
docker run -p 8000:8000 llm-api
```
3. Prueba la API:
- La API estará disponible en: http://127.0.0.1:8000.


## 🛠️ Endpoints principales
### POST /question-llm/
- Procesa una pregunta y genera una respuesta basada en documentos relevantes.
Request Body:
```console
{
    "user_name": "Bryan_Guerra",
    "question": "Quien es Zara?"
}
```
Respuesta:
```console
{
    "user_name": "Bryan_Guerra",
    "question": "Quien es Zara?",
    "answer": "Zara es un intrépido explorador en la galaxia de Zenthoria, que descubre un antiguo artefacto clave para la paz entre los Dracorians y los Lumis. 🌌️🛡️🛸"
}
```

## 📦 Postman Collection
Se incluye una colección de Postman en la carpeta postman/ con el archivo LLM_API.postman_collection.json.

Cómo usarla:
1. Abre Postman y selecciona Importar.
2. Carga el archivo postman/LLM_API.postman_collection.json desde tu proyecto.
3. ¡Prueba los endpoints fácilmente! 🎉

## 📖 Documentación adicional
- Docker: Este proyecto incluye un archivo Dockerfile que permite desplegar la API rápidamente en un contenedor.
- Readability: Código modular y bien documentado siguiendo buenas prácticas.

## 🌍 Contribuciones
¡Las contribuciones son bienvenidas! Si encuentras un problema o deseas agregar una mejora, por favor abre un issue o envía un pull request. 🙌