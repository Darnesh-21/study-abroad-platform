'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { authAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store';

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuthStore();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await authAPI.login(formData);
      
      // Get user data (you might want to add a /me endpoint)
      login({ id: 1, full_name: 'User', email: formData.email }, res.data.access_token);
      
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-blue-950 flex">
      {/* Left Side - Image/Visual */}
      <div className="hidden lg:flex lg:flex-1 relative overflow-hidden">
        {/* Background Image */}
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{ backgroundImage: "url('/background_images/library-869061_1920.jpg')" }}
        ></div>
        
        {/* Gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-900/70 to-cyan-900/70 z-10"></div>
        
        {/* Content */}
        <div className="relative z-20 flex flex-col justify-center px-12 xl:px-20 text-white">
          <h1 className="text-5xl xl:text-6xl font-bold mb-6 leading-tight">
            Welcome Back to<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-300 to-cyan-300">
              Your Journey
            </span>
          </h1>
          <p className="text-xl text-gray-300 mb-8 leading-relaxed">
            Continue where you left off. Your study abroad dreams are just a login away.
          </p>
          
          {/* Stats */}
          <div className="grid grid-cols-3 gap-6">
            {[
              { number: '10K+', label: 'Students' },
              { number: '500+', label: 'Universities' },
              { number: '95%', label: 'Success Rate' }
            ].map((stat, idx) => (
              <div key={idx} className="text-center">
                <div className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-300 to-cyan-300">
                  {stat.number}
                </div>
                <div className="text-sm text-gray-400 mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right Side - Form */}
      <div className="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-20 xl:px-32 relative">
        {/* Background gradient effects */}
        <div className="absolute inset-0 bg-gradient-to-br from-cyan-900/20 via-transparent to-blue-900/20"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
        
        <div className="w-full max-w-md relative z-10">
          {/* Logo/Brand */}
          <Link href="/" className="flex items-center space-x-2 mb-8">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-lg"></div>
            <span className="text-2xl font-bold text-white">StudyAbroad.AI</span>
          </Link>

          {/* Form Container */}
          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl">
            <div className="mb-8">
              <h2 className="text-4xl font-bold text-white mb-2">Welcome Back</h2>
              <p className="text-gray-400 text-lg">
                Login to continue your journey
              </p>
            </div>

            {error && (
              <div className="mb-6 bg-red-500/10 border border-red-500/50 text-red-400 px-4 py-3 rounded-lg backdrop-blur-sm">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  required
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white placeholder-gray-500 transition backdrop-blur-sm"
                  placeholder="your.email@example.com"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Password
                </label>
                <input
                  type="password"
                  required
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white placeholder-gray-500 transition backdrop-blur-sm"
                  placeholder="Enter your password"
                  value={formData.password}
                  onChange={(e) =>
                    setFormData({ ...formData, password: e.target.value })
                  }
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 text-white py-3 rounded-lg font-semibold hover:shadow-2xl hover:shadow-blue-500/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed mt-6"
              >
                {loading ? 'Logging in...' : 'Login'}
              </button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-gray-400">
                Don't have an account?{' '}
                <Link href="/auth/signup" className="text-blue-400 font-semibold hover:text-blue-300 transition">
                  Sign Up
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
