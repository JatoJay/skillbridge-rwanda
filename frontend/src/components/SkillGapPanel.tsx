"use client";

import { X, GraduationCap, Clock, AlertTriangle, CheckCircle } from "lucide-react";
import { SkillGapReport } from "@/lib/api";

interface SkillGapPanelProps {
  report: SkillGapReport;
  jobTitle: string;
  onClose: () => void;
  language: string;
}

export default function SkillGapPanel({ report, jobTitle, onClose, language }: SkillGapPanelProps) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden">
        <div className="bg-gradient-to-r from-secondary-500 to-primary-500 px-6 py-4 flex items-center justify-between">
          <div>
            <h2 className="text-white font-semibold text-lg">
              {language === "rw" ? "Igice cy'ubumenyi" : "Skill Gap Analysis"}
            </h2>
            <p className="text-white/80 text-sm">{jobTitle}</p>
          </div>
          <button
            onClick={onClose}
            className="text-white/80 hover:text-white transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6 overflow-y-auto max-h-[calc(90vh-80px)]">
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="bg-green-50 rounded-xl p-4">
              <div className="flex items-center gap-2 text-green-700 mb-2">
                <CheckCircle className="w-5 h-5" />
                <span className="font-medium">
                  {language === "rw" ? "Ubumenyi ufite" : "Your Skills"}
                </span>
              </div>
              <div className="flex flex-wrap gap-1">
                {report.candidate_skills.map((skill) => (
                  <span
                    key={skill}
                    className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            <div className="bg-red-50 rounded-xl p-4">
              <div className="flex items-center gap-2 text-red-700 mb-2">
                <AlertTriangle className="w-5 h-5" />
                <span className="font-medium">
                  {language === "rw" ? "Ibikenewe" : "Skills to Learn"}
                </span>
              </div>
              <div className="flex flex-wrap gap-1">
                {report.missing_skills.map((skill) => (
                  <span
                    key={skill}
                    className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="bg-gray-50 rounded-xl p-4 mb-6">
            <h3 className="font-medium text-gray-900 mb-2">
              {language === "rw" ? "Incamake" : "Summary"}
            </h3>
            <p className="text-gray-700 text-sm">{report.gap_summary}</p>
          </div>

          <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <GraduationCap className="w-5 h-5 text-secondary-500" />
            {language === "rw" ? "Amahugurwa atangwa mu Rwanda" : "Recommended Training in Rwanda"}
          </h3>

          <div className="space-y-4">
            {report.training_recommendations.map((rec, idx) => (
              <div
                key={idx}
                className="border border-gray-200 rounded-xl p-4 hover:border-secondary-300 transition-colors"
              >
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h4 className="font-medium text-gray-900">{rec.program}</h4>
                    <p className="text-sm text-secondary-600">{rec.provider}</p>
                  </div>
                  <span className="bg-secondary-100 text-secondary-700 text-xs px-2 py-1 rounded-full">
                    {rec.skill}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mb-2">{rec.description}</p>
                <div className="flex items-center gap-1 text-sm text-gray-500">
                  <Clock className="w-4 h-4" />
                  {rec.duration}
                </div>
              </div>
            ))}

            {report.training_recommendations.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                <GraduationCap className="w-12 h-12 mx-auto mb-2 opacity-50" />
                <p>
                  {language === "rw"
                    ? "Nta mahugurwa agenwe. Gerageza kongera ubumenyi bwawe."
                    : "No specific training recommendations. Consider expanding your skill set."}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
