"use client";

import { useState, useEffect } from "react";
import { Loader2, TrendingUp, Users, Briefcase, Target, MapPin } from "lucide-react";
import { getInsights, InsightsData } from "@/lib/api";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

const COLORS = ["#00A651", "#00A0DC", "#FDD116", "#008C45", "#0084B8", "#E5BC14"];

export default function DashboardPage() {
  const [insights, setInsights] = useState<InsightsData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [language] = useState("en");

  useEffect(() => {
    loadInsights();
  }, []);

  const loadInsights = async () => {
    try {
      const data = await getInsights();
      setInsights(data);
    } catch (error) {
      console.error("Error loading insights:", error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-primary-500 mx-auto mb-4" />
          <p className="text-gray-600">Loading insights...</p>
        </div>
      </div>
    );
  }

  if (!insights) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8 text-center">
        <p className="text-gray-600">Unable to load insights data.</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          {language === "rw" ? "Imibare y'isoko ry'akazi" : "Labor Market Insights"}
        </h1>
        <p className="text-gray-600">
          {language === "rw"
            ? "Reba ibyo isoko ry'akazi ry'u Rwanda rikeneye"
            : "Real-time insights into Rwanda's job market"}
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
              <Users className="w-6 h-6 text-primary-600" />
            </div>
            <div>
              <p className="text-sm text-gray-500">
                {language === "rw" ? "Abashaka akazi" : "Job Seekers"}
              </p>
              <p className="text-2xl font-bold text-gray-900">{insights.total_candidates}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-secondary-100 rounded-xl flex items-center justify-center">
              <Briefcase className="w-6 h-6 text-secondary-600" />
            </div>
            <div>
              <p className="text-sm text-gray-500">
                {language === "rw" ? "Akazi kahari" : "Active Jobs"}
              </p>
              <p className="text-2xl font-bold text-gray-900">{insights.total_jobs}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-accent-500/20 rounded-xl flex items-center justify-center">
              <Target className="w-6 h-6 text-accent-600" />
            </div>
            <div>
              <p className="text-sm text-gray-500">
                {language === "rw" ? "Guhuza kwarakozwe" : "Matches Made"}
              </p>
              <p className="text-2xl font-bold text-gray-900">{insights.matches_made}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-primary-500" />
            {language === "rw" ? "Ubumenyi busabwa cyane" : "Top In-Demand Skills"}
          </h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={insights.top_skills}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 80, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="count" fill="#00A651" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Briefcase className="w-5 h-5 text-secondary-500" />
            {language === "rw" ? "Inganda zitanga akazi" : "Sectors Hiring"}
          </h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={insights.sectors_hiring}
                  dataKey="count"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {insights.sectors_hiring.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <MapPin className="w-5 h-5 text-red-500" />
          {language === "rw" ? "Igice cy'ubumenyi hakurikijwe akarere" : "Skill Gap by Region"}
        </h2>
        <div className="grid md:grid-cols-5 gap-4">
          {insights.skill_gaps_by_region.map((region) => (
            <div key={region.region} className="text-center">
              <div className="relative w-24 h-24 mx-auto mb-2">
                <svg className="w-24 h-24 transform -rotate-90">
                  <circle
                    cx="48"
                    cy="48"
                    r="40"
                    stroke="#e5e7eb"
                    strokeWidth="8"
                    fill="none"
                  />
                  <circle
                    cx="48"
                    cy="48"
                    r="40"
                    stroke={region.gap_score > 50 ? "#ef4444" : region.gap_score > 35 ? "#f59e0b" : "#22c55e"}
                    strokeWidth="8"
                    fill="none"
                    strokeDasharray={`${region.gap_score * 2.51} 251`}
                    strokeLinecap="round"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-xl font-bold text-gray-900">{region.gap_score}%</span>
                </div>
              </div>
              <p className="text-sm font-medium text-gray-700">{region.region}</p>
              <p className="text-xs text-gray-500">
                {region.gap_score > 50
                  ? language === "rw" ? "Ikirenga" : "High Gap"
                  : region.gap_score > 35
                  ? language === "rw" ? "Hagati" : "Medium"
                  : language === "rw" ? "Gito" : "Low Gap"}
              </p>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-8 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-2xl p-8 text-white">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div>
            <h3 className="text-xl font-semibold mb-2">
              {language === "rw" ? "Shakisha amakuru yimbitse" : "Need Deeper Insights?"}
            </h3>
            <p className="text-white/80">
              {language === "rw"
                ? "Vugana natwe kugira ngo ubone raporo yuzuye."
                : "Contact us for custom labor market reports and analytics."}
            </p>
          </div>
          <button className="bg-white text-primary-600 px-6 py-3 rounded-xl font-medium hover:bg-gray-100 transition-colors whitespace-nowrap">
            {language === "rw" ? "Vugana natwe" : "Contact Us"}
          </button>
        </div>
      </div>
    </div>
  );
}
