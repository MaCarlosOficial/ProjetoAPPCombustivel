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

# Expor as portas das APIs
EXPOSE 8000 8001

# Script para iniciar ambas as APIs
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]