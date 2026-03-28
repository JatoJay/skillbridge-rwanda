import json
import os
import httpx
from config import get_settings

settings = get_settings()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

SYSTEM_PROMPT_PROFILER = """You are SkillBridge Rwanda's AI career assistant. Your role is to have a friendly conversation with job seekers in Rwanda to understand their professional background, skills, and career goals.

Context about Rwanda's job market:
- Key sectors: AgriTech, Tourism, Construction, ICT, Finance, Healthcare
- Major employers: RwandAir, Bank of Kigali, MTN Rwanda, Zipline, Norrsken Kigali, Andela
- Training providers: TVET colleges, RDB programs, ALX Africa, Andela, University of Rwanda, CMU-Africa

Guidelines:
1. Be warm, encouraging, and conversational
2. Ask about their work experience, education, and skills naturally
3. Understand their preferred sectors and location preferences
4. After gathering enough information (usually 4-5 exchanges), summarize what you've learned
5. Support both English and Kinyarwanda - respond in the language the user uses

When you have gathered sufficient information, end your response with a JSON block containing the extracted profile:
```json
{
  "profile_complete": true,
  "profile": {
    "skills": [{"name": "skill_name", "level": "beginner/intermediate/advanced"}],
    "experience_level": "entry/mid/senior",
    "preferred_sectors": ["sector1", "sector2"],
    "location": "city/region",
    "education": "highest education",
    "languages": ["language1", "language2"],
    "bio": "brief professional summary"
  }
}
```

If more information is needed, respond naturally without the JSON block."""

SYSTEM_PROMPT_JOB_EXTRACTION = """Extract structured information from this job description. Return ONLY valid JSON:
{
  "title": "job title",
  "required_skills": ["skill1", "skill2"],
  "preferred_skills": ["skill3"],
  "sector": "one of: ICT, Finance, Healthcare, Tourism, AgriTech, Construction, Education, Manufacturing, Retail, Logistics",
  "experience_level": "entry/mid/senior"
}"""

SYSTEM_PROMPT_GAP_ANALYSIS = """Analyze skill gaps and recommend Rwandan training programs. Return ONLY valid JSON:
{
  "missing_skills": ["skill1", "skill2"],
  "gap_summary": "explanation of gaps",
  "training_recommendations": [
    {"skill": "skill", "provider": "TVET/RDB/ALX/Andela/University of Rwanda/CMU-Africa", "program": "program name", "duration": "duration", "description": "brief description"}
  ]
}"""


async def call_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        return ""

    url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            url,
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048}
            }
        )
        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        return ""


class GeminiService:
    async def chat_profile(self, messages: list[dict], language: str = "en") -> dict:
        if not GEMINI_API_KEY:
            return {"message": "Please tell me about your skills and experience.", "profile_complete": False, "extracted_profile": None}

        conversation = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])
        lang_note = "Respond in Kinyarwanda." if language == "rw" else ""

        prompt = f"{SYSTEM_PROMPT_PROFILER}\n\n{lang_note}\n\nConversation:\n{conversation}\n\nASSISTANT:"

        response_text = await call_gemini(prompt)

        if not response_text:
            return {"message": "I'd love to learn more about you. What kind of work experience do you have?", "profile_complete": False, "extracted_profile": None}

        profile_complete = False
        extracted_profile = None

        if "```json" in response_text and '"profile_complete": true' in response_text:
            try:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_str = response_text[json_start:json_end].strip()
                data = json.loads(json_str)
                if data.get("profile_complete"):
                    profile_complete = True
                    extracted_profile = data.get("profile")
                    response_text = response_text[:response_text.find("```json")].strip()
            except json.JSONDecodeError:
                pass

        return {
            "message": response_text,
            "profile_complete": profile_complete,
            "extracted_profile": extracted_profile
        }

    async def analyze_skill_gap(self, candidate_skills: list[str], required_skills: list[str], job_title: str) -> dict:
        if not GEMINI_API_KEY:
            missing = list(set(required_skills) - set(candidate_skills))
            return {"missing_skills": missing, "gap_summary": f"You need to develop: {', '.join(missing)}", "training_recommendations": []}

        prompt = f"""{SYSTEM_PROMPT_GAP_ANALYSIS}

Job Title: {job_title}
Candidate Skills: {', '.join(candidate_skills)}
Required Skills: {', '.join(required_skills)}"""

        response = await call_gemini(prompt)

        try:
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                return json.loads(response[json_start:json_end].strip())
            return json.loads(response)
        except:
            missing = list(set(required_skills) - set(candidate_skills))
            return {"missing_skills": missing, "gap_summary": response or f"Skills to develop: {', '.join(missing)}", "training_recommendations": []}

    async def extract_job_info(self, description: str) -> dict:
        if not GEMINI_API_KEY:
            return {"title": "Position", "required_skills": [], "preferred_skills": [], "sector": "General", "experience_level": "mid"}

        prompt = f"{SYSTEM_PROMPT_JOB_EXTRACTION}\n\nJob Description:\n{description}"

        response = await call_gemini(prompt)

        try:
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                return json.loads(response[json_start:json_end].strip())
            return json.loads(response)
        except:
            return {"title": "Position", "required_skills": [], "preferred_skills": [], "sector": "General", "experience_level": "mid"}

    async def generate_match_explanation(self, candidate_bio: str, candidate_skills: list[str], job_title: str, job_description: str, match_score: float) -> str:
        if not GEMINI_API_KEY:
            return f"Strong match based on your skills in {', '.join(candidate_skills[:3])}."

        prompt = f"""Generate a brief (2-3 sentences) explanation of why this candidate is a {match_score:.0%} match.
Candidate: {candidate_bio}
Skills: {', '.join(candidate_skills)}
Job: {job_title}
Description: {job_description[:200]}"""

        response = await call_gemini(prompt)
        return response.strip() if response else f"Good match based on your {', '.join(candidate_skills[:3])} skills."


gemini_service = GeminiService()
