# 🧠 MeetingMind AI

**AI-powered meeting assistant** — Записывайте, транскрибируйте и анализируйте встречи с помощью искусственного интеллекта.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

---

## ✨ Возможности

| Функция | Описание |
|---------|----------|
| 🎙️ **Транскрипция** | Автоматическая расшифровка аудио в текст (Whisper AI) |
| 🤖 **AI Анализ** | Саммари, ключевые темы, задачи из встреч |
| 📊 **Deep Analytics** | Talk time, sentiment analysis, emotion heatmap |
| 📔 **Заметки** | Личные заметки с тегами и привязкой к встречам |
| 📅 **Календарь** | Интеграция с Google/Outlook календарями |
| 💬 **Комментарии** | Обсуждения к встречам и транскриптам |
| 🔗 **Sharing** | Общий доступ к встречам с командой |
| 🤖 **AI Templates** | Пользовательские шаблоны анализа |
| 🔐 **Безопасность** | JWT аутентификация, E2E шифрование |

---

## 🚀 Быстрый старт

### Требования
- Docker & Docker Compose
- Node.js 20+ (опционально, для разработки)
- Python 3.11+ (опционально, для разработки)

### 1. Клонировать репозиторий
```bash
git clone https://github.com/YOUR_USERNAME/meetingmind.git
cd meetingmind
```

### 2. Настроить окружение
```bash
# Production
cp .env.production.example .env.production
nano .env.production  # Отредактируйте секреты

# Development
cp .env.example .env
```

### 3. Запустить production версию
```bash
./deploy-prod.sh
```

### 4. Запустить development версию
```bash
docker-compose up -d
```

### 5. Открыть в браузере
```
Production:  https://localhost
Development: http://localhost:3000
```

---

## 🏗️ Архитектура

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Desktop Client │────▶│   Backend API    │────▶│   AI Engine     │
│  (Electron)     │     │   (FastAPI)      │     │   (Whisper+LLM) │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                       │                        │
         ▼                       ▼                        ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Local Recording│     │  PostgreSQL DB   │     │  S3 Storage     │
│  & Noise Cancel │     │  + Redis Cache   │     │  (Recordings)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

---

## 📁 Структура проекта

```
meetingmind/
├── backend/              # FastAPI сервер
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Конфигурация, безопасность
│   │   ├── db/           # База данных
│   │   ├── models/       # SQLAlchemy модели
│   │   ├── schemas/      # Pydantic схемы
│   │   └── services/     # Бизнес-логика
│   ├── tests/            # Тесты
│   ├── Dockerfile        # Dev Dockerfile
│   └── Dockerfile.prod   # Production Dockerfile
├── frontend/             # React приложение
│   ├── src/
│   │   ├── components/   # UI компоненты
│   │   ├── pages/        # Страницы
│   │   ├── hooks/        # React хуки
│   │   ├── lib/          # Утилиты
│   │   └── store/        # Zustand store
│   ├── Dockerfile
│   └── Dockerfile.prod
├── ai-engine/            # AI модули
│   ├── transcription/    # Whisper транскрипция
│   └── analysis/         # LLM анализ
├── docker/               # Docker конфиги
│   ├── nginx/            # Nginx конфигурация
│   └── postgres/         # PostgreSQL init
├── docs/                 # Документация
├── docker-compose.yml    # Dev compose
├── docker-compose.prod.yml  # Production compose
└── deploy-prod.sh        # Production deploy script
```

---

## 🔧 Технологический стек

### Backend
- **FastAPI** — веб-фреймворк
- **PostgreSQL** — основная БД
- **Redis** — кэш и очереди
- **SQLAlchemy** — ORM
- **Pydantic** — валидация данных
- **Celery** — фоновые задачи

### AI Engine
- **OpenAI Whisper** — транскрипция
- **LLM (GPT-4/Claude)** — анализ встреч
- **PyTorch** — ML inference

### Frontend
- **React 18** — UI фреймворк
- **TypeScript** — типизация
- **Tailwind CSS** — стилизация
- **Zustand** — state management
- **React Query** — data fetching

### Infrastructure
- **Docker** — контейнеризация
- **Nginx** — reverse proxy
- **MinIO** — S3 storage

---

## 📊 Сравнение с аналогами

| Функция | Fireflies.ai | Otter.ai | MeetingMind AI |
|---------|--------------|----------|----------------|
| Транскрипция | ✅ | ✅ | ✅ |
| AI Summary | ✅ | ✅ | ✅ |
| Action Items | ✅ | ⚠️ | ✅ |
| **Заметки** | ⚠️ | ❌ | ✅ |
| **Календарь** | ⚠️ | ❌ | ✅ |
| **Комментарии** | ❌ | ❌ | ✅ |
| **Sharing** | ⚠️ | ⚠️ | ✅ |
| **AI Templates** | ❌ | ❌ | ✅ |
| **Self-hosted** | ❌ | ❌ | ✅ |
| **E2E Encryption** | ❌ | ❌ | ✅ |

---

## 🔒 Безопасность

- JWT аутентификация с refresh токенами
- Bcrypt хэширование паролей
- CORS политика
- Rate limiting
- SQL injection защита (SQLAlchemy ORM)
- Поддержка HTTPS

---

## 📖 Документация

- [API Documentation](docs/API.md)
- [Getting Started](docs/GETTING_STARTED.md)
- [Production Deployment](docs/PRODUCTION.md)
- [Features](docs/FEATURES.md)
- [Roadmap](docs/ROADMAP.md)

---

## 🤝 Contributing

1. Fork репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменений (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

---

## 📄 Лицензия

MIT License — см. [LICENSE](LICENSE)

---

## 📞 Контакты

- **Website:** https://meetingmind.ai
- **Email:** support@meetingmind.ai
- **Discord:** https://discord.gg/meetingmind
- **Twitter:** @MeetingMindAI

---

## 🙏 Благодарности

- [OpenAI](https://openai.com/) за Whisper API
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [All contributors](../../graphs/contributors)

---

**Made with ❤️ by MeetingMind Team**
