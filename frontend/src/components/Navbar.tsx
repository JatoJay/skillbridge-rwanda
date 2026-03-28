"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Briefcase, BarChart3, Building2, Home, Globe } from "lucide-react";

interface NavbarProps {
  language: string;
  onLanguageChange: (lang: string) => void;
}

export default function Navbar({ language, onLanguageChange }: NavbarProps) {
  const pathname = usePathname();

  const links = [
    { href: "/", label: language === "rw" ? "Ahabanza" : "Home", icon: Home },
    { href: "/matches", label: language === "rw" ? "Akazi" : "Jobs", icon: Briefcase },
    { href: "/employer", label: language === "rw" ? "Abakoresha" : "Employers", icon: Building2 },
    { href: "/dashboard", label: language === "rw" ? "Imibare" : "Insights", icon: BarChart3 },
  ];

  return (
    <nav className="bg-white border-b border-gray-100 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">SB</span>
            </div>
            <span className="font-bold text-xl text-gray-900">
              SkillBridge<span className="text-primary-500">Rwanda</span>
            </span>
          </Link>

          <div className="hidden md:flex items-center gap-1">
            {links.map((link) => {
              const Icon = link.icon;
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-primary-50 text-primary-600"
                      : "text-gray-600 hover:bg-gray-100"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {link.label}
                </Link>
              );
            })}
          </div>

          <button
            onClick={() => onLanguageChange(language === "en" ? "rw" : "en")}
            className="flex items-center gap-2 px-3 py-2 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
          >
            <Globe className="w-4 h-4 text-gray-600" />
            <span className="text-sm font-medium text-gray-700">
              {language === "en" ? "RW" : "EN"}
            </span>
          </button>
        </div>
      </div>

      <div className="md:hidden border-t border-gray-100 px-2 py-2 flex justify-around">
        {links.map((link) => {
          const Icon = link.icon;
          const isActive = pathname === link.href;
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`flex flex-col items-center gap-1 px-3 py-2 rounded-lg text-xs font-medium transition-colors ${
                isActive
                  ? "text-primary-600"
                  : "text-gray-500"
              }`}
            >
              <Icon className="w-5 h-5" />
              {link.label}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
