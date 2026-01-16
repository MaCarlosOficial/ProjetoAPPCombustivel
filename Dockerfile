FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema se necessário
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro para aproveitar cache de camadas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos os arquivos da pasta APIS
COPY APIS/ ./APIS/

# Comando para iniciar
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]