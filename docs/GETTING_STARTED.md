# Getting Started with MeetingMind AI

## Prerequisites

- Docker & Docker Compose
- Node.js 20+ (optional, for local frontend development)
- Python 3.11+ (optional, for local backend development)

## Quick Start with Docker

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/meetingmind.git
cd meetingmind
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set your API keys:

```bash
# OpenAI API Key (for Whisper transcription)
OPENAI_API_KEY=sk-your-openai-api-key

# LLM API Key (for meeting analysis)
LLM_API_KEY=sk-your-llm-api-key
```

### 3. Start All Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis cache
- MinIO (S3 storage)
- Backend API (FastAPI)
- Celery worker
- Frontend (React)
- Bucket initialization

### 4. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **MinIO Console:** http://localhost:9001 (minioadmin/minioadmin)

### 5. Create Your First Account

1. Open http://localhost:3000
2. Click "Sign up"
3. Enter your email and password
4. Start creating meetings!

---

## Development Setup

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (if using Alembic)
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

---

## Architecture Overview

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

## Common Issues

### Database Connection Error

Make sure PostgreSQL is running:
```bash
docker-compose ps db
```

Restart if needed:
```bash
docker-compose restart db
```

### Frontend Won't Start

Clear node_modules and reinstall:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### AI Processing Fails

Check that API keys are set correctly in `.env`:
```bash
docker-compose logs worker | grep -i error
```

---

## Next Steps

1. **Configure Integrations:** Set up Zoom/Google Meet integrations
2. **Customize AI Models:** Adjust Whisper and LLM settings
3. **Set Up Desktop Client:** Build the Electron app for silent recording
4. **Configure S3:** Set up production S3 storage

---

## Support

- Documentation: https://docs.meetingmind.ai
- Issues: https://github.com/meetingmind/meetingmind/issues
- Discord: https://discord.gg/meetingmind
