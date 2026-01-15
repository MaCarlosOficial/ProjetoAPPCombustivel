#!/bin/bash

# Iniciar a API de login na porta 8000 em segundo plano
uvicorn APIS.login:app --host 0.0.0.0 --port 8000 &
LOGIN_PID=$!

# Aguardar um pouco para a API de login iniciar
sleep 3

# Iniciar a API de consulta na porta 8001 em segundo plano  
uvicorn APIS.main:app --host 0.0.0.0 --port 8001 &
MAIN_PID=$!

echo "APIs iniciadas:"
echo "  Login API: http://localhost:8000"
echo "  Consulta API: http://localhost:8001"
echo "  Login API Docs: http://localhost:8000/docs"
echo "  Consulta API Docs: http://localhost:8001/docs"

# Função para encerrar ambas as APIs quando o container parar
trap "kill $LOGIN_PID $MAIN_PID" SIGINT SIGTERM

# Manter o container rodando
wait $LOGIN_PID $MAIN_PID