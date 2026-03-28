# SkillBridge Rwanda

AI-powered job matching platform connecting skilled professionals with employment opportunities in Rwanda.

## Features

- **Conversational Skills Profiler**: Chat-based onboarding powered by Vertex AI Gemini Pro
- **AI Job Matching**: Semantic matching using text embeddings and vector search
- **Skill Gap Advisor**: Personalized training recommendations from Rwandan institutions
- **Employer Portal**: Post jobs and find matching candidates instantly
- **Labor Market Insights**: Real-time dashboard with market analytics

## Tech Stack

### Frontend
- Next.js 14 (App Router)
- Tailwind CSS
- Recharts for data visualization

### Backend
- Python FastAPI
- Vertex AI (Gemini 1.5 Pro, Text Embeddings)
- Cloud Translation API

### Infrastructure
- Google Cloud Run
- Cloud Firestore
- Cloud Storage

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- Google Cloud SDK
- GCP Project with billing enabled

### Local Development

1. **Clone and setup**
```bash
cd skillbridge-rwanda
cp .env.example .env
# Edit .env with your configuration
```

2. **Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

3. **Frontend**
```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:3000

### GCP Deployment

1. **Setup GCP resources**
```bash
export GCP_PROJECT_ID=your-project-id
export GCP_REGION=us-central1
cd infra
chmod +x setup.sh deploy.sh
./setup.sh
```

2. **Deploy**
```bash
./deploy.sh
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Send chat message for profiling |
| `/chat/finalize` | POST | Finalize candidate profile |
| `/match/{candidate_id}` | POST | Get job matches |
| `/match/gap/{candidate_id}/{job_id}` | POST | Get skill gap analysis |
| `/employer/jobs` | POST | Post a new job |
| `/employer/jobs` | GET | List all jobs |
| `/insights` | GET | Get labor market insights |

## Project Structure

```
skillbridge-rwanda/
├── frontend/          # Next.js app
├── backend/           # FastAPI app
├── infra/            # GCP setup scripts
├── seed_data/        # Sample job listings
└── README.md
```

## Environment Variables

See `.env.example` for all required configuration.

## Language Support

- English (en)
- Kinyarwanda (rw)

## License

MIT
