# Prmpt

A gamified prompt engineering academy - learn to craft effective AI prompts through interactive lessons.

## Project Structure

```
├── frontend/     # Next.js 15 + TypeScript + Tailwind
└── backend/      # FastAPI + Python
```

## Quick Start

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
conda run -n CrawlerMode pip install -r requirements.txt
conda run -n CrawlerMode uvicorn main:app --reload --port 8000
```

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)
```
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_supabase_service_key
OPENAI_API_KEY=your_openai_key
GOOGLE_AI_API_KEY=your_gemini_key
ANTHROPIC_API_KEY=your_claude_key
XAI_API_KEY=your_grok_key
```

## Tech Stack

- **Frontend**: Next.js 15, TypeScript, Tailwind CSS, Framer Motion
- **Backend**: FastAPI, Python 3.11+
- **Auth/DB**: Supabase
- **AI Providers**: OpenAI, Google Gemini, Anthropic Claude, xAI Grok
