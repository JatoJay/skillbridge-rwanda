from vertexai.language_models import TextEmbeddingModel
import vertexai
from config import get_settings

settings = get_settings()


class EmbeddingService:
    def __init__(self):
        vertexai.init(project=settings.project_id, location=settings.location)
        self.model = TextEmbeddingModel.from_pretrained(settings.embedding_model)

    async def get_embedding(self, text: str) -> list[float]:
        embeddings = self.model.get_embeddings([text])
        return embeddings[0].values

    async def get_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.get_embeddings(texts)
        return [e.values for e in embeddings]

    def create_candidate_text(self, profile: dict) -> str:
        skills = ", ".join([s.get("name", s) if isinstance(s, dict) else s for s in profile.get("skills", [])])
        sectors = ", ".join(profile.get("preferred_sectors", []))

        return f"""
        Professional Profile:
        Skills: {skills}
        Experience Level: {profile.get("experience_level", "Not specified")}
        Preferred Sectors: {sectors}
        Location: {profile.get("location", "Not specified")}
        Education: {profile.get("education", "Not specified")}
        Bio: {profile.get("bio", "")}
        """.strip()

    def create_job_text(self, job: dict) -> str:
        required = ", ".join(job.get("required_skills", []))
        preferred = ", ".join(job.get("preferred_skills", []))

        return f"""
        Job: {job.get("title", "")} at {job.get("company", "")}
        Sector: {job.get("sector", "")}
        Location: {job.get("location", "")}
        Experience Level: {job.get("experience_level", "")}
        Required Skills: {required}
        Preferred Skills: {preferred}
        Description: {job.get("description", "")}
        """.strip()


embedding_service = EmbeddingService()
