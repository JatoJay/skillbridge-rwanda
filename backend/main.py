from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat, match, employer, insights
from config import get_settings

settings = get_settings()

app = FastAPI(
    title="SkillBridge Rwanda API",
    description="AI-powered job matching platform for Rwanda",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(match.router)
app.include_router(employer.router)
app.include_router(insights.router)


@app.get("/")
async def root():
    return {
        "name": "SkillBridge Rwanda API",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "chat": "/chat",
            "match": "/match/{candidate_id}",
            "gap_analysis": "/match/gap/{candidate_id}/{job_id}",
            "employer": "/employer/jobs",
            "insights": "/insights"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
