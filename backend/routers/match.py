from fastapi import APIRouter, HTTPException
from models.job import JobMatch, SkillGapReport
from services.gemini_service import gemini_service
from services.embedding_service import embedding_service
from services.vector_search import vector_search_service
from services.database import db

router = APIRouter(prefix="/match", tags=["matching"])


@router.post("/{candidate_id}")
async def match_jobs_for_candidate(candidate_id: str, top_k: int = 5):
    try:
        candidate = await db.get_candidate(candidate_id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")

        candidate_embedding = candidate.get("embedding")
        if not candidate_embedding:
            profile_text = embedding_service.create_candidate_text(candidate)
            candidate_embedding = await embedding_service.get_embedding(profile_text)
            await db.update_candidate(candidate_id, {"embedding": candidate_embedding})
            await vector_search_service.index_candidate(candidate_id, candidate_embedding)

        all_jobs = await db.get_active_jobs()
        for job in all_jobs:
            if not job.get("embedding"):
                job_text = embedding_service.create_job_text(job)
                job_embedding = await embedding_service.get_embedding(job_text)
                job["embedding"] = job_embedding
                await vector_search_service.index_job(job["id"], job_embedding)

        matches = await vector_search_service.search_jobs_for_candidate(
            candidate_embedding, top_k
        )

        candidate_skills = [
            s.get("name") if isinstance(s, dict) else s
            for s in candidate.get("skills", [])
        ]
        candidate_bio = candidate.get("bio", "")

        results = []
        for job_id, score in matches:
            job = await db.get_job(job_id)
            if job:
                explanation = await gemini_service.generate_match_explanation(
                    candidate_bio,
                    candidate_skills,
                    job.get("title", ""),
                    job.get("description", ""),
                    score
                )

                required_skills = set(job.get("required_skills", []))
                candidate_skills_set = set(candidate_skills)
                skill_gaps = list(required_skills - candidate_skills_set)

                await db.record_match(candidate_id, job_id, score)

                job_copy = job.copy()
                job_copy.pop("embedding", None)

                results.append({
                    "job": job_copy,
                    "score": round(score * 100, 1),
                    "explanation": explanation,
                    "skill_gaps": skill_gaps
                })

        return {"matches": results, "total": len(results)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/gap/{candidate_id}/{job_id}", response_model=SkillGapReport)
async def analyze_skill_gap(candidate_id: str, job_id: str):
    try:
        candidate = await db.get_candidate(candidate_id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")

        job = await db.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        candidate_skills = [
            s.get("name") if isinstance(s, dict) else s
            for s in candidate.get("skills", [])
        ]
        required_skills = job.get("required_skills", [])

        gap_analysis = await gemini_service.analyze_skill_gap(
            candidate_skills,
            required_skills,
            job.get("title", "")
        )

        return SkillGapReport(
            candidate_skills=candidate_skills,
            required_skills=required_skills,
            missing_skills=gap_analysis.get("missing_skills", []),
            gap_summary=gap_analysis.get("gap_summary", ""),
            training_recommendations=gap_analysis.get("training_recommendations", [])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/candidates/{candidate_id}")
async def get_candidate_profile(candidate_id: str):
    candidate = await db.get_candidate(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    candidate_copy = candidate.copy()
    candidate_copy.pop("embedding", None)
    return candidate_copy
