const API_URL = 'https://skillbridge-backend-25390365712.us-central1.run.app';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface Skill {
  name: string;
  level?: string;
}

export interface CandidateProfile {
  id?: string;
  full_name?: string;
  email?: string;
  phone?: string;
  skills: Skill[];
  experience_level?: string;
  preferred_sectors: string[];
  location?: string;
  bio?: string;
  languages: string[];
  education?: string;
}

export interface JobListing {
  id: string;
  title: string;
  company: string;
  description: string;
  required_skills: string[];
  preferred_skills: string[];
  experience_level: string;
  sector: string;
  location: string;
  salary_range?: string;
  employment_type: string;
}

export interface JobMatch {
  job: JobListing;
  score: number;
  explanation: string;
  skill_gaps: string[];
}

export interface SkillGapReport {
  candidate_skills: string[];
  required_skills: string[];
  missing_skills: string[];
  gap_summary: string;
  training_recommendations: TrainingRecommendation[];
}

export interface TrainingRecommendation {
  skill: string;
  provider: string;
  program: string;
  duration: string;
  description: string;
}

export interface InsightsData {
  top_skills: { name: string; count: number }[];
  sectors_hiring: { name: string; count: number }[];
  skill_gaps_by_region: { region: string; gap_score: number }[];
  total_candidates: number;
  total_jobs: number;
  matches_made: number;
}

export async function sendChatMessage(
  messages: ChatMessage[],
  sessionId?: string,
  language: string = 'en'
): Promise<{
  message: string;
  session_id: string;
  profile_complete: boolean;
  extracted_profile?: CandidateProfile;
}> {
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      messages,
      session_id: sessionId,
      language,
    }),
  });

  if (!response.ok) {
    throw new Error('Chat request failed');
  }

  return response.json();
}

export async function finalizeProfile(sessionId: string): Promise<{
  candidate_id: string;
  profile: CandidateProfile;
  message: string;
}> {
  const response = await fetch(`${API_URL}/chat/finalize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId }),
  });

  if (!response.ok) {
    throw new Error('Finalize request failed');
  }

  return response.json();
}

export async function getJobMatches(
  candidateId: string,
  topK: number = 5
): Promise<{ matches: JobMatch[]; total: number }> {
  const response = await fetch(`${API_URL}/match/${candidateId}?top_k=${topK}`, {
    method: 'POST',
  });

  if (!response.ok) {
    throw new Error('Match request failed');
  }

  return response.json();
}

export async function getSkillGap(
  candidateId: string,
  jobId: string
): Promise<SkillGapReport> {
  const response = await fetch(`${API_URL}/match/gap/${candidateId}/${jobId}`, {
    method: 'POST',
  });

  if (!response.ok) {
    throw new Error('Skill gap request failed');
  }

  return response.json();
}

export async function postJob(data: {
  description: string;
  company: string;
  location: string;
  contact_email?: string;
}): Promise<{
  job: JobListing;
  extracted_info: Record<string, unknown>;
  top_candidates: Array<{
    candidate_id: string;
    name: string;
    score: number;
    matching_skills: string[];
    explanation: string;
  }>;
  message: string;
}> {
  const response = await fetch(`${API_URL}/employer/jobs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Job post request failed');
  }

  return response.json();
}

export async function getInsights(): Promise<InsightsData> {
  const response = await fetch(`${API_URL}/insights`);

  if (!response.ok) {
    throw new Error('Insights request failed');
  }

  return response.json();
}

export async function getJobs(): Promise<{ jobs: JobListing[]; total: number }> {
  const response = await fetch(`${API_URL}/employer/jobs`);

  if (!response.ok) {
    throw new Error('Jobs request failed');
  }

  return response.json();
}
