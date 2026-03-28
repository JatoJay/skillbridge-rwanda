import numpy as np
from typing import Optional
from config import get_settings

settings = get_settings()


class VectorSearchService:
    def __init__(self):
        self.candidates_vectors: dict[str, list[float]] = {}
        self.jobs_vectors: dict[str, list[float]] = {}

    def cosine_similarity(self, a: list[float], b: list[float]) -> float:
        a_np = np.array(a)
        b_np = np.array(b)
        return float(np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np)))

    async def index_candidate(self, candidate_id: str, embedding: list[float]):
        self.candidates_vectors[candidate_id] = embedding

    async def index_job(self, job_id: str, embedding: list[float]):
        self.jobs_vectors[job_id] = embedding

    async def search_jobs_for_candidate(
        self,
        candidate_embedding: list[float],
        top_k: int = 5
    ) -> list[tuple[str, float]]:
        if not self.jobs_vectors:
            return []

        scores = []
        for job_id, job_embedding in self.jobs_vectors.items():
            score = self.cosine_similarity(candidate_embedding, job_embedding)
            scores.append((job_id, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    async def search_candidates_for_job(
        self,
        job_embedding: list[float],
        top_k: int = 3
    ) -> list[tuple[str, float]]:
        if not self.candidates_vectors:
            return []

        scores = []
        for candidate_id, candidate_embedding in self.candidates_vectors.items():
            score = self.cosine_similarity(job_embedding, candidate_embedding)
            scores.append((candidate_id, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    async def delete_candidate(self, candidate_id: str):
        if candidate_id in self.candidates_vectors:
            del self.candidates_vectors[candidate_id]

    async def delete_job(self, job_id: str):
        if job_id in self.jobs_vectors:
            del self.jobs_vectors[job_id]


vector_search_service = VectorSearchService()
