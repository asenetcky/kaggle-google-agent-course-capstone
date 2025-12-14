# 🐳 Docker Deployment Guide for Toddle Ops

This guide explains how to run Toddle Ops using Docker and Docker Compose.

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

The easiest way to run Toddle Ops with all dependencies:

```bash
# 1. Make sure .env file exists with required variables
cp .env.example .env
# Edit .env and add your API keys

# 2. Start the application
docker-compose up -d

# 3. Access the UI
# Open http://localhost:8501 in your browser

# 4. View logs
docker-compose logs -f toddle-ops

# 5. Stop the application
docker-compose down
```

### Option 2: Docker Run

Build and run the container directly:

```bash
# Build the image
docker build -t toddle-ops:latest .

# Run the container
docker run -d \
  --name toddle-ops-ui \
  -p 8501:8501 \
  -e GOOGLE_API_KEY=${GOOGLE_API_KEY} \
  -e SUPABASE_USER=${SUPABASE_USER} \
  -e SUPABASE_PASSWORD=${SUPABASE_PASSWORD} \
  --env-file .env \
  toddle-ops:latest

# View logs
docker logs -f toddle-ops-ui

# Stop the container
docker stop toddle-ops-ui && docker rm toddle-ops-ui
```

### Option 3: Makefile Commands

Convenient shortcuts:

```bash
# Build Docker image
make docker-build

# Start with Docker Compose
make docker-run

# View logs
make docker-logs

# Stop containers
make docker-stop
```

## 📋 Requirements

- **Docker** 24.0+ ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose** 2.0+ (included with Docker Desktop)
- **API Keys** (see below)

## 🔐 Environment Variables

Required environment variables in `.env`:

```bash
# Required: Google Gemini API
GOOGLE_API_KEY=your_gemini_api_key_here

# Required: Supabase Database
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your_supabase_password

# Optional: For production deployments
GOOGLE_PROJECT_ID=your_project_id
DEPLOYED_REGION=us-central1
```

## 🏗️ Architecture

The Docker setup includes:

### Dockerfile
- **Base Image:** Python 3.13-slim
- **Package Manager:** uv (fast Python package installer)
- **User:** Non-root user for security
- **Port:** 8501 (Streamlit default)
- **Health Check:** Built into compose file

### docker-compose.yml
- **Service:** toddle-ops (main application)
- **Optional:** PostgreSQL service (for local development without Supabase)
- **Networking:** Isolated bridge network
- **Volumes:** Optional source code mounting for development

## 🎨 Streamlit UI Features

The web interface provides:

- 💬 **Chat Interface** - Natural conversation with the AI agent
- 📊 **Session Management** - Persistent conversations across restarts
- 🎯 **Quick Prompts** - Pre-made suggestions for common requests
- 🛡️ **Safety Notes** - Important reminders for supervision
- 📝 **Formatted Output** - Clean, readable project instructions
- 🔄 **Session Reset** - Start fresh conversations anytime

## 🔧 Development Mode

For development with hot-reloading:

1. **Uncomment volume mount** in `docker-compose.yml`:
   ```yaml
   volumes:
     - ./src:/app/src:ro
   ```

2. **Restart container**:
   ```bash
   docker-compose restart
   ```

3. **Changes to Python files** will require container restart, but Streamlit will auto-reload

## 🔍 Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs toddle-ops

# Common issues:
# - Missing GOOGLE_API_KEY
# - Invalid Supabase credentials
# - Port 8501 already in use
```

### Database connection errors
```bash
# Test Supabase connection
docker-compose exec toddle-ops python -c "
from toddle_ops.services.sessions import session_service
print('Connection successful!')
"

# If using local PostgreSQL, uncomment in docker-compose.yml
```

### Port already in use
```bash
# Change port in docker-compose.yml
ports:
  - "8502:8501"  # Use 8502 instead
```

### Image build fails
```bash
# Clear cache and rebuild
docker builder prune
docker-compose build --no-cache
```

## 🌐 Production Deployment

### 1. Using Docker Hub

```bash
# Build and tag
docker build -t yourusername/toddle-ops:v0.3.0 .
docker tag yourusername/toddle-ops:v0.3.0 yourusername/toddle-ops:latest

# Push to Docker Hub
docker push yourusername/toddle-ops:v0.3.0
docker push yourusername/toddle-ops:latest

# Run on production server
docker pull yourusername/toddle-ops:latest
docker run -d \
  --name toddle-ops \
  -p 80:8501 \
  --env-file .env \
  --restart unless-stopped \
  yourusername/toddle-ops:latest
```

### 2. Using GitHub Container Registry (ghcr.io)

Images are automatically built and published via GitHub Actions:

```bash
# Pull the latest image
docker pull ghcr.io/asenetcky/toddle-ops:latest

# Run it
docker run -d \
  --name toddle-ops \
  -p 8501:8501 \
  --env-file .env \
  ghcr.io/asenetcky/toddle-ops:latest
```

### 3. Cloud Deployment Options

#### **Google Cloud Run**
```bash
# Build for Cloud Run
gcloud builds submit --tag gcr.io/PROJECT-ID/toddle-ops

# Deploy
gcloud run deploy toddle-ops \
  --image gcr.io/PROJECT-ID/toddle-ops \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=${GOOGLE_API_KEY}
```

#### **AWS ECS/Fargate**
Use the Dockerfile with AWS ECS task definitions.

#### **Azure Container Instances**
```bash
az container create \
  --resource-group toddle-ops \
  --name toddle-ops-ui \
  --image ghcr.io/asenetcky/toddle-ops:latest \
  --dns-name-label toddle-ops \
  --ports 8501 \
  --environment-variables GOOGLE_API_KEY=${GOOGLE_API_KEY}
```

#### **Railway / Render / Fly.io**
These platforms support Docker deployment via git push or Docker image.

## 🔒 Security Best Practices

1. **Never commit `.env` file** - Added to `.gitignore`
2. **Use secrets management** in production (AWS Secrets Manager, Google Secret Manager)
3. **Enable HTTPS** via reverse proxy (nginx, Caddy, Traefik)
4. **Restrict network access** with firewall rules
5. **Scan images** for vulnerabilities:
   ```bash
   docker scan toddle-ops:latest
   ```

## 📊 Monitoring

### Health Checks
```bash
# Check if container is healthy
docker ps --filter "name=toddle-ops"

# Test health endpoint
curl http://localhost:8501/_stcore/health
```

### Resource Usage
```bash
# Monitor container stats
docker stats toddle-ops-ui

# View detailed info
docker inspect toddle-ops-ui
```

## 🧹 Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove images
docker rmi toddle-ops:latest

# Remove all unused Docker resources
docker system prune -a
```

## 🎯 Next Steps

1. ✅ Set up environment variables
2. ✅ Build and run the container
3. ✅ Access the UI at http://localhost:8501
4. ✅ Generate your first toddler project!
5. 📈 Consider adding monitoring (Prometheus, Grafana)
6. 🔐 Set up authentication if exposing publicly
7. 🌐 Deploy to production cloud platform

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Docker Documentation](https://docs.docker.com/)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Supabase Documentation](https://supabase.com/docs)

## 💡 Tips

- **Local Development:** Use `make ui` to run Streamlit locally without Docker
- **Debugging:** Add `--server.runOnSave=true` to CMD in Dockerfile for auto-reload
- **Performance:** Increase container resources if experiencing slowdowns
- **Scaling:** Use Docker Swarm or Kubernetes for multi-container deployment
