"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight, MessageSquare, Target, GraduationCap, Building2 } from "lucide-react";
import ChatProfiler from "@/components/ChatProfiler";
import { CandidateProfile } from "@/lib/api";

export default function HomePage() {
  const [showChat, setShowChat] = useState(false);
  const [language, setLanguage] = useState("en");
  const router = useRouter();

  const handleProfileComplete = (candidateId: string, profile: CandidateProfile) => {
    localStorage.setItem("candidateId", candidateId);
    localStorage.setItem("candidateProfile", JSON.stringify(profile));
    router.push("/matches");
  };

  const features = [
    {
      icon: MessageSquare,
      title: language === "rw" ? "Vuga n'AI" : "Chat-Based Profiling",
      description: language === "rw"
        ? "Tuvugana natwe mu Kinyarwanda cyangwa Icyongereza"
        : "Tell us about yourself in a natural conversation",
    },
    {
      icon: Target,
      title: language === "rw" ? "Kubona akazi" : "AI Job Matching",
      description: language === "rw"
        ? "Tuguhuza n'akazi kakwiye bitewe n'ubumenyi bwawe"
        : "We match you with jobs based on your actual skills",
    },
    {
      icon: GraduationCap,
      title: language === "rw" ? "Amahugurwa" : "Training Paths",
      description: language === "rw"
        ? "Menya amahugurwa yo mu Rwanda akwiye"
        : "Get personalized training recommendations",
    },
  ];

  return (
    <div className="min-h-screen">
      {!showChat ? (
        <>
          <section className="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-500 to-secondary-500 text-white">
            <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAxOGMtOS45NDEgMC0xOCA4LjA1OS0xOCAxOHM4LjA1OSAxOCAxOCAxOCAxOC04LjA1OSAxOC0xOC04LjA1OS0xOC0xOC0xOHptMCAzMmMtNy43MzIgMC0xNC02LjI2OC0xNC0xNHM2LjI2OC0xNCAxNC0xNCAxNCA2LjI2OCAxNCAxNC02LjI2OCAxNC0xNCAxNHoiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iLjA1Ii8+PC9nPjwvc3ZnPg==')] opacity-30" />
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-32 relative">
              <div className="text-center max-w-3xl mx-auto">
                <h1 className="text-4xl md:text-6xl font-bold mb-6">
                  {language === "rw" ? (
                    <>Bona Akazi Kakwiye mu <span className="text-accent-500">Rwanda</span></>
                  ) : (
                    <>Find Your Perfect Job Match in <span className="text-accent-500">Rwanda</span></>
                  )}
                </h1>
                <p className="text-xl md:text-2xl text-white/90 mb-8">
                  {language === "rw"
                    ? "Dukoresha AI kugira ngo tuguhuze n'amahirwe y'akazi akwiye ubumenyi bwawe."
                    : "AI-powered job matching that understands your skills and connects you with the right opportunities."}
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <button
                    onClick={() => setShowChat(true)}
                    className="bg-white text-primary-600 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-gray-100 transition-colors flex items-center justify-center gap-2"
                  >
                    {language === "rw" ? "Tangira Nonaha" : "Get Started"}
                    <ArrowRight className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => router.push("/employer")}
                    className="border-2 border-white/30 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-white/10 transition-colors flex items-center justify-center gap-2"
                  >
                    <Building2 className="w-5 h-5" />
                    {language === "rw" ? "Ndi Umukoresha" : "I'm an Employer"}
                  </button>
                </div>
                <p className="mt-6 text-white/70 text-sm">
                  {language === "rw"
                    ? "Nta CV isabwa • Vuga mu Kinyarwanda cyangwa Icyongereza"
                    : "No CV required • Chat in English or Kinyarwanda"}
                </p>
              </div>
            </div>
            <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-gray-50 to-transparent" />
          </section>

          <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
            <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
              {language === "rw" ? "Uko bikora" : "How It Works"}
            </h2>
            <div className="grid md:grid-cols-3 gap-8">
              {features.map((feature, idx) => {
                const Icon = feature.icon;
                return (
                  <div
                    key={idx}
                    className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100 hover:shadow-xl transition-shadow"
                  >
                    <div className="w-14 h-14 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center mb-6">
                      <Icon className="w-7 h-7 text-white" />
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
                    <p className="text-gray-600">{feature.description}</p>
                  </div>
                );
              })}
            </div>
          </section>

          <section className="bg-gradient-to-r from-secondary-500 to-primary-500 text-white py-16">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
              <h2 className="text-3xl font-bold mb-6">
                {language === "rw" ? "Witegure gutangira?" : "Ready to Find Your Match?"}
              </h2>
              <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
                {language === "rw"
                  ? "Tangira kuvugana na AI yacu kugira ngo ubaze umwirondoro wawe muminota mike."
                  : "Start chatting with our AI to build your profile in just a few minutes."}
              </p>
              <button
                onClick={() => setShowChat(true)}
                className="bg-white text-primary-600 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-gray-100 transition-colors"
              >
                {language === "rw" ? "Tangira Kuvugana" : "Start Chatting Now"}
              </button>
            </div>
          </section>
        </>
      ) : (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <button
            onClick={() => setShowChat(false)}
            className="text-gray-600 hover:text-gray-900 mb-6 flex items-center gap-2"
          >
            ← {language === "rw" ? "Subira inyuma" : "Back to Home"}
          </button>
          <ChatProfiler language={language} onProfileComplete={handleProfileComplete} />
        </section>
      )}
    </div>
  );
}
