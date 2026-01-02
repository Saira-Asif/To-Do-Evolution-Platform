# Quickstart Guide: Multi-Phase Todo Application

**Feature**: 001-todo-app-arch-evolution
**Date**: 2026-01-02

## Overview

This guide provides quick setup instructions for each phase of the Multi-Phase Todo Application, from the console application to the cloud-native deployment.

## Prerequisites

### System Requirements
- Python 3.11+ with pip
- Node.js 20+ with npm
- Docker (for Phases IV and V)
- Git
- DigitalOcean account (for Phase V)

### Development Tools
- A modern code editor (VS Code recommended)
- Terminal/shell access
- Git client

## Phase I: Console Application Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todo-evolution-platform
```

### 2. Set up Python Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install rich pydantic pytest mypy
```

### 3. Run the Console Application
```bash
# Navigate to Phase I source
cd src/cli

# Run the application
python main.py --help
```

### 4. Run Tests
```bash
# From project root
pytest src/ --cov --cov-report=html

# Run type checking
mypy src/
```

### 5. Basic Usage
```bash
# Add a todo
python src/cli/main.py add "Buy groceries"

# List todos
python src/cli/main.py list

# Complete a todo
python src/cli/main.py complete 1

# Update a todo
python src/cli/main.py update 1 "Buy groceries - urgent"
```

## Phase II: Web Application Setup

### 1. Backend Setup
```bash
# From project root
cd backend

# Activate Python environment
source ../venv/bin/activate

# Install backend dependencies
pip install fastapi uvicorn sqlmodel python-multipart python-jose[cryptography] passlib[bcrypt] psycopg2-binary

# Set up database
uvicorn src.api.main:app --reload
```

### 2. Frontend Setup
```bash
# Open new terminal, from project root
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 3. Database Setup
```bash
# Ensure PostgreSQL is running (Neon DB recommended)
# Create .env file with database connection details:
DATABASE_URL="postgresql://username:password@localhost:5432/todo_db"
```

### 4. API Documentation
- Open http://localhost:8000/docs for auto-generated OpenAPI documentation
- API endpoints available at http://localhost:8000/api/v1/

## Phase III: AI Chatbot Integration

### 1. AI Service Setup
```bash
# Install AI dependencies
pip install openai python-dotenv

# Add API keys to .env:
OPENAI_API_KEY="your-openai-api-key"
QWEN_API_KEY="your-qwen-api-key"
```

### 2. Start AI Chatbot
```bash
# From project root
cd ai-chatbot
python -m uvicorn src.main:app --reload
```

### 3. Test AI Integration
```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "remind me tomorrow at 3pm"}'
```

## Phase IV: Kubernetes Deployment

### 1. Install Prerequisites
```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Start Minikube
minikube start
```

### 2. Deploy Application
```bash
# From project root
cd k8s/helm

# Install the application
helm install todo-app .
```

### 3. Access Services
```bash
# Get service URLs
minikube service todo-frontend --url
minikube service todo-backend --url
minikube service todo-chatbot --url
```

### 4. Monitor with Prometheus/Grafana
```bash
# Start Grafana
minikube service grafana --url
```

## Phase V: Cloud Production Deployment

### 1. DigitalOcean Setup
```bash
# Install doctl
curl -sL https://repos.insomnia.rest/get-insomnia.sh | sudo bash -

# Authenticate
doctl auth init
```

### 2. Create DOKS Cluster
```bash
doctl kubernetes cluster create todo-cluster --region nyc1
```

### 3. Deploy to DOKS
```bash
# Configure kubectl
doctl kubernetes cluster kubeconfig save todo-cluster

# Deploy using Helm
helm install todo-app-prod .
```

### 4. Set up Kafka and Dapr
```bash
# Install Dapr
dapr init -k

# Configure Kafka
kubectl apply -f .infra/kafka/
```

## Running Tests Across All Phases

### Unit Tests
```bash
# Phase I
pytest src/ -v

# Phase II
pytest backend/src/ -v
npm test --prefix frontend

# Phase III
pytest ai-chatbot/src/ -v
```

### Integration Tests
```bash
# Backend integration tests
pytest backend/tests/integration/ -v

# E2E tests with Playwright
npx playwright test --project=chromium
```

### Performance Tests
```bash
# Load test with Apache Bench
ab -n 1000 -c 10 http://localhost:8000/api/v1/todos/
```

## Common Commands

### Development
```bash
# Start all services (requires multiple terminals)
# Terminal 1: Backend
cd backend && uvicorn src.api.main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev

# Terminal 3: AI Service
cd ai-chatbot && uvicorn src.main:app --reload
```

### Database Migrations
```bash
# Generate migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

### Docker Commands
```bash
# Build all services
docker-compose build

# Run all services
docker-compose up -d
```

## Troubleshooting

### Phase I Issues
- **Rich not found**: Ensure virtual environment is activated and dependencies installed
- **Type checking errors**: Run `mypy src/` to identify specific issues

### Phase II Issues
- **Database connection**: Verify PostgreSQL is running and credentials are correct
- **CORS errors**: Check frontend origin is allowed in backend configuration

### Phase III Issues
- **API rate limits**: Implement retry logic and caching for AI API calls
- **Intent recognition**: Verify API keys and model availability

### Phase IV Issues
- **Kubernetes resources**: Ensure sufficient memory and CPU for Minikube
- **Service discovery**: Check that services are properly exposed

### Phase V Issues
- **Cloud connectivity**: Verify DigitalOcean credentials and cluster access
- **Auto-scaling**: Check HPA configuration and resource metrics

## Next Steps

1. Complete Phase I implementation before moving to Phase II
2. Ensure all tests pass at each phase before proceeding
3. Review the architecture documentation for each phase
4. Follow the task breakdown in tasks.md for implementation details