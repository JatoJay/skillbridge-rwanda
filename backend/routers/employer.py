from fastapi import APIRouter, HTTPException
from models.job import EmployerJobPost, JobCreate, CandidateMatch
from services.gemini_service import gemini_service
from services.embedding_service import embedding_service
from services.vector_search import vector_search_service
from services.database import db

router = APIRouter(prefix="/employer", tags=["employer"])


@router.post("/jobs")
async def create_job_posting(request: EmployerJobPost):
    try:
        extracted = await gemini_service.extract_job_info(request.description)

        job_data = {
            "title": extracted.get("title", "Position"),
            "company": request.company,
            "description": request.description,
            "required_skills": extracted.get("required_skills", []),
            "preferred_skills": extracted.get("preferred_skills", []),
            "experience_level": extracted.get("experience_level", "mid"),
            "sector": extracted.get("sector", "ICT"),
            "location": request.location,
            "employment_type": "full-time",
            "contact_email": request.contact_email
        }

        job_text = embedding_service.create_job_text(job_data)
        embedding = await embedding_service.get_embedding(job_text)
        job_data["embedding"] = embedding

        job_id = await db.create_job(job_data)
        await vector_search_service.index_job(job_id, embedding)

        top_candidates = await vector_search_service.search_candidates_for_job(
            embedding, top_k=3
        )

        matched_candidates = []
        for candidate_id, score in top_candidates:
            candidate = await db.get_candidate(candidate_id)
            if candidate:
                candidate_skills = [
                    s.get("name") if isinstance(s, dict) else s
                    for s in candidate.get("skills", [])
                ]
                required_skills = set(job_data["required_skills"])
                matching = list(set(candidate_skills) & required_skills)

                explanation = await gemini_service.generate_match_explanation(
                    candidate.get("bio", ""),
                    candidate_skills,
                    job_data["title"],
                    job_data["description"],
                    score
                )

                matched_candidates.append({
                    "candidate_id": candidate_id,
                    "name": candidate.get("full_name", "Anonymous"),
                    "score": round(score * 100, 1),
                    "matching_skills": matching,
                    "explanation": explanation
                })

        job_response = job_data.copy()
        job_response["id"] = job_id
        job_response.pop("embedding", None)

        return {
            "job": job_response,
            "extracted_info": extracted,
            "top_candidates": matched_candidates,
            "message": "Job posted successfully!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs")
async def list_employer_jobs(company: str = None):
    jobs = await db.get_all_jobs()

    if company:
        jobs = [j for j in jobs if j.get("company", "").lower() == company.lower()]

    result = []
    for job in jobs:
        job_copy = job.copy()
        job_copy.pop("embedding", None)
        result.append(job_copy)

    return {"jobs": result, "total": len(result)}


@router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    job = await db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job_copy = job.copy()
    job_copy.pop("embedding", None)
    return job_copy


@router.get("/jobs/{job_id}/candidates")
async def get_matching_candidates(job_id: str, top_k: int = 5):
    job = await db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job_embedding = job.get("embedding")
    if not job_embedding:
        job_text = embedding_service.create_job_text(job)
        job_embedding = await embedding_service.get_embedding(job_text)

    top_candidates = await vector_search_service.search_candidates_for_job(
        job_embedding, top_k=top_k
    )

    matched_candidates = []
    for candidate_id, score in top_candidates:
        candidate = await db.get_candidate(candidate_id)
        if candidate:
            candidate_skills = [
                s.get("name") if isinstance(s, dict) else s
                for s in candidate.get("skills", [])
            ]
            required_skills = set(job.get("required_skills", []))
            matching = list(set(candidate_skills) & required_skills)

            matched_candidates.append({
                "candidate_id": candidate_id,
                "name": candidate.get("full_name", "Anonymous"),
                "score": round(score * 100, 1),
                "matching_skills": matching,
                "experience_level": candidate.get("experience_level"),
                "location": candidate.get("location")
            })

    return {"candidates": matched_candidates, "total": len(matched_candidates)}
