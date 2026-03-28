import json
import uuid
from datetime import datetime
from typing import Optional
from pathlib import Path


class InMemoryDatabase:
    def __init__(self):
        self.candidates: dict[str, dict] = {}
        self.jobs: dict[str, dict] = {}
        self.chat_sessions: dict[str, list] = {}
        self.matches: list[dict] = []
        self._load_seed_data()

    def _load_seed_data(self):
        seed_path = Path(__file__).parent.parent.parent / "seed_data" / "jobs.json"
        if seed_path.exists():
            with open(seed_path, "r") as f:
                jobs_data = json.load(f)
                for job in jobs_data:
                    job_id = str(uuid.uuid4())
                    job["id"] = job_id
                    job["created_at"] = datetime.now().isoformat()
                    job["is_active"] = True
                    self.jobs[job_id] = job

    async def create_candidate(self, profile: dict) -> str:
        candidate_id = str(uuid.uuid4())
        profile["id"] = candidate_id
        profile["created_at"] = datetime.now().isoformat()
        profile["updated_at"] = datetime.now().isoformat()
        self.candidates[candidate_id] = profile
        return candidate_id

    async def get_candidate(self, candidate_id: str) -> Optional[dict]:
        return self.candidates.get(candidate_id)

    async def update_candidate(self, candidate_id: str, profile: dict):
        if candidate_id in self.candidates:
            profile["updated_at"] = datetime.now().isoformat()
            self.candidates[candidate_id].update(profile)

    async def get_all_candidates(self) -> list[dict]:
        return list(self.candidates.values())

    async def create_job(self, job: dict) -> str:
        job_id = str(uuid.uuid4())
        job["id"] = job_id
        job["created_at"] = datetime.now().isoformat()
        job["is_active"] = True
        self.jobs[job_id] = job
        return job_id

    async def get_job(self, job_id: str) -> Optional[dict]:
        return self.jobs.get(job_id)

    async def get_all_jobs(self) -> list[dict]:
        return list(self.jobs.values())

    async def get_active_jobs(self) -> list[dict]:
        return [j for j in self.jobs.values() if j.get("is_active", True)]

    async def save_chat_session(self, session_id: str, messages: list):
        self.chat_sessions[session_id] = messages

    async def get_chat_session(self, session_id: str) -> list:
        return self.chat_sessions.get(session_id, [])

    async def record_match(self, candidate_id: str, job_id: str, score: float):
        self.matches.append({
            "candidate_id": candidate_id,
            "job_id": job_id,
            "score": score,
            "created_at": datetime.now().isoformat()
        })

    async def get_insights(self) -> dict:
        skill_counts = {}
        for job in self.jobs.values():
            for skill in job.get("required_skills", []):
                skill_counts[skill] = skill_counts.get(skill, 0) + 1

        sector_counts = {}
        for job in self.jobs.values():
            sector = job.get("sector", "Other")
            sector_counts[sector] = sector_counts.get(sector, 0) + 1

        return {
            "top_skills": sorted(
                [{"name": k, "count": v} for k, v in skill_counts.items()],
                key=lambda x: x["count"],
                reverse=True
            )[:10],
            "sectors_hiring": sorted(
                [{"name": k, "count": v} for k, v in sector_counts.items()],
                key=lambda x: x["count"],
                reverse=True
            ),
            "skill_gaps_by_region": [
                {"region": "Kigali", "gap_score": 35},
                {"region": "Northern Province", "gap_score": 55},
                {"region": "Southern Province", "gap_score": 48},
                {"region": "Eastern Province", "gap_score": 52},
                {"region": "Western Province", "gap_score": 50}
            ],
            "total_candidates": len(self.candidates),
            "total_jobs": len(self.jobs),
            "matches_made": len(self.matches)
        }


db = InMemoryDatabase()
