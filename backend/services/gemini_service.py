import json
from typing import Optional
import vertexai
from vertexai.generative_models import GenerativeModel, Part, Content
from config import get_settings

settings = get_settings()

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

SYSTEM_PROMPT_GAP_ANALYSIS = """You are a career advisor for SkillBridge Rwanda. Analyze skill gaps between a candidate and a job requirement, then recommend specific Rwandan training programs.

Available training providers in Rwanda:
- TVET Colleges: Technical and vocational training across Rwanda
- RDB (Rwanda Development Board): Business and entrepreneurship programs
- ALX Africa: Software engineering, data science, and leadership programs
- Andela: Software development training
- University of Rwanda: Degree and certificate programs
- CMU-Africa: Master's programs in IT and engineering
- Digital Opportunity Trust: Digital skills training
- Akilah Institute: Business and hospitality training for women

Provide your response as JSON:
```json
{
  "missing_skills": ["skill1", "skill2"],
  "gap_summary": "Clear explanation of the gaps",
  "training_recommendations": [
    {
      "skill": "skill_name",
      "provider": "provider_name",
      "program": "specific program name",
      "duration": "estimated duration",
      "description": "brief description"
    }
  ]
}
```"""

SYSTEM_PROMPT_JOB_EXTRACTION = """You are a job posting analyzer for SkillBridge Rwanda. Extract structured information from job descriptions.

Sectors to categorize into: AgriTech, Tourism, Construction, ICT, Finance, Healthcare, Education, Manufacturing, Retail, Logistics

Experience levels: entry, mid, senior

Provide your response as JSON:
```json
{
  "title": "extracted or inferred job title",
  "required_skills": ["skill1", "skill2"],
  "preferred_skills": ["skill3", "skill4"],
  "sector": "one of the defined sectors",
  "experience_level": "entry/mid/senior"
}
```"""


class GeminiService:
    def __init__(self):
        vertexai.init(project=settings.project_id, location=settings.location)
        self.model = GenerativeModel(settings.gemini_model)

    async def chat_profile(self, messages: list[dict], language: str = "en") -> dict:
        chat_history = []
        for msg in messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            chat_history.append(Content(role=role, parts=[Part.from_text(msg["content"])]))

        chat = self.model.start_chat(history=chat_history)

        lang_instruction = ""
        if language == "rw":
            lang_instruction = "\n\nRespond in Kinyarwanda."

        response = chat.send_message(
            f"{SYSTEM_PROMPT_PROFILER}{lang_instruction}\n\nUser: {messages[-1]['content']}"
        )

        response_text = response.text
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

    async def analyze_skill_gap(
        self,
        candidate_skills: list[str],
        required_skills: list[str],
        job_title: str
    ) -> dict:
        prompt = f"""{SYSTEM_PROMPT_GAP_ANALYSIS}

Job Title: {job_title}
Candidate Skills: {', '.join(candidate_skills)}
Required Skills: {', '.join(required_skills)}

Analyze the gaps and provide training recommendations."""

        response = self.model.generate_content(prompt)

        try:
            json_start = response.text.find("```json") + 7
            json_end = response.text.find("```", json_start)
            json_str = response.text[json_start:json_end].strip()
            return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            return {
                "missing_skills": list(set(required_skills) - set(candidate_skills)),
                "gap_summary": response.text,
                "training_recommendations": []
            }

    async def extract_job_info(self, description: str) -> dict:
        prompt = f"""{SYSTEM_PROMPT_JOB_EXTRACTION}

Job Description:
{description}

Extract the structured job information."""

        response = self.model.generate_content(prompt)

        try:
            json_start = response.text.find("```json") + 7
            json_end = response.text.find("```", json_start)
            json_str = response.text[json_start:json_end].strip()
            return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            return {
                "title": "Unknown Position",
                "required_skills": [],
                "preferred_skills": [],
                "sector": "ICT",
                "experience_level": "mid"
            }

    async def generate_match_explanation(
        self,
        candidate_bio: str,
        candidate_skills: list[str],
        job_title: str,
        job_description: str,
        match_score: float
    ) -> str:
        prompt = f"""Generate a brief, encouraging explanation (2-3 sentences) of why this candidate is a {match_score:.0%} match for this job.

Candidate Background: {candidate_bio}
Candidate Skills: {', '.join(candidate_skills)}
Job Title: {job_title}
Job Description: {job_description}

Be specific about matching skills and experience. Be encouraging but honest."""

        response = self.model.generate_content(prompt)
        return response.text.strip()


gemini_service = GeminiService()
