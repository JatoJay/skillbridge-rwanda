from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class JobListing(BaseModel):
    id: Optional[str] = None
    title: str
    company: str
    description: str
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    experience_level: str
    sector: str
    location: str
    salary_range: Optional[str] = None
    employment_type: str = "full-time"
    embedding: Optional[list[float]] = None
    employer_id: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class JobCreate(BaseModel):
    title: str
    company: str
    description: str
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    experience_level: str = "mid"
    sector: str
    location: str = "Kigali"
    salary_range: Optional[str] = None
    employment_type: str = "full-time"


class JobMatch(BaseModel):
    job: JobListing
    score: float
    explanation: str
    skill_gaps: list[str] = Field(default_factory=list)


class SkillGapReport(BaseModel):
    candidate_skills: list[str]
    required_skills: list[str]
    missing_skills: list[str]
    gap_summary: str
    training_recommendations: list[dict]


class EmployerJobPost(BaseModel):
    description: str
    company: str
    location: str = "Kigali"
    contact_email: Optional[str] = None


class ExtractedJob(BaseModel):
    title: str
    required_skills: list[str]
    preferred_skills: list[str]
    sector: str
    experience_level: str


class CandidateMatch(BaseModel):
    candidate_id: str
    name: str
    score: float
    matching_skills: list[str]
    explanation: str


class InsightsData(BaseModel):
    top_skills: list[dict]
    sectors_hiring: list[dict]
    skill_gaps_by_region: list[dict]
    total_candidates: int
    total_jobs: int
    matches_made: int
