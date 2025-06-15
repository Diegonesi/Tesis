# Usar una imagen base de Python con Java preinstalado
FROM openjdk:11-jdk-slim

# Instalar Python
RUN apt-get update && apt-get install -y python3 python3-pip && apt-get clean

# Copiar el archivo de requerimientos y el código
COPY requirements.txt /app/requirements.txt
COPY . /app

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias de Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Comando para ejecutar el script
CMD ["python3", "Beam-Search_Spark.py"]