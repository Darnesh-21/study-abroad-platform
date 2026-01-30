'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { dashboardAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import { Dashboard } from '@/lib/types';

export default function DashboardPage() {
  const router = useRouter();
  const { isAuthenticated, logout, user } = useAuthStore();
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [loading, setLoading] = useState(true);

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

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-blue-950 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 mb-4 rounded-full bg-white/10 border border-white/20 animate-spin">
            <div className="w-12 h-12 rounded-full border-4 border-white/10 border-t-cyan-400"></div>
          </div>
          <p className="text-xl text-gray-400">Loading your journey...</p>
        </div>
      </div>
    );
  }

  if (!dashboard) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-blue-950 flex items-center justify-center">
        <div className="text-center">
          <p className="text-xl text-red-400">Failed to load dashboard</p>
        </div>
      </div>
    );
  }

  // Check if onboarding is complete - but don't redirect, just show alert
  // The profile completion alert will be shown in the dashboard
  const isProfileIncomplete = !dashboard.profile.onboarding_completed;

  const getStageText = (stage: string) => {
    const stages: Record<string, string> = {
      building_profile: 'Building Profile',
      discovering_universities: 'Discovering Universities',
      finalizing_universities: 'Finalizing Universities',
      preparing_applications: 'Preparing Applications',
      BUILDING_PROFILE: 'Building Profile',
      DISCOVERING_UNIVERSITIES: 'Discovering Universities',
      FINALIZING_UNIVERSITIES: 'Finalizing Universities',
      PREPARING_APPLICATIONS: 'Preparing Applications',
    };
    return stages[stage] || stage.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join(' ');
  };

  const getStrengthColor = (strength?: string) => {
    if (!strength) return 'bg-gray-100 text-gray-800';
    const colors: Record<string, string> = {
      strong: 'bg-green-100 text-green-800',
      average: 'bg-yellow-100 text-yellow-800',
      weak: 'bg-red-100 text-red-800',
    };
    return colors[strength] || 'bg-gray-100 text-gray-800';
  };

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-blue-950">
      {/* Navigation */}
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

      {/* StudyAbroad AI Branding - Fixed Left Top */}
      <div className="fixed left-6 top-6 z-30">
        <Link href="/dashboard" className="flex items-center gap-2 group">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-lg group-hover:scale-110 transition"></div>
          <span className="text-2xl font-black bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
            StudyAbroad AI
          </span>
        </Link>
      </div>

      {/* Vertical Progress Bar - Fixed Left Side */}
      <div className="fixed left-6 top-1/2 z-30 w-32 -translate-y-1/2">
        <div className="relative bg-gradient-to-br from-blue-950/40 via-gray-900/40 to-cyan-950/40 backdrop-blur-2xl border border-cyan-400/30 rounded-3xl shadow-2xl shadow-cyan-500/20 overflow-hidden">
          {/* Glow effect */}
          <div className="absolute inset-0 bg-gradient-to-b from-cyan-500/5 via-blue-500/5 to-transparent"></div>
          
          {/* Header */}
          <div className="relative px-4 py-6 border-b border-cyan-400/20">
            <h3 className="text-base font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-300 to-blue-400 text-center tracking-wider uppercase">
              Journey
            </h3>
          </div>
          
          <div className="relative px-6 py-8">
            <div className="relative flex flex-col items-center">
              {[
                { key: 'building_profile', label: 'Building', icon: '📝' },
                { key: 'discovering_universities', label: 'Discovering', icon: '🔍' },
                { key: 'finalizing_universities', label: 'Finalizing', icon: '✓' },
                { key: 'preparing_applications', label: 'Preparing', icon: '🎓' }
              ].map((stage, index) => {
                const isActive = dashboard.profile.current_stage === stage.key || dashboard.profile.current_stage === stage.key.toUpperCase();
                const currentIndex = ['building_profile', 'discovering_universities', 'finalizing_universities', 'preparing_applications']
                  .indexOf(dashboard.profile.current_stage.toLowerCase());
                const isPast = currentIndex > index;
                
                return (
                  <div key={stage.key} className="flex flex-col items-center mb-14 last:mb-0 relative z-10">
                    <div className={`relative w-16 h-16 rounded-2xl flex items-center justify-center text-2xl font-bold transition-all duration-500 ${
                      isActive ? 'bg-gradient-to-br from-cyan-400 to-blue-500 text-white shadow-2xl shadow-cyan-400/60 scale-110' :
                      isPast ? 'bg-gradient-to-br from-emerald-400 to-green-500 text-white shadow-xl shadow-green-400/40' :
                      'bg-gray-800/60 border border-gray-600/40 text-gray-600'
                    }`}>
                      {isActive && (
                        <div className="absolute inset-0 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-2xl animate-ping opacity-20"></div>
                      )}
                      <span className="relative z-10">{isPast ? '✓' : stage.icon}</span>
                    </div>
                    <p className={`text-[10px] text-center font-bold mt-2.5 uppercase tracking-wide ${
                      isActive ? 'text-cyan-300' : isPast ? 'text-emerald-400' : 'text-gray-600'
                    }`}>
                      {stage.label}
                    </p>
                  </div>
                );
              })}
              
              {/* Vertical connecting line */}
              <div className="absolute left-1/2 top-8 bottom-8 w-0.5 bg-gradient-to-b from-gray-700/40 to-gray-800/40 -z-10 rounded-full -translate-x-1/2">
                <div 
                  className="w-full bg-gradient-to-b from-cyan-400 via-blue-500 to-cyan-500 transition-all duration-700 rounded-full shadow-lg shadow-cyan-400/50"
                  style={{
                    height: `${(['building_profile', 'discovering_universities', 'finalizing_universities', 'preparing_applications']
                      .indexOf(dashboard.profile.current_stage.toLowerCase()) / 3) * 100}%`
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Dashboard Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
            Welcome back, {dashboard.profile.full_name || user?.email?.split('@')[0] || 'Student'}! 
          </h1>
          <p className="text-gray-400 mt-2 text-lg">
            Here's your study abroad journey at a glance
          </p>
        </div>

        {/* Check if profile is complete */}
        {!dashboard.profile.onboarding_completed && (
          <div className="bg-yellow-500/20 border-2 border-yellow-400/50 p-6 rounded-xl shadow-lg shadow-yellow-500/20 mb-8">
            <div className="flex items-start gap-4">
              <span className="text-3xl">️</span>
              <div>
                <h2 className="text-xl font-bold text-white mb-2">Profile Setup Required</h2>
                <p className="text-gray-300 mb-4">
                  Complete your profile to get personalized university recommendations and start your application journey.
                </p>
                <Link
                  href="/profile"
                  className="inline-block px-6 py-2 bg-gradient-to-r from-yellow-500 to-yellow-600 text-white rounded-lg hover:shadow-lg hover:shadow-yellow-500/50 transition font-medium"
                >
                   Complete Profile
                </Link>
              </div>
            </div>
          </div>
        )}

        {/* Quick Stats */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          <div className="bg-white/10 backdrop-blur-md border border-white/20 p-8 rounded-2xl hover:border-blue-400/50 hover:bg-white/15 transition shadow-xl">
            <h3 className="text-base font-semibold text-gray-400 mb-6">
              Current Stage
            </h3>
            <p className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
              {getStageText(dashboard.profile.current_stage)}
            </p>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 p-8 rounded-2xl hover:border-green-400/50 hover:bg-white/15 transition shadow-xl">
            <h3 className="text-base font-semibold text-gray-400 mb-6">
              Shortlisted Universities
            </h3>
            <div>
              <p className="text-5xl font-bold text-white">
                {dashboard.shortlisted_universities.length}
              </p>
              <p className="text-base text-gray-400 mt-3">
                {dashboard.locked_universities_count} committed
              </p>
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 p-8 rounded-2xl hover:border-amber-400/50 hover:bg-white/15 transition shadow-xl">
            <h3 className="text-base font-semibold text-gray-400 mb-6">
              Pending Tasks
            </h3>
            <p className="text-5xl font-bold text-white">
              {dashboard.todos.length}
            </p>
            <p className="text-base text-gray-400 mt-3">
              Action items for your journey
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mb-8 flex gap-4">
          <Link
            href="/universities"
            className="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-blue-500 to-cyan-500 text-white text-lg font-semibold rounded-xl hover:bg-white hover:text-gray-900 transition-all hover:scale-105 hover:shadow-2xl"
          >
             Discover Universities
          </Link>

          {dashboard.locked_universities_count >= 3 && (
            <Link
              href="/counselor"
              className="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-blue-500 to-cyan-500 text-white text-lg font-semibold rounded-xl hover:bg-white hover:text-gray-900 transition-all hover:scale-105 hover:shadow-2xl"
            >
               AI Counselor
            </Link>
          )}
        </div>

        {/* Committed Universities with Tasks and Documents */}
        {dashboard.committed_universities && dashboard.committed_universities.length > 0 ? (
          <div>
            <h2 className="text-3xl font-bold text-white flex items-center gap-3 mb-8">
               Your Committed Universities
            </h2>
            <div className="space-y-4">
              {dashboard.committed_universities.map((commitment) => (
                <button
                  key={commitment.shortlisted_university.id}
                  onClick={() => router.push(`/dashboard/university/${commitment.shortlisted_university.id}`)}
                  className="w-full text-left bg-white/5 border border-white/20 p-6 rounded-2xl hover:bg-white/10 hover:border-blue-400/50 transition shadow-lg"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-2xl font-bold text-white">
                        {commitment.shortlisted_university.university.name}
                      </h3>
                      <p className="text-base text-gray-400 mt-2">
                         {commitment.shortlisted_university.university.country}
                      </p>
                      {commitment.tasks && commitment.tasks.length > 0 && (
                        <p className="text-sm text-cyan-400 mt-2">
                          {commitment.tasks.length} tasks • Click to view details
                        </p>
                      )}
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="px-4 py-2 bg-blue-500/30 border border-blue-400/50 text-blue-300 text-sm font-semibold rounded-lg">
                        {commitment.shortlisted_university.category}
                      </span>
                      <span className="text-3xl">→</span>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="bg-white/5 border border-white/20 p-16 rounded-2xl text-center">
            <p className="text-gray-400 text-xl mb-6">No committed universities yet</p>
            <Link
              href="/universities"
              className="inline-block px-6 py-2 bg-gradient-to-r from-blue-500 to-cyan-500 text-white rounded-lg hover:shadow-lg hover:shadow-blue-500/30 transition font-medium"
            >
               Explore Universities
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
