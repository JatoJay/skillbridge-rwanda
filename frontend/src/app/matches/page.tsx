"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Loader2, Briefcase, RefreshCw, User } from "lucide-react";
import JobMatchCard from "@/components/JobMatchCard";
import SkillGapPanel from "@/components/SkillGapPanel";
import { getJobMatches, getSkillGap, JobMatch, SkillGapReport, CandidateProfile } from "@/lib/api";

export default function MatchesPage() {
  const [matches, setMatches] = useState<JobMatch[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [candidateId, setCandidateId] = useState<string | null>(null);
  const [profile, setProfile] = useState<CandidateProfile | null>(null);
  const [selectedJobId, setSelectedJobId] = useState<string | null>(null);
  const [gapReport, setGapReport] = useState<SkillGapReport | null>(null);
  const [isLoadingGap, setIsLoadingGap] = useState(false);
  const [language] = useState("en");
  const router = useRouter();

  useEffect(() => {
    const storedId = localStorage.getItem("candidateId");
    const storedProfile = localStorage.getItem("candidateProfile");

    if (!storedId) {
      router.push("/");
      return;
    }

    setCandidateId(storedId);
    if (storedProfile) {
      setProfile(JSON.parse(storedProfile));
    }

    loadMatches(storedId);
  }, [router]);

  const loadMatches = async (id: string) => {
    setIsLoading(true);
    try {
      const result = await getJobMatches(id);
      setMatches(result.matches);
    } catch (error) {
      console.error("Error loading matches:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleViewGap = async (jobId: string) => {
    if (!candidateId) return;
    setSelectedJobId(jobId);
    setIsLoadingGap(true);

    try {
      const report = await getSkillGap(candidateId, jobId);
      setGapReport(report);
    } catch (error) {
      console.error("Error loading gap analysis:", error);
    } finally {
      setIsLoadingGap(false);
    }
  };

  const selectedJob = matches.find((m) => m.job.id === selectedJobId);

  if (isLoading) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-primary-500 mx-auto mb-4" />
          <p className="text-gray-600">
            {language === "rw" ? "Turimo gushaka akazi kakwiye..." : "Finding your best job matches..."}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {profile && (
        <div className="bg-white rounded-xl shadow-md border border-gray-100 p-6 mb-8">
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-4">
              <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center">
                <User className="w-8 h-8 text-white" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-gray-900">
                  {profile.full_name || (language === "rw" ? "Umwirondoro wawe" : "Your Profile")}
                </h2>
                <p className="text-gray-600 text-sm mb-2">{profile.bio}</p>
                <div className="flex flex-wrap gap-2">
                  {profile.skills?.slice(0, 5).map((skill) => (
                    <span
                      key={typeof skill === "string" ? skill : skill.name}
                      className="text-xs bg-primary-100 text-primary-700 px-2 py-1 rounded"
                    >
                      {typeof skill === "string" ? skill : skill.name}
                    </span>
                  ))}
                  {profile.skills?.length > 5 && (
                    <span className="text-xs text-gray-500">+{profile.skills.length - 5} more</span>
                  )}
                </div>
              </div>
            </div>
            <button
              onClick={() => candidateId && loadMatches(candidateId)}
              className="text-gray-500 hover:text-gray-700 p-2"
              title="Refresh matches"
            >
              <RefreshCw className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}

      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <Briefcase className="w-6 h-6 text-primary-500" />
          {language === "rw" ? "Akazi kakwiye" : "Your Job Matches"}
        </h1>
        <span className="text-gray-500 text-sm">
          {matches.length} {language === "rw" ? "akazi yabonetse" : "jobs found"}
        </span>
      </div>

      {matches.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-xl shadow-md">
          <Briefcase className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            {language === "rw" ? "Nta kazi kabonetse" : "No Matches Found"}
          </h3>
          <p className="text-gray-600 mb-6">
            {language === "rw"
              ? "Ntabwo tubonye akazi gahura n'umwirondoro wawe."
              : "We couldn't find jobs matching your profile yet."}
          </p>
          <button
            onClick={() => router.push("/")}
            className="bg-primary-500 text-white px-6 py-3 rounded-xl hover:bg-primary-600 transition-colors"
          >
            {language === "rw" ? "Vugurura umwirondoro" : "Update Your Profile"}
          </button>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {matches.map((match) => (
            <JobMatchCard
              key={match.job.id}
              match={match}
              onViewGap={handleViewGap}
              language={language}
            />
          ))}
        </div>
      )}

      {selectedJobId && gapReport && selectedJob && !isLoadingGap && (
        <SkillGapPanel
          report={gapReport}
          jobTitle={selectedJob.job.title}
          onClose={() => {
            setSelectedJobId(null);
            setGapReport(null);
          }}
          language={language}
        />
      )}

      {isLoadingGap && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-8">
            <Loader2 className="w-8 h-8 animate-spin text-primary-500 mx-auto mb-4" />
            <p className="text-gray-600">
              {language === "rw" ? "Turimo gusesengura..." : "Analyzing skill gaps..."}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
