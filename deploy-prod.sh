#!/bin/bash
# ===========================================
# MeetingMind AI - Production Deployment Script
# ===========================================
# Usage: ./deploy-prod.sh
# ===========================================

set -e

echo "🚀 MeetingMind AI - Production Deployment"
echo "=========================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo -e "${YELLOW}⚠️  .env.production not found${NC}"
    echo "Creating from .env.production.example..."
    cp .env.production.example .env.production
    echo -e "${RED}❗ Please edit .env.production and set secure values!${NC}"
    echo "Required changes:"
    echo "  - SECRET_KEY"
    echo "  - JWT_SECRET_KEY"
    echo "  - POSTGRES_PASSWORD"
    echo "  - REDIS_PASSWORD"
    echo "  - OPENAI_API_KEY"
    echo "  - LLM_API_KEY"
    exit 1
fi

# Generate secure keys if not set
if grep -q "CHANGE_THIS" .env.production; then
    echo -e "${RED}❗ Please update .env.production with secure values!${NC}"
    echo "The following need to be changed:"
    grep "CHANGE_THIS" .env.production | head -5
    exit 1
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose found${NC}"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p docker/nginx/ssl
mkdir -p logs

# Generate self-signed SSL certificate (for testing only!)
# For production, use Let's Encrypt
if [ ! -f docker/nginx/ssl/fullchain.pem ]; then
    echo "🔐 Generating self-signed SSL certificate..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout docker/nginx/ssl/privkey.pem \
        -out docker/nginx/ssl/fullchain.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    echo -e "${YELLOW}⚠️  Self-signed certificate generated (for testing only!)${NC}"
    echo "For production, replace with Let's Encrypt certificate"
fi

# Build and start services
echo "🏗️  Building Docker images..."
docker-compose -f docker-compose.prod.yml build

echo "🚀 Starting services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Check health
echo "🏥 Checking service health..."
docker-compose -f docker-compose.prod.yml ps

# Show logs
echo ""
echo "📋 Service logs (last 20 lines):"
docker-compose -f docker-compose.prod.yml logs --tail=20

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "📍 Access points:"
echo "   • Frontend:    https://localhost"
echo "   • Backend API: https://localhost/api"
echo "   • API Docs:    https://localhost/docs"
echo "   • MinIO:       http://localhost:9001"
echo ""
echo "📋 Useful commands:"
echo "   • View logs:       docker-compose -f docker-compose.prod.yml logs -f"
echo "   • Stop services:   docker-compose -f docker-compose.prod.yml down"
echo "   • Restart:         docker-compose -f docker-compose.prod.yml restart"
echo "   • Scale worker:    docker-compose -f docker-compose.prod.yml up -d --scale worker=4"
echo ""
echo -e "${YELLOW}⚠️  For production SSL, replace the self-signed certificate with Let's Encrypt:${NC}"
echo "   certbot certonly --webroot -w /var/www/certbot -d your-domain.com"
echo ""
