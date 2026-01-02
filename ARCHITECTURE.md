# Architecture: Multi-Phase Todo Application

## Overview

This document describes the architecture of the multi-phase todo application that evolves from a console application to a cloud-native distributed system.

## Phase I: Console Application

- **Technology Stack**: Python 3.11+, Rich, Pydantic, pytest
- **Architecture**: Clean architecture with separation of concerns
- **Components**:
  - `src/models/` - Data models (Todo, User)
  - `src/services/` - Business logic (TodoService, ValidationService)
  - `src/cli/` - Rich CLI interface
  - `tests/` - Unit and integration tests

## Phase II: Web Application

- **Technology Stack**: Next.js 14+, TypeScript, Tailwind CSS, FastAPI, SQLModel, Neon DB
- **Architecture**: Full-stack application with API endpoints
- **Components**:
  - `backend/` - FastAPI backend with authentication
  - `frontend/` - Next.js frontend with responsive UI
  - `database/` - PostgreSQL integration via SQLModel

## Phase III: AI Chatbot

- **Technology Stack**: OpenAI ChatKit, Agents SDK, MCP SDK, Qwen API
- **Architecture**: Natural language processing with intent recognition
- **Components**:
  - `ai-chatbot/` - AI service with NLU capabilities

## Phase IV: Kubernetes Deployment

- **Technology Stack**: Docker, Minikube, Helm, Prometheus, Grafana
- **Architecture**: Containerized microservices with orchestration
- **Components**:
  - `k8s/` - Helm charts and Kubernetes manifests

## Phase V: Cloud Production

- **Technology Stack**: Kafka, Dapr, DigitalOcean DOKS, GitHub Actions, Zipkin
- **Architecture**: Production-scale distributed system
- **Components**:
  - `.infra/` - Cloud infrastructure as code