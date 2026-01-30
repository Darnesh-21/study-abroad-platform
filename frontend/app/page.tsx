'use client';

import Link from 'next/link';
import { useAuthStore } from '@/lib/store';

export default function Home() {
  const { isAuthenticated } = useAuthStore();

  return (
    <main className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-blue-950 text-white">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-black/80 backdrop-blur-lg border-b border-white/10 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-lg"></div>
              <span className="text-2xl font-bold text-white">
                StudyAbroad.AI
              </span>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-300 hover:text-white transition">
                Features
              </a>
              <a href="#how-it-works" className="text-gray-300 hover:text-white transition">
                How It Works
              </a>
              <a href="#about" className="text-gray-300 hover:text-white transition">
                About
              </a>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                href="/auth/login"
                className="text-white hover:text-gray-300 transition font-medium"
              >
                Log In
              </Link>
              <Link
                href="/auth/signup"
                className="px-6 py-2 bg-white text-black rounded-lg hover:bg-gray-200 transition font-semibold"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-900/20 via-transparent to-cyan-900/20"></div>
        <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
        
        <div className="relative max-w-7xl mx-auto">
          <div className="max-w-4xl">
            <h1 className="text-6xl md:text-7xl lg:text-8xl font-bold leading-tight mb-8">
              The New Standard<br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">
                in Study Abroad
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-400 mb-12 max-w-2xl">
              Use AI to Get a 360-Degree View of Your Application Journey
            </p>
            <Link
              href="/auth/signup"
              className="inline-block px-10 py-4 bg-gradient-to-r from-blue-500 to-cyan-500 text-white text-lg font-semibold rounded-lg hover:shadow-2xl hover:shadow-blue-500/50 transition-all hover:scale-105"
            >
              Learn More
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 px-4 relative">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Powered by <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">AI Intelligence</span>
            </h2>
            <p className="text-xl text-gray-400">Everything you need for your study abroad journey</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-8 bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl hover:bg-white/10 transition group">
              <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold mb-3">AI Counselor</h3>
              <p className="text-gray-400 leading-relaxed">
                Get personalized guidance powered by advanced AI that understands your profile and goals
              </p>
            </div>

            <div className="p-8 bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl hover:bg-white/10 transition group">
              <div className="w-14 h-14 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold mb-3">Smart Matching</h3>
              <p className="text-gray-400 leading-relaxed">
                Discover universities categorized as Dream, Target, and Safe based on your profile
              </p>
            </div>

            <div className="p-8 bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl hover:bg-white/10 transition group">
              <div className="w-14 h-14 bg-gradient-to-br from-orange-500 to-yellow-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold mb-3">Track Progress</h3>
              <p className="text-gray-400 leading-relaxed">
                AI-generated to-do lists and document tracking for each university application
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-24 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Your Journey in <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">4 Simple Steps</span>
            </h2>
          </div>

          <div className="grid md:grid-cols-4 gap-8">
            {[
              { num: "01", title: "Create Profile", desc: "Share your academic background and goals" },
              { num: "02", title: "Get Recommendations", desc: "AI analyzes and suggests best-fit universities" },
              { num: "03", title: "Lock Universities", desc: "Commit to 3+ universities to unlock counselor" },
              { num: "04", title: "AI Guidance", desc: "Get personalized help throughout your journey" }
            ].map((step, index) => (
              <div key={index} className="relative">
                <div className="text-6xl font-bold text-white/5 mb-4">{step.num}</div>
                <h3 className="text-xl font-bold mb-2">{step.title}</h3>
                <p className="text-gray-400">{step.desc}</p>
                {index < 3 && (
                  <div className="hidden md:block absolute top-8 left-full w-full h-0.5 bg-gradient-to-r from-blue-500/50 to-transparent"></div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="p-12 bg-gradient-to-br from-blue-900/30 to-cyan-900/30 border border-white/10 rounded-3xl backdrop-blur-sm">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Ready to Start Your Journey?
            </h2>
            <p className="text-xl text-gray-400 mb-8">
              Join students who are successfully navigating their study abroad applications with AI guidance
            </p>
            <Link
              href="/auth/signup"
              className="inline-block px-10 py-4 bg-white text-black text-lg font-semibold rounded-lg hover:bg-gray-200 transition-all hover:scale-105"
            >
              Get Started Free
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 border-t border-white/10">
        <div className="max-w-7xl mx-auto text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-lg"></div>
            <span className="text-xl font-bold">StudyAbroad.AI</span>
          </div>
          <p className="text-gray-400">© 2026 StudyAbroad.AI. Your AI-powered study abroad companion.</p>
        </div>
      </footer>

      {/* Floating Chat Button */}
      <div className="fixed bottom-8 right-8">
        <button className="w-14 h-14 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-full shadow-2xl hover:shadow-blue-500/50 transition-all hover:scale-110 flex items-center justify-center">
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        </button>
      </div>
    </main>
  );
}
