"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, Brain, Zap, Shield, ChevronRight, BarChart, Users, FileSearch } from "lucide-react";

export default function LandingPage() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { 
        staggerChildren: 0.2,
        delayChildren: 0.3
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  return (
    <div className="min-h-screen bg-[#030712] selection:bg-blue-500/30">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 glass border-b border-white/5 px-6 md:px-12 py-4 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-purple-600 flex items-center justify-center">
            <Brain size={18} className="text-white" />
          </div>
          <span className="text-xl font-black tracking-tight text-white">Resume<span className="text-blue-500">AI</span></span>
        </div>
        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-400">
          <a href="#features" className="hover:text-white transition-colors">Features</a>
          <a href="#how-it-works" className="hover:text-white transition-colors">How it Works</a>
          <Link href="/dashboard" className="px-5 py-2 rounded-full bg-white text-black hover:bg-gray-200 transition-all font-bold">
            Launch App
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6 md:px-12 relative overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] bg-blue-600/10 blur-[120px] rounded-full pointer-events-none" />
        
        <motion.div 
          className="max-w-5xl mx-auto text-center"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div variants={itemVariants} className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-bold mb-8">
            <Zap size={12} fill="currentColor" />
            <span>AI-POWERED RECRUITMENT 2.0</span>
          </motion.div>
          
          <motion.h1 variants={itemVariants} className="text-6xl md:text-8xl font-black tracking-tight mb-8 leading-[1.1]">
            Next Generation <br />
            <span className="gradient-text">Candidate Screening</span>
          </motion.h1>
          
          <motion.p variants={itemVariants} className="text-xl text-gray-400 max-w-2xl mx-auto mb-12">
            Leverage advanced TF-IDF analysis and weighted skill extraction to find perfect matches in seconds, not days.
          </motion.p>
          
          <motion.div variants={itemVariants} className="flex flex-col sm:flex-row items-center justify-center gap-6">
            <Link href="/dashboard" className="group px-8 py-4 bg-blue-600 rounded-2xl font-bold text-lg hover:bg-blue-500 transition-all flex items-center gap-2 shadow-2xl shadow-blue-600/20">
              Start Screening Now
              <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
            </Link>
            <button className="px-8 py-4 glass text-white font-bold text-lg border-white/10 hover:border-white/20 transition-all">
              Watch Demo
            </button>
          </motion.div>
        </motion.div>

        {/* Hero Visual */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 1, duration: 1 }}
          className="mt-20 max-w-6xl mx-auto glass-card border-white/10 p-4 aspect-[16/9] md:aspect-[21/9] overflow-hidden"
        >
          <div className="w-full h-full bg-[#030712] rounded-lg border border-white/5 flex items-center justify-center opacity-50 italic text-gray-700">
             Dashboard Preview
          </div>
        </motion.div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-24 px-6 md:px-12 bg-black/50">
        <div className="max-w-7xl mx-auto">
          <div className="mb-20">
            <h2 className="text-4xl font-bold mb-4">Precision Engineering</h2>
            <p className="text-gray-400">Our AI uses a multi-layered approach to resume evaluation.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="glass-card p-10">
              <div className="w-12 h-12 rounded-2xl bg-blue-500/20 flex items-center justify-center mb-6">
                <FileSearch className="text-blue-400" />
              </div>
              <h3 className="text-xl font-bold mb-4">Semantic Analysis</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Using TF-IDF and Cosine Similarity to understand the deep semantic relationship between job descriptions and resumes.
              </p>
            </div>

            <div className="glass-card p-10">
              <div className="w-12 h-12 rounded-2xl bg-purple-500/20 flex items-center justify-center mb-6">
                <Zap className="text-purple-400" />
              </div>
              <h3 className="text-xl font-bold mb-4">Fast Extraction</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Instant extraction of technical and soft skills from PDF and DOCX files using high-performance parsing utility.
              </p>
            </div>

            <div className="glass-card p-10">
              <div className="w-12 h-12 rounded-2xl bg-pink-500/20 flex items-center justify-center mb-6">
                <BarChart className="text-pink-400" />
              </div>
              <h3 className="text-xl font-bold mb-4">Weighted Scoring</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Customizable scoring weights ensure that both overall experience and specific skill matches contribute to the final rank.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-white/5 px-6 md:px-12">
        <div className="max-w-7xl mx-auto flex flex-col md:row justify-between items-center gap-8">
          <div className="flex items-center gap-2">
            <Brain size={24} className="text-blue-500" />
            <span className="text-xl font-black text-white">ResumeAI</span>
          </div>
          <div className="text-gray-500 text-sm">
            © 2026 ResumeAI. Built for high-performance HR teams.
          </div>
          <div className="flex gap-6 text-gray-400">
             <a href="#" className="hover:text-white transition-colors text-xs font-semibold">Privacy Policy</a>
             <a href="#" className="hover:text-white transition-colors text-xs font-semibold">Terms of Service</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
