#!/bin/bash
cd /home/kostik/meetingmind/backend

# Принудительно устанавливаем переменные окружения
export DATABASE_URL="sqlite:///./meetingmind.db"
export SECRET_KEY="dev-secret-key"
export JWT_SECRET_KEY="dev-jwt-secret"

# Запуск сервера
exec ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
