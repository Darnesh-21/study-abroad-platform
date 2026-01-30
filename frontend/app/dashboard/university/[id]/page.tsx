'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { dashboardAPI, todosAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import { Dashboard } from '@/lib/types';

export default function UniversityDetailPage() {
  const router = useRouter();
  const params = useParams();
  const universityId = parseInt(params.id as string);
  const { isAuthenticated, logout } = useAuthStore();
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [loading, setLoading] = useState(true);
  const [isTasksExpanded, setIsTasksExpanded] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/auth/login');
      return;
    }

    loadDashboard();
  }, [isAuthenticated]);

  const loadDashboard = async () => {
    try {
      const res = await dashboardAPI.get();
      setDashboard(res.data);
    } catch (error) {
      console.error('Failed to load dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-blue-950 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 mb-4 rounded-full bg-white/10 border border-white/20 animate-spin">
            <div className="w-12 h-12 rounded-full border-4 border-white/10 border-t-cyan-400"></div>
          </div>
          <p className="text-xl text-gray-400">Loading...</p>
        </div>
      </div>
    );
  }

  const commitment = dashboard?.committed_universities?.find(
    c => c.shortlisted_university.id === universityId
  );

  if (!commitment) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-blue-950">
        <div className="fixed left-6 top-6 z-30">
          <Link href="/dashboard" className="flex items-center gap-2 group">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-lg group-hover:scale-110 transition"></div>
            <span className="text-2xl font-black bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
              StudyAbroad AI
            </span>
          </Link>
        </div>
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
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-white/10 transition"
                >
                   AI Counselor
                </Link>
              </div>
            </div>
          </div>
        </nav>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <p className="text-xl text-gray-400 mb-4">University not found</p>
            <Link
              href="/dashboard"
              className="inline-block px-6 py-2 bg-gradient-to-r from-blue-500 to-cyan-500 text-white rounded-lg hover:shadow-lg hover:shadow-blue-500/30 transition font-medium"
            >
              ← Back to Dashboard
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-blue-950">
      <div className="fixed left-6 top-6 z-30">
        <Link href="/dashboard" className="flex items-center gap-2 group">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-lg group-hover:scale-110 transition"></div>
          <span className="text-2xl font-black bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
            StudyAbroad AI
          </span>
        </Link>
      </div>
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
                className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-white/10 transition"
              >
                 AI Counselor
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Back Button */}
        <button
          onClick={() => router.back()}
          className="mb-6 text-gray-400 hover:text-white flex items-center gap-2 transition"
        >
          ← Back to Universities
        </button>

        {/* University Header */}
        <div className="bg-gradient-to-r from-blue-500/20 to-cyan-500/20 border border-white/20 p-8 rounded-xl mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">
            {commitment.shortlisted_university.university.name}
          </h1>
          <div className="flex items-center gap-6 text-gray-300">
            <span className="flex items-center gap-2">
               {commitment.shortlisted_university.university.country}
            </span>
            <span className="px-4 py-2 bg-blue-500/30 border border-blue-400/50 text-blue-300 font-medium rounded">
              {commitment.shortlisted_university.category}
            </span>
          </div>
          {commitment.shortlisted_university.fit_reason && (
            <p className="text-gray-300 mt-6">
              <span className="font-medium text-cyan-300">Why this fit:</span> {commitment.shortlisted_university.fit_reason}
            </p>
          )}
        </div>

        {/* AI To-Do List */}
        <div className="mb-8">
          <button
            onClick={() => setIsTasksExpanded(!isTasksExpanded)}
            className="w-full flex items-center justify-between p-4 bg-white/5 border border-white/20 rounded-xl hover:bg-white/10 transition mb-4"
          >
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
               AI To-Do List ({commitment.tasks.length} tasks)
            </h2>
            <span className="text-2xl text-white">
              {isTasksExpanded ? '▼' : '▶'}
            </span>
          </button>
          
          {isTasksExpanded && (
            <>
              {commitment.tasks.length === 0 ? (
                <p className="text-gray-400">No pending tasks for this university</p>
              ) : (
                <div className="space-y-3">
                  {commitment.tasks.map((task) => (
                    <div
                      key={task.id}
                      className="flex items-start gap-3 p-4 bg-white/5 border border-white/20 rounded-lg hover:border-white/30 transition"
                    >
                      <button
                        onClick={() => {
                          // Update local state immediately
                          if (dashboard) {
                            const updatedDashboard = {
                              ...dashboard,
                              committed_universities: dashboard.committed_universities?.map(cu => ({
                                ...cu,
                                tasks: cu.tasks.map(t => 
                                  t.id === task.id ? { ...t, is_completed: !t.is_completed } : t
                                )
                              }))
                            };
                            setDashboard(updatedDashboard);
                            
                            // Call API in background
                            todosAPI.update(task.id, { is_completed: !task.is_completed }).catch(err => {
                              console.error('Failed to update todo:', err);
                            });
                          }
                        }}
                        className="flex-shrink-0"
                      >
                        <div className={`w-5 h-5 rounded border-2 mt-1 flex items-center justify-center transition ${
                          task.is_completed 
                            ? 'bg-green-500 border-green-500' 
                            : 'border-gray-400 hover:border-green-400'
                        }`}>
                          {task.is_completed && (
                            <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                          )}
                        </div>
                      </button>
                      <div className="flex-1">
                        <p className={`font-semibold text-base ${task.is_completed ? 'line-through text-gray-500' : 'text-white'}`}>{task.title}</p>
                        <p className={`text-sm mt-1 ${task.is_completed ? 'line-through text-gray-600' : 'text-gray-400'}`}>{task.description}</p>
                        <div className="flex items-center gap-2 mt-2">
                          <span className="text-xs px-2 py-1 bg-blue-500/20 border border-blue-400/30 text-blue-300 rounded">
                            {task.category}
                          </span>
                          <span className={`text-xs px-2 py-1 rounded ${
                            task.priority === 'High'
                              ? 'bg-red-500/20 border border-red-400/30 text-red-300'
                              : task.priority === 'Medium'
                              ? 'bg-yellow-500/20 border border-yellow-400/30 text-yellow-300'
                              : 'bg-green-500/20 border border-green-400/30 text-green-300'
                          }`}>
                            {task.priority}
                          </span>
                          {task.due_date && (
                            <span className="text-xs text-gray-400">
                              Due: {new Date(task.due_date).toLocaleDateString()}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
        </div>

        {/* Required Documents */}
        <div>
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
             Required Documents
          </h2>
          <div className="space-y-3">
            {commitment.documents.map((doc) => {
              const documentLabels: Record<string, string> = {
                SOP: 'Statement of Purpose (SOP)',
                RECOMMENDATION_LETTER: 'Letter of Recommendation',
                RESUME: 'Resume / CV',
                TRANSCRIPTS: 'Transcripts'
              };

              const statusColors: Record<string, string> = {
                DRAFTING: 'text-yellow-300',
                PENDING: 'text-orange-300',
                READY: 'text-green-300',
                UPLOADED: 'text-cyan-300'
              };

              const statusBg: Record<string, string> = {
                DRAFTING: 'bg-yellow-500/10 border border-yellow-400/30',
                PENDING: 'bg-orange-500/10 border border-orange-400/30',
                READY: 'bg-green-500/10 border border-green-400/30',
                UPLOADED: 'bg-cyan-500/10 border border-cyan-400/30'
              };

              const statusIcon: Record<string, string> = {
                DRAFTING: '️',
                PENDING: '⏳',
                READY: '',
                UPLOADED: ''
              };

              return (
                <div key={doc.id} className={`flex items-center justify-between p-4 rounded-lg ${statusBg[doc.status]}`}>
                  <div className="flex items-center gap-3 flex-1">
                    <span className="text-xl">{statusIcon[doc.status]}</span>
                    <div>
                      <p className="font-medium text-white">{documentLabels[doc.document_type]}</p>
                      <p className={`text-sm ${statusColors[doc.status]}`}>
                        {doc.status.replace(/_/g, ' ')}
                        {doc.due_date && ` • Due in ${Math.ceil((new Date(doc.due_date).getTime() - Date.now()) / (1000 * 60 * 60 * 24))} days`}
                      </p>
                    </div>
                  </div>
                  <button className="px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg text-sm font-medium transition border border-white/20">
                    {doc.status === 'UPLOADED' ? ' View' : 'Upload'}
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
