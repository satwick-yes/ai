"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, FileText, Send, CheckCircle2, AlertCircle, BarChart3, Users, Languages } from "lucide-react";

interface Candidate {
  name: string;
  score: number;
  skills: string[];
  relevance: string;
  semantic_score: number;
  skill_score: number;
  keyword_score: number;
  matched_skills: string[];
  missing_skills: string[];
}

export default function Dashboard() {
  const [jobDescription, setJobDescription] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const [results, setResults] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [webSkills, setWebSkills] = useState<string[]>([]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
    }
  };

  const handleRank = async () => {
    if (!jobDescription || files.length === 0) {
      setError("Please provide both a job description and at least one resume.");
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("job_description", jobDescription);
    files.forEach((file) => {
      formData.append("resumes", file);
    });

    try {
      const response = await fetch("http://localhost:8000/rank-resumes", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to rank resumes. Please ensure the backend is running.");
      }

      const data = await response.json();
      setResults(data.candidates || []);
      setWebSkills(data.web_skills || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#030712] text-white p-6 md:p-12">
      <div className="max-w-7xl mx-auto">
        <header className="mb-12 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold gradient-text mb-2">ResumeAI Dashboard</h1>
            <p className="text-gray-400">Identify top talent with precision and speed.</p>
          </div>
          <div className="hidden md:flex gap-4">
            <div className="glass px-4 py-2 flex items-center gap-2">
              <Users size={18} className="text-blue-400" />
              <span className="text-sm font-medium">Recruiter Mode</span>
            </div>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Inputs Section */}
          <div className="lg:col-span-1 space-y-8">
            <section className="glass-card p-6">
              <div className="flex items-center gap-3 mb-4">
                <FileText className="text-blue-400" />
                <h2 className="text-xl font-semibold">Job Description</h2>
              </div>
              <textarea
                className="w-full h-64 bg-black/30 border border-white/10 rounded-xl p-4 text-sm focus:ring-2 focus:ring-blue-500 outline-none resize-none transition-all"
                placeholder="Paste the job requirements here..."
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
              />
            </section>

            <section className="glass-card p-6">
              <div className="flex items-center gap-3 mb-4">
                <Upload className="text-purple-400" />
                <h2 className="text-xl font-semibold">Upload Resumes</h2>
              </div>
              <div className="relative group">
                <input
                  type="file"
                  multiple
                  accept=".pdf,.docx"
                  onChange={handleFileChange}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                />
                <div className="border-2 border-dashed border-white/10 rounded-xl p-8 text-center group-hover:border-blue-500/50 transition-colors">
                  <Upload className="mx-auto mb-4 text-gray-500 group-hover:text-blue-400 transition-colors" size={32} />
                  <p className="text-sm text-gray-400">
                    {files.length > 0
                      ? `${files.length} files selected`
                      : "Drag & drop or click to upload PDF/DOCX"}
                  </p>
                </div>
              </div>
              {files.length > 0 && (
                <div className="mt-4 space-y-2 max-h-32 overflow-y-auto">
                  {files.map((file, idx) => (
                    <div key={idx} className="flex items-center gap-2 text-xs text-gray-400 bg-white/5 p-2 rounded">
                      <FileText size={14} />
                      <span className="truncate">{file.name}</span>
                    </div>
                  ))}
                </div>
              )}
            </section>

            <button
              onClick={handleRank}
              disabled={loading}
              className="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl font-bold text-lg hover:opacity-90 transition-all flex items-center justify-center gap-2 shadow-lg shadow-blue-900/20 disabled:opacity-50"
            >
              {loading ? (
                <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  <Send size={20} />
                  Run AI Screening
                </>
              )}
            </button>

            {error && (
              <div className="p-4 bg-red-900/20 border border-red-500/30 rounded-xl flex items-start gap-3">
                <AlertCircle className="text-red-400 shrink-0" size={20} />
                <p className="text-sm text-red-200">{error}</p>
              </div>
            )}
          </div>

          {/* Results Section */}
          <div className="lg:col-span-2">
            <section className="glass-card min-h-[600px] p-8">
              <div className="flex justify-between items-center mb-8">
                <div className="flex items-center gap-3">
                  <BarChart3 className="text-pink-400" />
                  <h2 className="text-2xl font-bold">Ranking Results</h2>
                </div>
                {results.length > 0 && (
                  <span className="text-xs font-mono bg-blue-500/20 text-blue-300 px-3 py-1 rounded-full border border-blue-500/30">
                    {results.length} Candidates Scored
                  </span>
                )}
              </div>

              <AnimatePresence mode="wait">
                {webSkills.length > 0 && (
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mb-6 p-4 glass border-blue-500/30 rounded-xl">
                    <h3 className="text-sm font-semibold text-blue-400 mb-2 flex items-center gap-2">
                       <Languages size={16} /> Web-Searched Required Skills Detected:
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {webSkills.map((skill, idx) => (
                        <span key={idx} className="bg-blue-500/20 text-blue-100 text-xs px-2 py-1 rounded border border-blue-500/30">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </motion.div>
                )}
                {results.length > 0 ? (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="space-y-4"
                  >
                    {results.map((candidate, idx) => (
                      <motion.div
                        key={idx}
                        initial={{ x: 20, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        transition={{ delay: idx * 0.1 }}
                        className="glass p-5 flex flex-col gap-4 border-l-4"
                        style={{
                          borderLeftColor:
                            candidate.score > 70 ? "#10b981" : 
                            candidate.score > 40 ? "#f59e0b" : "#ef4444"
                        }}
                      >
                        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                            <div className="flex-1">
                            <h3 className="text-xl font-bold text-gray-100 mb-2">{candidate.name}</h3>
                            <div className="flex flex-wrap gap-2">
                                {candidate.skills.slice(0, 5).map((skill, sIdx) => (
                                <span key={sIdx} className="bg-white/5 text-[10px] uppercase tracking-wider px-2 py-1 rounded border border-white/10 text-gray-400">
                                    {skill}
                                </span>
                                ))}
                                {candidate.skills.length > 5 && (
                                <span className="text-[10px] text-gray-500 self-center">+{candidate.skills.length - 5} more</span>
                                )}
                            </div>
                            </div>

                            <div className="flex items-center gap-8 pl-6 border-l border-white/5">
                            <div className="text-right">
                                <p className="text-[10px] text-gray-500 uppercase tracking-tighter mb-1">Relevance</p>
                                <span className={`text-sm font-bold ${
                                candidate.relevance === "High" ? "text-emerald-400" :
                                candidate.relevance === "Medium" ? "text-amber-400" : "text-rose-400"
                                }`}>
                                {candidate.relevance}
                                </span>
                            </div>
                            <div className="w-16 h-16 rounded-full border-4 border-white/5 flex items-center justify-center relative shrink-0">
                                <svg className="w-full h-full -rotate-90 absolute inset-0">
                                    <circle 
                                        cx="32" cy="32" r="28" 
                                        className="stroke-white/5 fill-transparent" strokeWidth="4" 
                                    ></circle>
                                    <circle 
                                        cx="32" cy="32" r="28" 
                                        className="stroke-blue-500 fill-transparent transition-all duration-1000" 
                                        strokeWidth="4" 
                                        strokeDasharray={`${2 * Math.PI * 28}`}
                                        strokeDashoffset={`${2 * Math.PI * 28 * (1 - candidate.score / 100)}`}
                                        strokeLinecap="round"
                                    ></circle>
                                </svg>
                                <span className="text-lg font-black">{Math.round(candidate.score)}</span>
                            </div>
                            </div>
                        </div>

                        <div className="pt-4 border-t border-white/10 grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <h4 className="text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-2">Score Breakdown</h4>
                                <div className="space-y-1 text-xs font-mono">
                                    <div className="flex justify-between items-center bg-white/5 px-2 py-1 rounded">
                                        <span className="text-gray-400">Semantic AI (50%)</span>
                                        <span className="text-blue-400">{candidate.semantic_score}%</span>
                                    </div>
                                    <div className="flex justify-between items-center bg-white/5 px-2 py-1 rounded">
                                        <span className="text-gray-400">Skill Target (30%)</span>
                                        <span className="text-emerald-400">{candidate.skill_score}%</span>
                                    </div>
                                    <div className="flex justify-between items-center bg-white/5 px-2 py-1 rounded">
                                        <span className="text-gray-400">Keywords (20%)</span>
                                        <span className="text-purple-400">{candidate.keyword_score}%</span>
                                    </div>
                                </div>
                            </div>
                            <div>
                                <h4 className="text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-2">Missing Demanded Skills</h4>
                                <div className="flex flex-wrap gap-1.5">
                                    {candidate.missing_skills?.length > 0 ? (
                                        candidate.missing_skills.map((ms, msIdx) => (
                                            <span key={msIdx} className="bg-red-500/10 text-red-400 text-[10px] px-2 py-0.5 rounded border border-red-500/20">
                                                {ms}
                                            </span>
                                        ))
                                    ) : (
                                        <span className="text-emerald-400 font-medium text-xs flex items-center gap-1">
                                            <CheckCircle2 size={14} /> Perfect skills match!
                                        </span>
                                    )}
                                </div>
                            </div>
                        </div>
                      </motion.div>
                    ))}
                  </motion.div>
                ) : (
                  <div className="h-[400px] flex flex-col items-center justify-center text-center opacity-40">
                    <BarChart3 size={64} className="mb-4 text-gray-600" />
                    <p className="text-lg">No analysis data yet.</p>
                    <p className="text-sm">Upload resumes and run the screening to see results.</p>
                  </div>
                )}
              </AnimatePresence>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
}
