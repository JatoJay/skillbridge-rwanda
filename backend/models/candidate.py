from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Skill(BaseModel):
    name: str
    level: Optional[str] = None


class CandidateProfile(BaseModel):
    id: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: list[Skill] = Field(default_factory=list)
    experience_level: Optional[str] = None
    preferred_sectors: list[str] = Field(default_factory=list)
    location: Optional[str] = None
    bio: Optional[str] = None
    languages: list[str] = Field(default_factory=list)
    education: Optional[str] = None
    embedding: Optional[list[float]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CandidateCreate(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: list[Skill] = Field(default_factory=list)
    experience_level: Optional[str] = None
    preferred_sectors: list[str] = Field(default_factory=list)
    location: Optional[str] = None
    bio: Optional[str] = None
    languages: list[str] = Field(default_factory=list)
    education: Optional[str] = None


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    session_id: Optional[str] = None
    language: str = "en"


class ChatResponse(BaseModel):
    message: str
    session_id: str
    profile_complete: bool = False
    extracted_profile: Optional[CandidateProfile] = None


class ProfileFinalizeRequest(BaseModel):
    session_id: str
    candidate_id: Optional[str] = None
