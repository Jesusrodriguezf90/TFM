#!/bin/bash
echo "Iniciando API + frontend en puerto 8000..."
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000