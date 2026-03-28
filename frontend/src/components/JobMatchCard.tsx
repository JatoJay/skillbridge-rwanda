"use client";

import { Building2, MapPin, Briefcase, ChevronRight, TrendingUp } from "lucide-react";
import { JobMatch } from "@/lib/api";

interface JobMatchCardProps {
  match: JobMatch;
  onViewGap: (jobId: string) => void;
  language: string;
}

export default function JobMatchCard({ match, onViewGap, language }: JobMatchCardProps) {
  const { job, score, explanation, skill_gaps } = match;

  const getScoreColor = (score: number) => {
    if (score >= 80) return "bg-green-500";
    if (score >= 60) return "bg-yellow-500";
    return "bg-orange-500";
  };

  return (
    <div className="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden hover:shadow-lg transition-shadow">
      <div className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900">{job.title}</h3>
            <div className="flex items-center gap-2 text-gray-600 mt-1">
              <Building2 className="w-4 h-4" />
              <span className="text-sm">{job.company}</span>
            </div>
          </div>
          <div className="flex flex-col items-end">
            <div className="flex items-center gap-2">
              <span className="text-2xl font-bold text-primary-600">{score}%</span>
              <TrendingUp className="w-5 h-5 text-primary-500" />
            </div>
            <span className="text-xs text-gray-500">
              {language === "rw" ? "Guhura" : "Match"}
            </span>
          </div>
        </div>

        <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
          <div
            className={`h-2 rounded-full ${getScoreColor(score)} transition-all duration-500`}
            style={{ width: `${score}%` }}
          />
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          <div className="flex items-center gap-1 text-sm text-gray-600 bg-gray-100 px-3 py-1 rounded-full">
            <MapPin className="w-3 h-3" />
            {job.location}
          </div>
          <div className="flex items-center gap-1 text-sm text-gray-600 bg-gray-100 px-3 py-1 rounded-full">
            <Briefcase className="w-3 h-3" />
            {job.experience_level}
          </div>
          <div className="text-sm text-secondary-600 bg-secondary-50 px-3 py-1 rounded-full">
            {job.sector}
          </div>
        </div>

        <p className="text-sm text-gray-700 mb-4 line-clamp-2">{explanation}</p>

        {job.salary_range && (
          <p className="text-sm font-medium text-primary-600 mb-4">{job.salary_range}</p>
        )}

        <div className="mb-4">
          <p className="text-xs text-gray-500 mb-2">
            {language === "rw" ? "Ubumenyi busabwa:" : "Required Skills:"}
          </p>
          <div className="flex flex-wrap gap-1">
            {job.required_skills.slice(0, 5).map((skill) => (
              <span
                key={skill}
                className={`text-xs px-2 py-1 rounded ${
                  skill_gaps.includes(skill)
                    ? "bg-red-100 text-red-700"
                    : "bg-green-100 text-green-700"
                }`}
              >
                {skill}
              </span>
            ))}
          </div>
        </div>

        {skill_gaps.length > 0 && (
          <button
            onClick={() => onViewGap(job.id)}
            className="w-full flex items-center justify-center gap-2 text-secondary-600 hover:text-secondary-700 text-sm font-medium py-2 border border-secondary-200 rounded-lg hover:bg-secondary-50 transition-colors"
          >
            {language === "rw" ? "Reba uburyo bwo kwiga" : "View Training Recommendations"}
            <ChevronRight className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  );
}
