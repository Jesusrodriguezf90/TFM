# Imagen base ligera de Python
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Se instalan las librerías del sistema necesarias para LightGBM
RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*

# Se copian dependencias y se instalan
COPY requirements/requirements_dev.txt .
RUN pip install --no-cache-dir -r requirements_dev.txt

# Se copia el código fuente y web
COPY src/ src/
COPY web/ web/

# Se copia el script de inicio
COPY start.sh .
RUN chmod +x start.sh

# Se agrega PYTHONPATH para que los imports funcionen
ENV PYTHONPATH=/app

# Se exponen los puertos de la API y la web
EXPOSE 8000

# Comando por defecto para ejecutar API + web
CMD ["./start.sh"]