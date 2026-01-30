'use client';

import { useState, useEffect, useRef } from 'react';
import { usePathname } from 'next/navigation';
import { counselorAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store';

interface Message {
  id: number;
  message: string;
  role: 'user' | 'assistant';
  timestamp: string;
}

const SUGGESTED_QUESTIONS = [
  'Profile assessment and strengths/gaps analysis',
  'University recommendations based on your profile',
  'Application timeline and to-do list',
  'Budget and funding planning',
  'Test preparation strategy',
  'Visa and documentation guidance',
];

export default function ChatBot() {
  const { isAuthenticated } = useAuthStore();
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Don't show chatbot on auth pages, landing page, or onboarding
  const excludedPaths = ['/', '/auth/login', '/auth/signup', '/onboarding'];
  const shouldHide = excludedPaths.includes(pathname);

  useEffect(() => {
    // Load chat history on component mount if authenticated
    if (isAuthenticated) {
      loadHistory();
    }
  }, [isAuthenticated]);

  useEffect(() => {
    if (isOpen && isAuthenticated && messages.length === 0) {
      loadHistory();
    }
  }, [isOpen, isAuthenticated]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadHistory = async () => {
    try {
      const res = await counselorAPI.getHistory();
      setMessages(res.data);
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  };

  const handleSendMessage = async (message: string) => {
    setInput('');
    setLoading(true);

    // Add user message immediately
    const userMsg: Message = {
      id: Date.now(),
      message: message,
      role: 'user',
      timestamp: new Date().toISOString(),
    };

    try {
      const res = await counselorAPI.chat(message);
      setMessages(prev => [...prev, userMsg, res.data]);
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    await handleSendMessage(input);
  };

  const handleQuestionClick = async (question: string) => {
    await handleSendMessage(question);
  };

  // Don't render on excluded paths or when not authenticated
  if (!isAuthenticated || shouldHide) return null;

  return (
    <>
      {/* Floating Chat Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 bg-green-600 text-white p-4 rounded-full shadow-lg hover:bg-green-700 transition z-50 flex items-center gap-2"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
            />
          </svg>
          <span className="font-semibold">AI Counselor</span>
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-96 h-[600px] bg-white rounded-lg shadow-2xl z-50 flex flex-col border border-gray-200">
          {/* Header */}
          <div className="bg-green-600 text-white p-4 rounded-t-lg flex justify-between items-center">
            <div>
              <h3 className="font-bold text-lg">AI Study Abroad Counselor</h3>
              <p className="text-xs text-green-100">Ask me anything!</p>
            </div>
            <div className="flex gap-3 items-center">
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
                className="px-3 py-1 bg-red-500 hover:bg-red-600 text-white text-sm rounded transition flex items-center gap-1"
                title="Clear all chat messages"
              >
                <svg
                  className="w-4 h-4"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Clear
              </button>
              <button
                onClick={() => setIsOpen(false)}
                className="p-1 hover:bg-green-700 rounded transition"
                title="Close"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
            {messages.length === 0 ? (
              <div className="space-y-4">
                <div className="text-center text-gray-600 mb-4">
                  <div className="text-4xl mb-2"></div>
                  <p className="font-semibold mb-1">Welcome!</p>
                  <p className="text-sm">Select a question to get started</p>
                </div>
                
                {/* Suggested Questions */}
                <div className="space-y-2">
                  {SUGGESTED_QUESTIONS.map((question, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleQuestionClick(question)}
                      disabled={loading}
                      className="w-full text-left px-4 py-3 bg-gradient-to-r from-green-50 to-emerald-50 hover:from-green-100 hover:to-emerald-100 text-gray-800 rounded-lg text-sm transition border border-green-300 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                    >
                       {question}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <>
                {messages.map((msg, idx) => (
                  <div
                    key={msg.id || idx}
                    className={`flex ${
                      msg.role === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    <div
                      className={`px-4 py-3 rounded-lg max-w-[75%] break-words leading-relaxed ${
                        msg.role === 'user'
                          ? 'bg-green-600 text-white rounded-br-none'
                          : 'bg-white text-gray-800 shadow-md rounded-bl-none border-l-4 border-green-500'
                      }`}
                    >
                      {msg.role === 'assistant' ? (
                        <div className="prose prose-sm max-w-none">
                          {msg.message.includes('[CLICKABLE_ACTIONS]') ? (
                            // Render clickable action items
                            <div>
                              {msg.message.split('[CLICKABLE_ACTIONS]')[0] && (
                                <div className="mb-3">
                                  {msg.message.split('[CLICKABLE_ACTIONS]')[0].split('\n').map((line, i) => 
                                    line.trim() && (
                                      <p key={i} className="mb-2">{line}</p>
                                    )
                                  )}
                                </div>
                              )}
                              
                              <div className="space-y-2 my-3">
                                {msg.message
                                  .split('[CLICKABLE_ACTIONS]')[1]
                                  .split('[/CLICKABLE_ACTIONS]')[0]
                                  .split('\n')
                                  .filter(line => line.trim())
                                  .map((action, idx) => (
                                    <button
                                      key={idx}
                                      onClick={() => handleQuestionClick(action.trim())}
                                      className="w-full text-left px-3 py-2 bg-gradient-to-r from-blue-50 to-cyan-50 hover:from-blue-100 hover:to-cyan-100 text-gray-800 rounded border border-blue-300 text-sm transition hover:shadow-md"
                                    >
                                      ▸ {action.trim()}
                                    </button>
                                  ))}
                              </div>

                              {msg.message.split('[/CLICKABLE_ACTIONS]')[1] && (
                                <div className="mt-3">
                                  {msg.message.split('[/CLICKABLE_ACTIONS]')[1].split('\n').map((line, i) => 
                                    line.trim() && (
                                      <p key={i} className="mb-2">{line}</p>
                                    )
                                  )}
                                </div>
                              )}
                            </div>
                          ) : (
                            // Render normal text response
                            msg.message.split('\n').map((line, i) => {
                              // Bold headers (lines starting with ** or single words followed by :)
                              if (line.includes('**')) {
                                return (
                                  <p key={i} className="font-semibold text-green-700 mb-1 mt-2 first:mt-0">
                                    {line.replace(/\*\*/g, '')}
                                  </p>
                                );
                              }
                              // Bullet points
                              if (line.trim().startsWith('') || line.trim().startsWith('•') || line.trim().startsWith('-')) {
                                return (
                                  <div key={i} className="ml-2 mb-1 flex gap-2">
                                    <span className="text-green-600 font-bold"></span>
                                    <span>{line.trim().replace(/^[•-]\s*/, '')}</span>
                                  </div>
                                );
                              }
                              // Numbered items
                              if (/^\d+\./.test(line.trim())) {
                                return (
                                  <div key={i} className="ml-2 mb-1 flex gap-2">
                                    <span className="text-green-600 font-bold">{line.match(/^\d+/)?.[0]}.</span>
                                    <span>{line.replace(/^\d+\.\s*/, '')}</span>
                                  </div>
                                );
                              }
                              // Regular paragraphs
                              if (line.trim()) {
                                return (
                                  <p key={i} className="mb-2">
                                    {line}
                                  </p>
                                );
                              }
                              return null;
                            })
                          )}
                        </div>
                      ) : (
                        <p>{msg.message}</p>
                      )}
                    </div>
                  </div>
                ))}
                
                {/* Show suggested questions when there are messages but no new ones being typed */}
                {messages.length > 0 && !loading && (
                  <div className="mt-4 pt-4 border-t border-gray-300">
                    <p className="text-xs text-gray-600 font-semibold mb-3 uppercase tracking-wide"> Continue asking:</p>
                    <div className="space-y-2">
                      {SUGGESTED_QUESTIONS.filter(q => {
                        const hasAsked = messages.some(m => 
                          m.role === 'user' && 
                          m.message.toLowerCase().trim() === q.toLowerCase().trim()
                        );
                        return !hasAsked;
                      }).map((question, idx) => (
                        <button
                          key={idx}
                          onClick={() => handleQuestionClick(question)}
                          disabled={loading}
                          className="w-full text-left px-3 py-2 bg-gradient-to-r from-green-50 to-emerald-50 hover:from-green-100 hover:to-emerald-100 text-gray-700 rounded-lg text-xs transition border border-green-200 disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-sm"
                        >
                           {question}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}
            
            {loading && (
              <div className="flex justify-start">
                <div className="bg-white text-gray-600 px-4 py-2 rounded-lg shadow">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t bg-white rounded-b-lg">
            <div className="flex gap-2">
              <input
                type="text"
                className="flex-1 px-4 py-2 border rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-green-600"
                placeholder="Type your question..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                disabled={loading}
              />
              <button
                onClick={handleSend}
                disabled={loading || !input.trim()}
                className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
