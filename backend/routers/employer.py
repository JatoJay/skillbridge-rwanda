import re
from fastapi import APIRouter, HTTPException
from models.job import EmployerJobPost, JobCreate, CandidateMatch
from services.vector_search import vector_search_service
from services.database import db

router = APIRouter(prefix="/employer", tags=["employer"])


def extract_skills_simple(description: str) -> list[str]:
    common_skills = [
        "Python", "JavaScript", "React", "Node.js", "SQL", "AWS", "Docker", "Kubernetes",
        "Java", "TypeScript", "PostgreSQL", "MongoDB", "Git", "Linux", "Excel", "Tableau",
        "Machine Learning", "Data Analysis", "Project Management", "Leadership", "Communication",
        "Marketing", "SEO", "Sales", "Customer Service", "Accounting", "Finance", "HR",
        "AutoCAD", "Figma", "Photoshop", "English", "French", "Kinyarwanda"
    ]
    found = []
    desc_lower = description.lower()
    for skill in common_skills:
        if skill.lower() in desc_lower:
            found.append(skill)
    return found[:8] if found else ["Communication", "Problem Solving"]


def extract_sector(description: str) -> str:
    desc_lower = description.lower()
    sectors = {
        "ICT": ["software", "developer", "engineer", "tech", "IT", "data", "web", "mobile", "cloud"],
        "Finance": ["bank", "financial", "accounting", "finance", "loan", "investment"],
        "Healthcare": ["health", "medical", "hospital", "nurse", "doctor", "clinical"],
        "Tourism": ["hotel", "tourism", "travel", "hospitality", "guide"],
        "AgriTech": ["agriculture", "farm", "crop", "agri"],
        "Construction": ["construction", "building", "architect", "civil"],
        "Education": ["teacher", "school", "education", "training"],
        "Manufacturing": ["manufacturing", "production", "factory"]
    }
    for sector, keywords in sectors.items():
        if any(kw in desc_lower for kw in keywords):
            return sector
    return "General"


def extract_title(description: str) -> str:
    lines = description.strip().split('\n')
    first_line = lines[0] if lines else description[:50]
    if len(first_line) < 60:
        return first_line.strip()
    words = description.split()[:6]
    return " ".join(words) + "..."


@router.post("/jobs")
async def create_job_posting(request: EmployerJobPost):
    try:
        skills = extract_skills_simple(request.description)
        sector = extract_sector(request.description)
        title = extract_title(request.description)

        extracted = {
            "title": title,
            "required_skills": skills,
            "preferred_skills": [],
            "sector": sector,
            "experience_level": "mid"
        }

        job_data = {
            "title": title,
            "company": request.company,
            "description": request.description,
            "required_skills": skills,
            "preferred_skills": [],
            "experience_level": "mid",
            "sector": sector,
            "location": request.location,
            "employment_type": "full-time",
            "contact_email": request.contact_email
        }

        job_id = await db.create_job(job_data)

        top_candidates = await vector_search_service.search_candidates_for_job(
            [], top_k=3
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

                matched_candidates.append({
                    "candidate_id": candidate_id,
                    "name": candidate.get("full_name", "Anonymous"),
                    "score": round(score * 100, 1),
                    "matching_skills": matching,
                    "explanation": f"Candidate has relevant experience for this {sector} role."
                })

        job_response = job_data.copy()
        job_response["id"] = job_id

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
