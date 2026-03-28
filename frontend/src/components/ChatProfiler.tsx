"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Loader2, User, Bot, CheckCircle } from "lucide-react";
import { sendChatMessage, finalizeProfile, CandidateProfile, ChatMessage } from "@/lib/api";

interface ChatProfilerProps {
  language: string;
  onProfileComplete: (candidateId: string, profile: CandidateProfile) => void;
}

export default function ChatProfiler({ language, onProfileComplete }: ChatProfilerProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [profileComplete, setProfileComplete] = useState(false);
  const [extractedProfile, setExtractedProfile] = useState<CandidateProfile | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const welcomeMessage = language === "rw"
      ? "Muraho! Ndi umufasha wawe wa SkillBridge Rwanda. Mbwira ibyawe n'ubumenyi bwawe, nzagufasha kubona akazi kakwiye."
      : "Hello! I'm your SkillBridge Rwanda career assistant. Tell me about yourself and your skills, and I'll help you find the perfect job match.";

    setMessages([{ role: "assistant", content: welcomeMessage }]);
  }, [language]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = { role: "user", content: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);

    try {
      const apiMessages = newMessages.filter((_, idx) => idx > 0);
      const response = await sendChatMessage(apiMessages, sessionId || undefined, language);

      setSessionId(response.session_id);
      setMessages([...newMessages, { role: "assistant", content: response.message }]);

      if (response.profile_complete && response.extracted_profile) {
        setProfileComplete(true);
        setExtractedProfile(response.extracted_profile);
      }
    } catch (error) {
      console.error("Chat error:", error);
      setMessages([
        ...newMessages,
        { role: "assistant", content: language === "rw"
          ? "Habaye ikibazo. Ongera ugerageze."
          : "Sorry, there was an error. Please try again."
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFinalize = async () => {
    if (!sessionId) return;
    setIsLoading(true);

    try {
      const result = await finalizeProfile(sessionId);
      onProfileComplete(result.candidate_id, result.profile);
    } catch (error) {
      console.error("Finalize error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] max-w-2xl mx-auto bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
      <div className="bg-gradient-to-r from-primary-500 to-secondary-500 px-6 py-4">
        <h2 className="text-white font-semibold text-lg">
          {language === "rw" ? "Vuga n'umufasha wacu" : "Chat with Career Assistant"}
        </h2>
        <p className="text-white/80 text-sm">
          {language === "rw"
            ? "Mbwira ubumenyi bwawe n'ibyo ukunda"
            : "Tell me about your skills and preferences"}
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin bg-gray-50">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex items-start gap-3 ${msg.role === "user" ? "flex-row-reverse" : ""}`}
          >
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                msg.role === "user" ? "bg-primary-500" : "bg-secondary-500"
              }`}
            >
              {msg.role === "user" ? (
                <User className="w-4 h-4 text-white" />
              ) : (
                <Bot className="w-4 h-4 text-white" />
              )}
            </div>
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                msg.role === "user"
                  ? "bg-primary-500 text-white rounded-tr-sm"
                  : "bg-white text-gray-800 shadow-sm border border-gray-100 rounded-tl-sm"
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-full bg-secondary-500 flex items-center justify-center">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div className="bg-white rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm border border-gray-100">
              <Loader2 className="w-5 h-5 animate-spin text-secondary-500" />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {profileComplete && extractedProfile && (
        <div className="px-4 py-3 bg-green-50 border-t border-green-100">
          <div className="flex items-center gap-2 text-green-700 mb-2">
            <CheckCircle className="w-5 h-5" />
            <span className="font-medium">
              {language === "rw" ? "Umwirondoro wawe wuzuye!" : "Profile Complete!"}
            </span>
          </div>
          <button
            onClick={handleFinalize}
            disabled={isLoading}
            className="w-full bg-primary-500 text-white py-3 rounded-xl font-medium hover:bg-primary-600 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <>
                {language === "rw" ? "Reba akazi kakwiye" : "Find My Job Matches"}
              </>
            )}
          </button>
        </div>
      )}

      <div className="p-4 bg-white border-t border-gray-100">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder={language === "rw" ? "Andika hano..." : "Type your message..."}
            className="flex-1 px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="bg-primary-500 text-white px-4 py-3 rounded-xl hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
