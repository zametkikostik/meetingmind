# 🚀 MeetingMind AI - Быстрый Запуск

## ⚠️ Проблема с Internal Server Error

Ошибка возникает потому что для работы требуется **PostgreSQL база данных**.

## ✅ Решение 1: Docker (Рекомендуется)

```bash
cd /home/kostik/meetingmind
docker-compose up -d
```

Это запустит:
- PostgreSQL (база данных)
- Redis (кэш)
- MinIO (хранилище)
- Backend
- Frontend

## ✅ Решение 2: Локальный PostgreSQL

```bash
# Установить PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Запустить
sudo systemctl start postgresql

# Создать базу данных
sudo -u postgres psql <<EOF
CREATE DATABASE meetingmind;
CREATE USER meetingmind WITH PASSWORD 'meetingmind_password';
GRANT ALL PRIVILEGES ON DATABASE meetingmind TO meetingmind;
\q
EOF

# Обновить .env
nano .env
# Изменить DATABASE_URL на:
# DATABASE_URL=postgresql://meetingmind:meetingmind_password@localhost:5432/meetingmind
```

## ✅ Решение 3: Исправление для SQLite (Демо режим)

Для работы с SQLite нужно заменить все `JSONB` на `JSON` в моделях.

---

## 📝 Текущий статус

```
✅ Backend зависимости установлены
✅ Frontend зависимости установлены
✅ Код исправлен (импорты, типы)
⚠️ Требуется PostgreSQL для запуска
```

---

## 🔧 Проверка после установки БД

```bash
# Terminal 1 - Backend
cd /home/kostik/meetingmind/backend
./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
cd /home/kostik/meetingmind/frontend
npm run dev
```

**Проверка:**
- http://localhost:8000/health
- http://localhost:3000

---

**Internal Server Error исчезнет после подключения к PostgreSQL!**
