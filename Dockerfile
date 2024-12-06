# Usa una imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias de tu proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Expón el puerto 8000, que es donde FastAPI correrá
EXPOSE 8000

# Comando para ejecutar la API de FastAPI cuando el contenedor se inicie
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
