"use client";

import { useState } from "react";
import { Loader2, Send, Building2, MapPin, Mail, CheckCircle, User, TrendingUp } from "lucide-react";
import { postJob } from "@/lib/api";

interface CandidateMatch {
  candidate_id: string;
  name: string;
  score: number;
  matching_skills: string[];
  explanation: string;
}

interface EmployerFormProps {
  language: string;
}

export default function EmployerForm({ language }: EmployerFormProps) {
  const [company, setCompany] = useState("");
  const [location, setLocation] = useState("Kigali");
  const [email, setEmail] = useState("");
  const [description, setDescription] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [matches, setMatches] = useState<CandidateMatch[]>([]);
  const [extractedInfo, setExtractedInfo] = useState<Record<string, unknown> | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!company || !description) return;

    setIsLoading(true);
    setSuccess(false);

    try {
      const result = await postJob({
        company,
        location,
        description,
        contact_email: email || undefined,
      });

      setSuccess(true);
      setMatches(result.top_candidates);
      setExtractedInfo(result.extracted_info);
    } catch (error) {
      console.error("Post job error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setCompany("");
    setDescription("");
    setEmail("");
    setSuccess(false);
    setMatches([]);
    setExtractedInfo(null);
  };

  if (success) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-green-50 border border-green-200 rounded-xl p-6 mb-6">
          <div className="flex items-center gap-2 text-green-700 mb-2">
            <CheckCircle className="w-6 h-6" />
            <h3 className="font-semibold text-lg">
              {language === "rw" ? "Akazi kashyizweho!" : "Job Posted Successfully!"}
            </h3>
          </div>
          {extractedInfo && (
            <div className="mt-4">
              <p className="text-sm text-gray-600 mb-2">
                {language === "rw" ? "AI yavuze:" : "AI Extracted:"}
              </p>
              <div className="flex flex-wrap gap-2">
                <span className="bg-white px-3 py-1 rounded-full text-sm border">
                  {String(extractedInfo.title || "Position")}
                </span>
                <span className="bg-secondary-100 text-secondary-700 px-3 py-1 rounded-full text-sm">
                  {String(extractedInfo.sector || "General")}
                </span>
                <span className="bg-gray-100 px-3 py-1 rounded-full text-sm">
                  {String(extractedInfo.experience_level || "mid")} level
                </span>
              </div>
              {Array.isArray(extractedInfo.required_skills) && extractedInfo.required_skills.length > 0 && (
                <div className="mt-3">
                  <p className="text-xs text-gray-500 mb-1">Skills extracted:</p>
                  <div className="flex flex-wrap gap-1">
                    {extractedInfo.required_skills.map((skill: string) => (
                      <span key={skill} className="text-xs bg-primary-100 text-primary-700 px-2 py-1 rounded">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {matches.length > 0 && (
          <div className="mb-6">
            <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <User className="w-5 h-5 text-primary-500" />
              {language === "rw" ? "Abakandida bakwiye" : "Top Matching Candidates"}
            </h3>
            <div className="space-y-4">
              {matches.map((candidate) => (
                <div
                  key={candidate.candidate_id}
                  className="bg-white border border-gray-200 rounded-xl p-4 hover:border-primary-300 transition-colors"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h4 className="font-medium text-gray-900">{candidate.name}</h4>
                      <p className="text-sm text-gray-600">{candidate.explanation}</p>
                    </div>
                    <div className="flex items-center gap-1 bg-primary-50 text-primary-700 px-3 py-1 rounded-full">
                      <TrendingUp className="w-4 h-4" />
                      <span className="font-semibold">{candidate.score}%</span>
                    </div>
                  </div>
                  {candidate.matching_skills.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-2">
                      {candidate.matching_skills.map((skill) => (
                        <span key={skill} className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
                          {skill}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {matches.length === 0 && (
          <div className="bg-gray-50 rounded-xl p-6 text-center mb-6">
            <User className="w-12 h-12 text-gray-400 mx-auto mb-2" />
            <p className="text-gray-600">
              {language === "rw"
                ? "Nta bakandida babonetse. Abashaka akazi baziyandikisha vuba."
                : "No matching candidates yet. Job seekers will register soon."}
            </p>
          </div>
        )}

        <button
          onClick={resetForm}
          className="w-full bg-gray-100 text-gray-700 py-3 rounded-xl font-medium hover:bg-gray-200 transition-colors"
        >
          {language === "rw" ? "Shyiraho akandi kazi" : "Post Another Job"}
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl mx-auto space-y-6">
      <div className="bg-white rounded-xl shadow-md border border-gray-100 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">
          {language === "rw" ? "Shyiraho akazi" : "Post a Job"}
        </h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              <Building2 className="w-4 h-4 inline mr-1" />
              {language === "rw" ? "Izina ry'ikigo" : "Company Name"}
            </label>
            <input
              type="text"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              placeholder={language === "rw" ? "urugero: MTN Rwanda" : "e.g., MTN Rwanda"}
              className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              <MapPin className="w-4 h-4 inline mr-1" />
              {language === "rw" ? "Aho akazi kaherereye" : "Location"}
            </label>
            <select
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="Kigali">Kigali</option>
              <option value="Musanze">Musanze</option>
              <option value="Huye">Huye</option>
              <option value="Rubavu">Rubavu</option>
              <option value="Rwamagana">Rwamagana</option>
              <option value="Muhanga">Muhanga</option>
              <option value="Nyagatare">Nyagatare</option>
              <option value="Remote">Remote</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              <Mail className="w-4 h-4 inline mr-1" />
              {language === "rw" ? "Email y'umukoresha" : "Contact Email"} (optional)
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="hr@company.rw"
              className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {language === "rw" ? "Ibisobanuro by'akazi" : "Job Description"}
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder={
                language === "rw"
                  ? "Sobanura akazi, ubumenyi bukenewe, n'ibindi..."
                  : "Describe the role, required skills, responsibilities..."
              }
              rows={6}
              className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              {language === "rw"
                ? "AI izavana ubumenyi busabwa mu bisobanuro byawe"
                : "Our AI will extract required skills from your description"}
            </p>
          </div>
        </div>
      </div>

      <button
        type="submit"
        disabled={isLoading || !company || !description}
        className="w-full bg-primary-500 text-white py-4 rounded-xl font-medium hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
      >
        {isLoading ? (
          <Loader2 className="w-5 h-5 animate-spin" />
        ) : (
          <>
            <Send className="w-5 h-5" />
            {language === "rw" ? "Ohereza akazi" : "Post Job & Find Candidates"}
          </>
        )}
      </button>
    </form>
  );
}
