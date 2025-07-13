# 🐳 Docker Deployment Guide

This guide provides quick instructions for deploying the ML Feature Engineering API using Docker.

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed
- Docker Compose available

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd ml-assignment
```

### 2. Start with Docker Compose
```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f
```

### 3. Access Services
- **API Server**: http://localhost:8002
- **Documentation**: http://localhost:5002/docs
- **Health Check**: http://localhost:8002/health

### 4. Stop Services
```bash
docker compose down
```

## 📋 Alternative Methods

### Using Docker Start Script
```bash
# Make executable
chmod +x docker-start.sh

# Start services
./docker-start.sh

# Stop services
./docker-start.sh stop
```

### Manual Docker Build
```bash
# Build image
docker build -t ml-feature-api .

# Run container
docker run -d \
  --name ml-feature-api \
  -p 8002:8002 \
  -p 5002:5002 \
  ml-feature-api
```

## 🔧 Management Commands

```bash
# View status
docker compose ps

# View logs
docker compose logs -f

# Restart services
docker compose restart

# Update and rebuild
docker compose down
docker compose build --no-cache
docker compose up -d
```

## 🏥 Health Monitoring

The container includes automatic health checks:
- **Endpoint**: http://localhost:8002/health
- **Interval**: Every 30 seconds
- **Auto-restart**: If unhealthy

## 🛠️ Troubleshooting

### Common Issues
```bash
# Check logs
docker compose logs ml-feature-api

# Check Docker status
docker info

# Rebuild from scratch
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Port Conflicts
```bash
# Check port usage
lsof -i :8002
lsof -i :5002

# Kill processes if needed
kill $(lsof -t -i:8002)
kill $(lsof -t -i:5002)
```

## 📊 Production Features

✅ **Auto-restart**: Container restarts if it crashes
✅ **Health checks**: Automatic health monitoring
✅ **Volume mounting**: Data persistence
✅ **Network isolation**: Secure container networking
✅ **Resource limits**: Optimized resource usage

## 📝 Environment Variables

```bash
# Customize deployment
PYTHONUNBUFFERED=1
NODE_ENV=production
```

## 🎯 API Testing

Once running, test the API:

```bash
# Health check
curl http://localhost:8002/health

# Test feature calculation
curl -X POST "http://localhost:8002/calculate-features" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "docker_test",
    "application_date": "2024-02-12T19:24:29.135000",
    "contracts": []
  }'
```

## 🔗 Links

- **API Documentation**: http://localhost:8002/docs
- **Interactive Docs**: http://localhost:5002/docs
- **Health Check**: http://localhost:8002/health

For detailed documentation, see [API Documentation](docs/api_documentation.md). 