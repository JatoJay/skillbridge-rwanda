"use client";

import { useState } from "react";
import "./globals.css";
import Navbar from "@/components/Navbar";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [language, setLanguage] = useState("en");

  return (
    <html lang={language}>
      <head>
        <title>SkillBridge Rwanda - AI Job Matching Platform</title>
        <meta name="description" content="Connecting skilled professionals with employment opportunities in Rwanda" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body className="bg-gray-50 min-h-screen">
        <Navbar language={language} onLanguageChange={setLanguage} />
        <main className="pb-8">
          {typeof children === "function"
            ? (children as (props: { language: string }) => React.ReactNode)({ language })
            : children}
        </main>
      </body>
    </html>
  );
}
