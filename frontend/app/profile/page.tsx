'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { profileAPI, onboardingAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store';

interface UserProfile {
  id: number;
  user_id: number;
  email?: string;
  full_name?: string;
  onboarding_completed: boolean;
  current_stage: string;
  current_education_level?: string;
  degree_major?: string;
  graduation_year?: number;
  gpa_percentage?: number;
  intended_degree?: string;
  field_of_study?: string;
  target_intake_year?: number;
  preferred_countries: string | string[];
  budget_min?: number;
  budget_max?: number;
  funding_plan?: string;
  ielts_toefl_status?: string;
  ielts_toefl_score?: number;
  gre_gmat_status?: string;
  gre_gmat_score?: number;
  sop_status?: string;
  academic_strength?: string;
  exam_strength?: string;
  overall_strength?: string;
}

interface FormData {
  current_education_level: string;
  degree_major: string;
  graduation_year: number;
  gpa_percentage: string;
  intended_degree: string;
  field_of_study: string;
  target_intake_year: number;
  preferred_countries: string[];
  budget_min: string;
  budget_max: string;
  funding_plan: string;
  ielts_toefl_status: string;
  ielts_toefl_score: string;
  gre_gmat_status: string;
  gre_gmat_score: string;
  sop_status: string;
}

export default function ProfilePage() {
  const router = useRouter();
  const { isAuthenticated, logout, user } = useAuthStore();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [editedProfile, setEditedProfile] = useState<Partial<UserProfile>>({});
  const [selectedCountries, setSelectedCountries] = useState<string[]>([]);
  
  // For first-time form
  const [step, setStep] = useState(1);
  const [formSubmitting, setFormSubmitting] = useState(false);
  const [formError, setFormError] = useState('');
  const [formData, setFormData] = useState<FormData>({
    current_education_level: '',
    degree_major: '',
    graduation_year: new Date().getFullYear(),
    gpa_percentage: '',
    intended_degree: '',
    field_of_study: '',
    target_intake_year: new Date().getFullYear() + 1,
    preferred_countries: [],
    budget_min: '',
    budget_max: '',
    funding_plan: '',
    ielts_toefl_status: 'NOT_STARTED',
    ielts_toefl_score: '',
    gre_gmat_status: 'NOT_STARTED',
    gre_gmat_score: '',
    sop_status: 'NOT_STARTED',
  });
  
  const availableCountries = [
    'USA', 'UK', 'Canada', 'Australia', 'Germany', 'France', 
    'Netherlands', 'Sweden', 'Singapore', 'Japan', 'South Korea',
    'Switzerland', 'New Zealand', 'Ireland', 'Italy', 'Spain'
  ];

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/auth/login');
      return;
    }
    loadProfile();
  }, [isAuthenticated]);

  const loadProfile = async () => {
    try {
      const res = await profileAPI.get();
      const profileData = res.data;
      
      // Parse preferred_countries if it's a string
      if (typeof profileData.preferred_countries === 'string') {
        try {
          profileData.preferred_countries = JSON.parse(profileData.preferred_countries);
        } catch {
          profileData.preferred_countries = [];
        }
      }
      
      setProfile(profileData);
      setSelectedCountries(profileData.preferred_countries || []);
      
      // If first time, populate form with existing data
      if (!profileData.onboarding_completed) {
        setFormData(prev => ({
          ...prev,
          current_education_level: profileData.current_education_level || '',
          degree_major: profileData.degree_major || '',
          graduation_year: profileData.graduation_year || new Date().getFullYear(),
          gpa_percentage: profileData.gpa_percentage ? String(profileData.gpa_percentage) : '',
          intended_degree: profileData.intended_degree || '',
          field_of_study: profileData.field_of_study || '',
          target_intake_year: profileData.target_intake_year || new Date().getFullYear() + 1,
          preferred_countries: profileData.preferred_countries || [],
          budget_min: profileData.budget_min ? String(profileData.budget_min) : '',
          budget_max: profileData.budget_max ? String(profileData.budget_max) : '',
          funding_plan: profileData.funding_plan || '',
          ielts_toefl_status: profileData.ielts_toefl_status || 'NOT_STARTED',
          ielts_toefl_score: profileData.ielts_toefl_score ? String(profileData.ielts_toefl_score) : '',
          gre_gmat_status: profileData.gre_gmat_status || 'NOT_STARTED',
          gre_gmat_score: profileData.gre_gmat_score ? String(profileData.gre_gmat_score) : '',
          sop_status: profileData.sop_status || 'NOT_STARTED',
        }));
        setFormData(prev => ({
          ...prev,
          preferred_countries: Array.isArray(profileData.preferred_countries) ? profileData.preferred_countries : [],
        }));
      }
    } catch (error) {
      console.error('Failed to load profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
    setEditedProfile(profile || {});
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditedProfile({});
    setSelectedCountries(profile?.preferred_countries as string[] || []);
  };

  const handleCountryToggle = (country: string) => {
    setSelectedCountries(prev => 
      prev.includes(country)
        ? prev.filter(c => c !== country)
        : [...prev, country]
    );
  };

  // Form submission for first-time profile
  const handleFormSubmit = async () => {
    setFormError('');
    setFormSubmitting(true);

    try {
      const submitData = {
        ...formData,
        preferred_countries: formData.preferred_countries,
        gpa_percentage: formData.gpa_percentage ? parseFloat(formData.gpa_percentage) : null,
        ielts_toefl_score: formData.ielts_toefl_score ? parseFloat(formData.ielts_toefl_score) : null,
        gre_gmat_score: formData.gre_gmat_score ? parseFloat(formData.gre_gmat_score) : null,
        budget_min: formData.budget_min ? parseFloat(formData.budget_min) : null,
        budget_max: formData.budget_max ? parseFloat(formData.budget_max) : null,
      };

      await onboardingAPI.complete(submitData);
      // Reload to get updated profile with onboarding_completed = true
      await loadProfile();
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail;
      if (Array.isArray(errorMsg)) {
        const messages = errorMsg.map((e: any) => e.msg).join(', ');
        setFormError(messages || 'Validation failed');
      } else if (typeof errorMsg === 'string') {
        setFormError(errorMsg);
      } else {
        setFormError('Failed to update profile');
      }
    } finally {
      setFormSubmitting(false);
    }
  };

  const nextStep = () => {
    if (step < 4) setStep(step + 1);
  };

  const prevStep = () => {
    if (step > 1) setStep(step - 1);
  };

  const handleSave = async () => {
    try {
      const updateData = {
        ...editedProfile,
        preferred_countries: selectedCountries
      };
      
      await profileAPI.update(updateData);
      alert('Profile updated successfully!');
      setIsEditing(false);
      loadProfile();
    } catch (error: any) {
      console.error('Failed to update profile:', error);
      alert(error.response?.data?.detail || 'Failed to update profile');
    }
  };

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  return (
    <>
      {/* If first time (onboarding not completed), show form */}
      {!loading && profile && !profile.onboarding_completed && (
        <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-blue-950 py-12 px-4">
          <div className="max-w-3xl mx-auto">
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 shadow-2xl">
              {/* Progress Bar */}
              <div className="mb-8">
                <div className="flex justify-between items-center mb-4">
                  {[1, 2, 3, 4].map((s) => (
                    <div
                      key={s}
                      className={`flex-1 h-2 mx-1 rounded ${
                        s <= step ? 'bg-gradient-to-r from-cyan-400 to-blue-500' : 'bg-white/10'
                      }`}
                    />
                  ))}
                </div>
                <p className="text-sm text-gray-400 text-center">
                  Step {step} of 4
                </p>
              </div>

              {formError && (
                <div className="mb-4 bg-red-500/20 border border-red-500/50 text-red-200 px-4 py-3 rounded-lg">
                  {formError}
                </div>
              )}

              {/* Step 1: Academic Background */}
              {step === 1 && (
                <div className="space-y-6">
                  <h2 className="text-2xl font-bold mb-6 text-white">Academic Background</h2>

                  <div>
                    <label className="block text-sm font-medium mb-2 text-gray-300">
                      Current Education Level
                    </label>
                    <select
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 transition"
                      value={formData.current_education_level}
                      onChange={(e) =>
                        setFormData({ ...formData, current_education_level: e.target.value })
                      }
                      required
                    >
                      <option value="" className="bg-slate-900 text-white">Select...</option>
                      <option value="High School" className="bg-slate-900 text-white">High School</option>
                      <option value="Bachelor's" className="bg-slate-900 text-white">Bachelor's</option>
                      <option value="Master's" className="bg-slate-900 text-white">Master's</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2 text-gray-300">
                      Degree / Major
                    </label>
                    <input
                      type="text"
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 transition"
                      value={formData.degree_major}
                      onChange={(e) =>
                        setFormData({ ...formData, degree_major: e.target.value })
                      }
                      required
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-2 text-gray-300">
                        Graduation Year
                      </label>
                      <input
                        type="number"
                        className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 transition"
                        value={formData.graduation_year}
                        onChange={(e) =>
                          setFormData({ ...formData, graduation_year: parseInt(e.target.value) })
                        }
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-2 text-gray-300">
                        GPA (out of 4.0)
                      </label>
                      <input
                        type="number"
                        step="0.01"
                        className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 transition"
                        value={formData.gpa_percentage}
                        onChange={(e) =>
                          setFormData({ ...formData, gpa_percentage: e.target.value })
                        }
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Step 2: Study Goals */}
              {step === 2 && (
                <div className="space-y-6">
                  <h2 className="text-2xl font-bold mb-6 text-white">Study Goals</h2>

                  <div>
                    <label className="block text-sm font-medium mb-2 text-gray-300">
                      Intended Degree
                    </label>
                    <select
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 transition"
                      value={formData.intended_degree}
                      onChange={(e) =>
                        setFormData({ ...formData, intended_degree: e.target.value })
                      }
                      required
                    >
                      <option value="" className="bg-slate-900 text-white">Select...</option>
                      <option value="Bachelor's" className="bg-slate-900 text-white">Bachelor's</option>
                      <option value="Master's" className="bg-slate-900 text-white">Master's</option>
                      <option value="MBA" className="bg-slate-900 text-white">MBA</option>
                      <option value="PhD" className="bg-slate-900 text-white">PhD</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2 text-gray-300">
                      Field of Study
                    </label>
                    <input
                      type="text"
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 transition"
                      value={formData.field_of_study}
                      onChange={(e) =>
                        setFormData({ ...formData, field_of_study: e.target.value })
                      }
                      placeholder="e.g., Computer Science, Business Analytics"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2 text-gray-300">
                      Target Intake Year
                    </label>
                    <input
                      type="number"
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 transition"
                      value={formData.target_intake_year}
                      onChange={(e) =>
                        setFormData({ ...formData, target_intake_year: parseInt(e.target.value) })
                      }
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2 text-gray-300">
                      Preferred Countries
                    </label>
                    <div className="grid grid-cols-3 gap-2">
                      {availableCountries.map((country) => (
                        <button
                          key={country}
                          type="button"
                          onClick={() => {
                            setFormData({
                              ...formData,
                              preferred_countries: formData.preferred_countries.includes(country)
                                ? formData.preferred_countries.filter((c) => c !== country)
                                : [...formData.preferred_countries, country],
                            });
                          }}
                          className={`px-3 py-2 rounded-lg text-sm font-medium transition ${
                            formData.preferred_countries.includes(country)
                              ? 'bg-gradient-to-r from-cyan-400 to-blue-500 text-white'
                              : 'bg-white/10 border border-white/20 text-gray-300 hover:bg-white/20'
                          }`}
                        >
                          {formData.preferred_countries.includes(country) && ' '}
                          {country}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Step 3: Budget & Funding */}
              {step === 3 && (
                <div className="space-y-6">
                  <h2 className="text-2xl font-bold mb-6 text-white">Budget & Funding</h2>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-2 text-gray-300">
                        Minimum Budget (USD)
                      </label>
                      <input
                        type="number"
                        className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 transition"
                        value={formData.budget_min}
                        onChange={(e) =>
                          setFormData({ ...formData, budget_min: e.target.value })
                        }
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-2 text-gray-300">
                        Maximum Budget (USD)
                      </label>
                      <input
                        type="number"
                        className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 transition"
                        value={formData.budget_max}
                        onChange={(e) =>
                          setFormData({ ...formData, budget_max: e.target.value })
                        }
                        required
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2 text-gray-300">
                      Funding Plan
                    </label>
                    <select
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 transition"
                      value={formData.funding_plan}
                      onChange={(e) =>
                        setFormData({ ...formData, funding_plan: e.target.value })
                      }
                      required
                    >
                      <option value="" className="bg-slate-900 text-white">Select...</option>
                      <option value="SELF_FUNDED" className="bg-slate-900 text-white">Self Funded</option>
                      <option value="SCHOLARSHIP_DEPENDENT" className="bg-slate-900 text-white">Scholarship Dependent</option>
                      <option value="LOAN_DEPENDENT" className="bg-slate-900 text-white">Loan Dependent</option>
                    </select>
                  </div>
                </div>
              )}

              {/* Step 4: Exams */}
              {step === 4 && (
                <div className="space-y-6">
                  <h2 className="text-2xl font-bold mb-6 text-white">English & Entrance Exams</h2>

                  <div>
                    <label className="block text-sm font-medium mb-2 text-gray-300">
                      IELTS/TOEFL Status
                    </label>
                    <select
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 transition"
                      value={formData.ielts_toefl_status}
                      onChange={(e) =>
                        setFormData({ ...formData, ielts_toefl_status: e.target.value })
                      }
                    >
                      <option value="NOT_STARTED" className="bg-slate-900 text-white">Not Started</option>
                      <option value="SCHEDULED" className="bg-slate-900 text-white">Scheduled</option>
                      <option value="COMPLETED" className="bg-slate-900 text-white">Completed</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2 text-gray-300">
                      IELTS/TOEFL Score
                    </label>
                    <input
                      type="number"
                      step="0.5"
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 transition"
                      value={formData.ielts_toefl_score}
                      onChange={(e) =>
                        setFormData({ ...formData, ielts_toefl_score: e.target.value })
                      }
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2 text-gray-300">
                      GRE/GMAT Status
                    </label>
                    <select
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 transition"
                      value={formData.gre_gmat_status}
                      onChange={(e) =>
                        setFormData({ ...formData, gre_gmat_status: e.target.value })
                      }
                    >
                      <option value="NOT_STARTED" className="bg-slate-900 text-white">Not Started</option>
                      <option value="SCHEDULED" className="bg-slate-900 text-white">Scheduled</option>
                      <option value="COMPLETED" className="bg-slate-900 text-white">Completed</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2 text-gray-300">
                      GRE/GMAT Score
                    </label>
                    <input
                      type="number"
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 transition"
                      value={formData.gre_gmat_score}
                      onChange={(e) =>
                        setFormData({ ...formData, gre_gmat_score: e.target.value })
                      }
                    />
                  </div>
                </div>
              )}

              {/* Buttons */}
              <div className="flex justify-between mt-8">
                <button
                  onClick={prevStep}
                  className={`px-6 py-3 rounded-lg font-medium transition ${
                    step === 1
                      ? 'bg-white/10 text-gray-500 cursor-not-allowed border border-white/20'
                      : 'bg-white/10 border border-white/20 text-gray-300 hover:bg-white/20'
                  }`}
                  disabled={step === 1}
                >
                  Previous
                </button>

                {step === 4 ? (
                  <button
                    onClick={handleFormSubmit}
                    disabled={formSubmitting}
                    className={`px-8 py-3 rounded-lg font-medium text-white transition ${
                      formSubmitting
                        ? 'bg-gray-500 cursor-not-allowed'
                        : 'bg-gradient-to-r from-cyan-400 to-blue-500 hover:shadow-lg hover:shadow-cyan-500/50'
                    }`}
                  >
                    {formSubmitting ? 'Completing...' : 'Complete Profile'}
                  </button>
                ) : (
                  <button
                    onClick={nextStep}
                    className="px-8 py-3 rounded-lg font-medium bg-gradient-to-r from-cyan-400 to-blue-500 text-white hover:shadow-lg hover:shadow-cyan-500/50 transition"
                  >
                    Next
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Regular profile page (after onboarding completed) */}
      {!loading && profile && profile.onboarding_completed && (
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

      {/* Logout - Fixed Right Top */}
      <div className="fixed right-6 top-6 z-30 flex items-center space-x-3">
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
              <Link href="/dashboard" className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-white/10 transition">
                Dashboard
              </Link>
              <Link href="/universities" className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-white/10 transition">
                Universities
              </Link>
              <Link href="/counselor" className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-white/10 transition">
                AI Counselor
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pt-24">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
            My Profile
          </h1>
          {!isEditing ? (
            <button
              onClick={handleEdit}
              className="px-6 py-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:shadow-lg hover:shadow-blue-500/50 transition font-medium"
            >
              Edit Profile
            </button>
          ) : (
            <div className="flex gap-3">
              <button
                onClick={handleCancel}
                className="px-6 py-2 bg-white/10 border border-white/20 text-white rounded-lg hover:bg-white/20 transition font-medium"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="px-6 py-2 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:shadow-lg hover:shadow-green-500/50 transition font-medium"
              >
                Save Changes
              </button>
            </div>
          )}
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-white/10 border border-white/20 animate-spin">
              <div className="w-12 h-12 rounded-full border-4 border-white/10 border-t-cyan-400"></div>
            </div>
          </div>
        ) : !profile ? (
          <div className="bg-white/10 backdrop-blur-md border border-white/20 p-8 rounded-lg text-center">
            <p className="text-gray-400">Failed to load profile</p>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Basic Info */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 p-6 rounded-xl">
              <h2 className="text-xl font-bold text-white mb-6"> Basic Information</h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Email</label>
                  <p className="text-white font-medium">{user?.email || 'Not provided'}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Full Name</label>
                  <p className="text-white font-medium">{user?.full_name || 'Not provided'}</p>
                </div>
              </div>
            </div>

            {/* Academic Background */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 p-6 rounded-xl">
              <h2 className="text-xl font-bold text-white mb-6"> Academic Background</h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">
                    Current Education Level
                  </label>
                  <p className="text-white font-medium">
                    {profile.current_education_level || 'Not provided'}
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Degree Major</label>
                  <p className="text-white font-medium">{profile.degree_major || 'Not provided'}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Graduation Year</label>
                  <p className="text-white font-medium">{profile.graduation_year || 'Not provided'}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">GPA / Percentage</label>
                  <p className="text-white font-medium">
                    {profile.gpa_percentage ? `${profile.gpa_percentage}/4.0` : 'Not provided'}
                  </p>
                </div>
              </div>
            </div>

            {/* Study Goals */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 p-6 rounded-xl">
              <h2 className="text-xl font-bold text-white mb-6"> Study Goals</h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Intended Degree</label>
                  <p className="text-white font-medium">{profile.intended_degree || 'Not provided'}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Field of Study</label>
                  <p className="text-white font-medium">{profile.field_of_study || 'Not provided'}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Target Intake Year</label>
                  <p className="text-white font-medium">{profile.target_intake_year || 'Not provided'}</p>
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-400 mb-3">
                     Preferred Countries {isEditing && <span className="text-cyan-300 text-xs">(Click to select/deselect)</span>}
                  </label>
                  {isEditing ? (
                    <div className="grid grid-cols-3 gap-2">
                      {availableCountries.map(country => (
                        <button
                          key={country}
                          type="button"
                          onClick={() => handleCountryToggle(country)}
                          className={`px-3 py-2 rounded-lg text-sm font-medium transition ${
                            selectedCountries.includes(country)
                              ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white'
                              : 'bg-white/10 border border-white/20 text-gray-300 hover:bg-white/20'
                          }`}
                        >
                          {selectedCountries.includes(country) && ' '}
                          {country}
                        </button>
                      ))}
                    </div>
                  ) : (
                    <p className="text-white font-medium">
                      {Array.isArray(profile.preferred_countries) && profile.preferred_countries.length > 0
                        ? profile.preferred_countries.join(', ')
                        : 'Not provided'}
                    </p>
                  )}
                </div>
              </div>
            </div>

            {/* Exam Scores */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 p-6 rounded-xl">
              <h2 className="text-xl font-bold text-white mb-6"> Exam Scores</h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">IELTS/TOEFL Status</label>
                  <p className="text-white font-medium">
                    {profile.ielts_toefl_status?.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) || 'Not Started'}
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">IELTS/TOEFL Score</label>
                  <p className="text-white font-medium">
                    {profile.ielts_toefl_score || 'N/A'}
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">GRE/GMAT Status</label>
                  <p className="text-white font-medium">
                    {profile.gre_gmat_status?.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) || 'Not Started'}
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">GRE/GMAT Score</label>
                  <p className="text-white font-medium">
                    {profile.gre_gmat_score || 'N/A'}
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">SOP Status</label>
                  <p className="text-white font-medium">
                    {profile.sop_status?.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) || 'Not Started'}
                  </p>
                </div>
              </div>
            </div>

            {/* Budget & Funding */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 p-6 rounded-xl">
              <h2 className="text-xl font-bold text-white mb-6"> Budget & Funding</h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Budget Range</label>
                  <p className="text-white font-medium">
                    {profile.budget_min && profile.budget_max
                      ? `$${profile.budget_min.toLocaleString()} - $${profile.budget_max.toLocaleString()}`
                      : 'Not provided'}
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Funding Plan</label>
                  <p className="text-white font-medium">
                    {profile.funding_plan?.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) || 'Not provided'}
                  </p>
                </div>
              </div>
            </div>

            {/* Profile Strength */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 p-6 rounded-xl">
              <h2 className="text-xl font-bold text-white mb-6">⭐ Profile Strength (AI-Generated)</h2>
              <div className="grid md:grid-cols-3 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-3"> Academic</label>
                  <span className={`px-3 py-2 rounded-lg text-sm font-semibold inline-block ${
                    profile.academic_strength === 'STRONG' ? 'bg-green-500/30 border border-green-400/50 text-green-300' :
                    profile.academic_strength === 'AVERAGE' ? 'bg-yellow-500/30 border border-yellow-400/50 text-yellow-300' :
                    'bg-red-500/30 border border-red-400/50 text-red-300'
                  }`}>
                    {profile.academic_strength || 'N/A'}
                  </span>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-3"> Exams</label>
                  <span className={`px-3 py-2 rounded-lg text-sm font-semibold inline-block ${
                    profile.exam_strength === 'STRONG' ? 'bg-green-500/30 border border-green-400/50 text-green-300' :
                    profile.exam_strength === 'AVERAGE' ? 'bg-yellow-500/30 border border-yellow-400/50 text-yellow-300' :
                    'bg-red-500/30 border border-red-400/50 text-red-300'
                  }`}>
                    {profile.exam_strength || 'N/A'}
                  </span>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-3"> Overall</label>
                  <span className={`px-3 py-2 rounded-lg text-sm font-semibold inline-block ${
                    profile.overall_strength === 'STRONG' ? 'bg-green-500/30 border border-green-400/50 text-green-300' :
                    profile.overall_strength === 'AVERAGE' ? 'bg-yellow-500/30 border border-yellow-400/50 text-yellow-300' :
                    'bg-red-500/30 border border-red-400/50 text-red-300'
                  }`}>
                    {profile.overall_strength || 'N/A'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
        </div>
      )}

      {/* Loading state */}
      {loading && (
        <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-blue-950 flex items-center justify-center">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 mb-4 rounded-full bg-white/10 border border-white/20 animate-spin">
              <div className="w-12 h-12 rounded-full border-4 border-white/10 border-t-cyan-400"></div>
            </div>
            <p className="text-xl text-gray-400">Loading...</p>
          </div>
        </div>
      )}
    </>
  );
}
