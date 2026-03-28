"use client";

import { useState, useEffect } from "react";
import { Building2, Briefcase, Users, Loader2 } from "lucide-react";
import EmployerForm from "@/components/EmployerForm";
import { getJobs, JobListing } from "@/lib/api";

export default function EmployerPage() {
  const [activeTab, setActiveTab] = useState<"post" | "browse">("post");
  const [jobs, setJobs] = useState<JobListing[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [language] = useState("en");

  useEffect(() => {
    if (activeTab === "browse") {
      loadJobs();
    }
  }, [activeTab]);

  const loadJobs = async () => {
    setIsLoading(true);
    try {
      const result = await getJobs();
      setJobs(result.jobs);
    } catch (error) {
      console.error("Error loading jobs:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-gradient-to-br from-secondary-500 to-primary-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <Building2 className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          {language === "rw" ? "Portal y'Abakoresha" : "Employer Portal"}
        </h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          {language === "rw"
            ? "Shyiraho akazi kandi AI izakubonere abakandida bakwiye."
            : "Post jobs and let our AI find you the best candidates instantly."}
        </p>
      </div>

      <div className="flex justify-center mb-8">
        <div className="bg-white rounded-xl p-1 shadow-md border border-gray-100 inline-flex">
          <button
            onClick={() => setActiveTab("post")}
            className={`px-6 py-3 rounded-lg font-medium text-sm transition-colors flex items-center gap-2 ${
              activeTab === "post"
                ? "bg-primary-500 text-white"
                : "text-gray-600 hover:bg-gray-100"
            }`}
          >
            <Briefcase className="w-4 h-4" />
            {language === "rw" ? "Shyiraho Akazi" : "Post a Job"}
          </button>
          <button
            onClick={() => setActiveTab("browse")}
            className={`px-6 py-3 rounded-lg font-medium text-sm transition-colors flex items-center gap-2 ${
              activeTab === "browse"
                ? "bg-primary-500 text-white"
                : "text-gray-600 hover:bg-gray-100"
            }`}
          >
            <Users className="w-4 h-4" />
            {language === "rw" ? "Reba Akazi" : "Browse Jobs"}
          </button>
        </div>
      </div>

      {activeTab === "post" ? (
        <EmployerForm language={language} />
      ) : (
        <div>
          {isLoading ? (
            <div className="text-center py-16">
              <Loader2 className="w-8 h-8 animate-spin text-primary-500 mx-auto mb-4" />
              <p className="text-gray-600">Loading jobs...</p>
            </div>
          ) : jobs.length === 0 ? (
            <div className="text-center py-16 bg-white rounded-xl shadow-md">
              <Briefcase className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {language === "rw" ? "Nta kazi kabonetse" : "No Jobs Posted Yet"}
              </h3>
              <p className="text-gray-600">
                {language === "rw"
                  ? "Tangira gushyiraho akazi kugira ngo ubone abakandida."
                  : "Start by posting a job to find candidates."}
              </p>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {jobs.map((job) => (
                <div
                  key={job.id}
                  className="bg-white rounded-xl shadow-md border border-gray-100 p-6 hover:shadow-lg transition-shadow"
                >
                  <h3 className="text-lg font-semibold text-gray-900 mb-1">{job.title}</h3>
                  <p className="text-secondary-600 text-sm mb-3">{job.company}</p>
                  <div className="flex flex-wrap gap-2 mb-4">
                    <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                      {job.location}
                    </span>
                    <span className="text-xs bg-secondary-100 text-secondary-700 px-2 py-1 rounded">
                      {job.sector}
                    </span>
                    <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                      {job.experience_level}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 line-clamp-3 mb-4">{job.description}</p>
                  <div className="flex flex-wrap gap-1">
                    {job.required_skills.slice(0, 4).map((skill) => (
                      <span
                        key={skill}
                        className="text-xs bg-primary-100 text-primary-700 px-2 py-1 rounded"
                      >
                        {skill}
                      </span>
                    ))}
                    {job.required_skills.length > 4 && (
                      <span className="text-xs text-gray-500">
                        +{job.required_skills.length - 4}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      <div className="mt-12 bg-gradient-to-r from-secondary-50 to-primary-50 rounded-2xl p-8 text-center">
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          {language === "rw" ? "Ishyura na Mobile Money" : "Pay with Mobile Money"}
        </h3>
        <p className="text-gray-600 mb-4">
          {language === "rw"
            ? "Vuba tuzashyira uburyo bwo kwishyura na MTN Mobile Money."
            : "MTN Mobile Money integration coming soon for premium job postings."}
        </p>
        <div className="inline-flex items-center gap-2 bg-white px-4 py-2 rounded-lg border border-gray-200">
          <span className="text-yellow-500 font-bold">MTN</span>
          <span className="text-gray-500">Mobile Money</span>
          <span className="text-xs bg-yellow-100 text-yellow-700 px-2 py-1 rounded">Coming Soon</span>
        </div>
      </div>
    </div>
  );
}
