'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { counselorAPI, dashboardAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store';

interface ChatMessage {
  id: number;
  role: string;
  message: string;
  created_at: string;
}

interface Question {
  id: string;
  title: string;
  description: string;
  suggested_message: string;
}

export default function CounselorPage() {
  const router = useRouter();
  const { isAuthenticated, logout } = useAuthStore();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [lockedCount, setLockedCount] = useState(0);
  const [checkingAccess, setCheckingAccess] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/auth/login');
      return;
    }
    checkLockedUniversities();
    loadHistory();
    loadQuestions();
  }, [isAuthenticated]);

  const checkLockedUniversities = async () => {
    try {
      const res = await dashboardAPI.get();
      setLockedCount(res.data.locked_universities_count);
    } catch (error) {
      console.error('Failed to check locked universities:', error);
    } finally {
      setCheckingAccess(false);
    }
  };

  const loadHistory = async () => {
    try {
      const res = await counselorAPI.getHistory();
      setMessages(res.data);
    } catch (error) {
      console.error('Failed to load history:', error);
    } finally {
      setLoadingHistory(false);
    }
  };

  const loadQuestions = async () => {
    try {
      const res = await counselorAPI.getQuestions();
      setQuestions(res.data.questions);
    } catch (error) {
      console.error('Failed to load questions:', error);
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    setLoading(true);

    try {
      const res = await counselorAPI.chat(userMessage);
      // Add both user and AI messages to the conversation
      if (res.data.conversation) {
        setMessages((prev) => [...prev, ...res.data.conversation]);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleQuestionClick = async (message: string) => {
    setLoading(true);

    try {
      const res = await counselorAPI.chat(message);
      // Add both user and AI messages to the conversation
      if (res.data.conversation) {
        setMessages((prev) => [...prev, ...res.data.conversation]);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-blue-950">
      {/* StudyAbroad AI Branding - Fixed Left Top */}
      <div className="fixed left-6 top-6 z-30">
        <Link href="/dashboard" className="flex items-center gap-2 group">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-lg group-hover:scale-110 transition"></div>
          <span className="text-2xl font-black bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
            StudyAbroad AI
          </span>
        </Link>
      </div>

      {/* Profile & Logout - Fixed Right Top */}
      <div className="fixed right-6 top-6 z-30 flex items-center space-x-3">
        <Link
          href="/profile"
          className="text-gray-300 hover:text-white px-4 py-2 rounded-lg hover:bg-white/10 transition font-medium backdrop-blur-md bg-black/40"
        >
           Profile
        </Link>
        <button
          onClick={handleLogout}
          className="bg-gradient-to-r from-red-500 to-red-600 text-white px-5 py-2 rounded-lg hover:shadow-lg hover:shadow-red-500/50 transition font-medium"
        >
          Logout
        </button>
      </div>

      {/* Navigation */}
      <nav className="backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-center items-center h-16">
            <div className="flex items-center space-x-1">
              <Link
                href="/dashboard"
                className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-white/10 transition"
              >
                 Dashboard
              </Link>
              <Link
                href="/universities"
                className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-white/10 transition"
              >
                 Universities
              </Link>
              <Link
                href="/counselor"
                className="text-cyan-400 font-semibold px-3 py-2 rounded-lg bg-white/10"
              >
                 AI Counselor
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Access Gate - Show if less than 3 locked universities */}
        {checkingAccess ? (
          <div className="text-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-400 mx-auto"></div>
            <p className="mt-4 text-gray-400">Checking access...</p>
          </div>
        ) : lockedCount < 3 ? (
          <div className="max-w-2xl mx-auto mt-20">
            <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl p-12 text-center">
              <div className="text-6xl mb-6"></div>
              <p className="text-xl text-gray-300">
                To unlock the AI Counselor, you need to commit to at least 3 universities.
              </p>
            </div>
          </div>
        ) : (
          <>
        {/* Header */}
        <div className="mb-8 flex justify-between items-start">
          <div>
            <h1 className="text-4xl font-bold text-white">AI Study Abroad Counselor</h1>
            <p className="text-gray-400 mt-2 text-lg">
              Get personalized guidance and recommendations for your study abroad journey
            </p>
          </div>
          <button
            onClick={async () => {
              if (window.confirm('Are you sure you want to clear all chat messages?')) {
                try {
                  await counselorAPI.clearHistory();
                  setMessages([]);
                } catch (error) {
                  console.error('Failed to clear history:', error);
                }
              }
            }}
            className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition flex items-center gap-2 shadow-lg hover:shadow-red-500/50"
            title="Clear all chat messages"
          >
            <svg
              className="w-5 h-5"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Clear Chat
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Chat Area */}
          <div className="lg:col-span-2">
            <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl shadow-blue-500/10 h-[calc(100vh-280px)] flex flex-col">
              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {loadingHistory ? (
                  <div className="text-center text-gray-400">Loading chat history...</div>
                ) : messages.length === 0 ? (
                  <div className="text-center text-gray-400 mt-8">
                    <p className="text-lg font-semibold mb-4"> Welcome to your AI Counselor!</p>
                    <p className="mb-6">Select a question from the right panel or ask me anything about your study abroad journey.</p>
                    <div className="text-xs text-gray-500 bg-white/5 rounded p-3 inline-block">
                       Tip: Ask about your profile, universities, timeline, budget, tests, or visa requirements
                    </div>
                  </div>
                ) : (
                  messages.map((msg) => (
                    <div key={msg.id} className="space-y-3">
                      {/* User Message */}
                      {msg.role === 'user' && (
                        <div className="flex justify-end">
                          <div className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white px-4 py-2 rounded-lg max-w-xs break-words shadow-lg">
                            {msg.message}
                          </div>
                        </div>
                      )}
                      {/* AI Response */}
                      {msg.role === 'assistant' && (
                        <div className="flex justify-start">
                          <div className="bg-white/10 backdrop-blur-sm text-gray-200 px-4 py-2 rounded-lg max-w-md whitespace-pre-wrap border border-white/20">
                            {msg.message}
                          </div>
                        </div>
                      )}
                    </div>
                  ))
                )}
                {loading && (
                  <div className="flex justify-start">
                    <div className="bg-white/10 backdrop-blur-sm text-gray-400 px-4 py-2 rounded-lg border border-white/20">
                      AI is typing...
                    </div>
                  </div>
                )}
              </div>

              {/* Input */}
              <div className="p-6 border-t border-white/10">
                <div className="flex gap-3">
                  <input
                    type="text"
                    className="flex-1 px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-cyan-400 focus:border-transparent backdrop-blur-sm"
                    placeholder="Ask a follow-up question or type your own..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    disabled={loading}
                  />
                  <button
                    onClick={handleSend}
                    disabled={loading || !input.trim()}
                    className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white px-6 py-3 rounded-lg hover:bg-white hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition shadow-lg"
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Predefined Questions Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl shadow-blue-500/10 p-6">
              <h2 className="text-lg font-bold text-cyan-400 mb-4">Quick Questions</h2>
              {questions.length === 0 ? (
                <div className="text-center text-gray-400 text-sm">Loading questions...</div>
              ) : (
                <div className="space-y-3">
                  {questions.map((question) => (
                    <button
                      key={question.id}
                      onClick={() => handleQuestionClick(question.suggested_message)}
                      disabled={loading}
                      className="w-full text-left p-3 bg-gradient-to-br from-blue-900/30 to-cyan-900/30 hover:from-blue-800/40 hover:to-cyan-800/40 border border-cyan-400/30 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed backdrop-blur-sm"
                    >
                      <div className="font-semibold text-white text-sm mb-1">
                        {question.title}
                      </div>
                      <div className="text-xs text-gray-400 line-clamp-2">
                        {question.description}
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
        </>
        )}
      </div>
    </div>
  );
}
