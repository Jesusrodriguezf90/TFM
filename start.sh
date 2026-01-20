#!/bin/bash
echo "Iniciando API + frontend en puerto 8000..."
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000 #0.0.0.0 permite que el contenedor acepte conexiones fuera del contenedor, no solo localhost del contenedor.