#!/bin/bash

# MeetingMind AI - Quick Start Script

echo "🚀 MeetingMind AI - Quick Start"
echo "================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop or docker service."
    exit 1
fi

echo "✅ Docker is running"

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env and add your API keys (OPENAI_API_KEY, LLM_API_KEY)"
    echo ""
fi

# Check if API keys are set
if grep -q "OPENAI_API_KEY=" .env && ! grep -q "OPENAI_API_KEY=$" .env; then
    echo "✅ OpenAI API key found"
else
    echo "⚠️  OPENAI_API_KEY not set in .env"
    echo "   AI features will not work without it."
    echo "   You can add it later and restart."
fi

echo ""
echo "📦 Starting Docker containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo ""
echo "🏥 Checking service health..."

# Check backend
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend API is ready (http://localhost:8000)"
else
    echo "⏳ Backend API is starting..."
fi

# Check frontend
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is ready (http://localhost:3000)"
else
    echo "⏳ Frontend is starting..."
fi

# Check database
if docker-compose ps | grep -q "db.*healthy\|db.*Up"; then
    echo "✅ Database is ready"
else
    echo "⏳ Database is starting..."
fi

echo ""
echo "================================"
echo "🎉 MeetingMind AI is starting!"
echo "================================"
echo ""
echo "📍 Access points:"
echo "   • Frontend:    http://localhost:3000"
echo "   • Backend API: http://localhost:8000"
echo "   • API Docs:    http://localhost:8000/docs"
echo "   • MinIO:       http://localhost:9001 (minioadmin/minioadmin)"
echo ""
echo "📝 Next steps:"
echo "   1. Open http://localhost:3000"
echo "   2. Create your first account"
echo "   3. Create a new meeting"
echo ""
echo "📚 Documentation: docs/GETTING_STARTED.md"
echo ""
echo "🛑 To stop: docker-compose down"
echo ""
