# ========================================
# Prmpt - Makefile for Docker Operations
# ========================================
# Usage: make <target>
# Run `make help` for available commands
# ========================================

.PHONY: help build up down logs shell clean rebuild dev

# Default target
help:
	@echo.
	@echo Prmpt Docker Commands
	@echo =====================
	@echo.
	@echo   make build     - Build all Docker images
	@echo   make up        - Start all services
	@echo   make down      - Stop all services
	@echo   make logs      - View logs (follow mode)
	@echo   make shell     - Open shell in backend container
	@echo   make clean     - Remove containers, images, and volumes
	@echo   make rebuild   - Clean rebuild of all images
	@echo   make dev       - Start in development mode
	@echo.

# Build all images
build:
	docker compose build

# Start services in detached mode
up:
	docker compose up -d

# Stop all services
down:
	docker compose down

# View logs in follow mode
logs:
	docker compose logs -f

# Open shell in backend container
shell:
	docker compose exec backend sh

# Remove containers, images, and volumes
clean:
	docker compose down -v --rmi local

# Full rebuild (clean + build)
rebuild: clean build

# Development mode (foreground with logs)
dev:
	docker compose up

# Backend only commands
.PHONY: build-backend up-backend logs-backend

build-backend:
	docker compose build backend

up-backend:
	docker compose up -d backend

logs-backend:
	docker compose logs -f backend

# Health check
.PHONY: health

health:
	curl -s http://localhost:8000/health || echo Backend not running
