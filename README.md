# Prmpt

A gamified prompt engineering academy - learn to craft effective AI prompts through interactive lessons.

## Project Structure

```
├── frontend/          # Next.js 15 + TypeScript + Tailwind
├── backend/           # FastAPI + Python
├── docker-compose.yml # Container orchestration
├── Makefile           # Docker commands
└── .env               # Environment variables (create from .env.example)
```

## Quick Start

### Using Docker (Recommended)

```bash
# 1. Copy environment file and add your keys
cp backend/.env.example .env

# 2. Build and run
make build
make up

# 3. View logs
make logs
```

**Available Make Commands:**
| Command | Description |
|---------|-------------|
| `make build` | Build all Docker images |
| `make up` | Start all services (detached) |
| `make down` | Stop all services |
| `make logs` | View logs (follow mode) |
| `make dev` | Start in foreground with logs |
| `make clean` | Remove containers and images |
| `make rebuild` | Full clean rebuild |
| `make health` | Check backend health |

### Local Development

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Environment Variables

Create a `.env` file in the project root (for Docker) or `backend/.env` (for local dev):

```bash
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_supabase_service_key

# AI Providers
OPENAI_API_KEY=your_openai_key
GOOGLE_AI_API_KEY=your_gemini_key
ANTHROPIC_API_KEY=your_claude_key
XAI_API_KEY=your_grok_key

# Optional
DEBUG=false
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Tech Stack

- **Frontend**: Next.js 15, TypeScript, Tailwind CSS, Framer Motion
- **Backend**: FastAPI, Python 3.11+
- **Auth/DB**: Supabase
- **AI Providers**: OpenAI, Google Gemini, Anthropic Claude, xAI Grok
- **Infrastructure**: Docker, Docker Compose

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API info |
| `GET /health` | Health check |
| `GET /api/levels` | Get all levels |
| `POST /api/judge` | Submit prompt for evaluation |

## 12-Factor App Compliance

This project follows [12-factor app](https://12factor.net/) methodology:
- ✅ Config via environment variables
- ✅ Stateless processes
- ✅ Port binding via `PORT` env var
- ✅ Logs to stdout/stderr
