'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { onboardingAPI, dashboardAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store';

export default function OnboardingPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Check if user has already completed onboarding on mount
  useEffect(() => {
    const checkOnboardingStatus = async () => {
      if (!isAuthenticated) {
        // Not logged in, redirect to login
        router.push('/auth/login');
        return;
      }

      try {
        const response = await dashboardAPI.get();
        if (response.data.profile.onboarding_completed) {
          // User already completed onboarding, redirect to dashboard
          router.push('/dashboard');
        }
      } catch (err) {
        // If error getting dashboard, continue showing onboarding form
        console.log('Could not fetch dashboard, showing onboarding form');
      }
    };

    checkOnboardingStatus();
  }, [isAuthenticated, router]);

  const [formData, setFormData] = useState({
    // Academic Background
    current_education_level: '',
    degree_major: '',
    graduation_year: new Date().getFullYear(),
    gpa_percentage: '',
    
    // Study Goal
    intended_degree: '',
    field_of_study: '',
    target_intake_year: new Date().getFullYear() + 1,
    preferred_countries: [] as string[],
    
    // Budget
    budget_min: '',
    budget_max: '',
    funding_plan: '',
    
    // Exams
    ielts_toefl_status: 'NOT_STARTED',
    ielts_toefl_score: '',
    gre_gmat_status: 'NOT_STARTED',
    gre_gmat_score: '',
    sop_status: 'NOT_STARTED',
  });

  const handleCountryToggle = (country: string) => {
    if (formData.preferred_countries.includes(country)) {
      setFormData({
        ...formData,
        preferred_countries: formData.preferred_countries.filter((c) => c !== country),
      });
    } else {
      setFormData({
        ...formData,
        preferred_countries: [...formData.preferred_countries, country],
      });
    }
  };

  const handleSubmit = async () => {
    setError('');
    setLoading(true);

    try {
      const submitData = {
        ...formData,
        gpa_percentage: formData.gpa_percentage ? parseFloat(formData.gpa_percentage) : null,
        ielts_toefl_score: formData.ielts_toefl_score ? parseFloat(formData.ielts_toefl_score) : null,
        gre_gmat_score: formData.gre_gmat_score ? parseFloat(formData.gre_gmat_score) : null,
        budget_min: parseFloat(formData.budget_min),
        budget_max: parseFloat(formData.budget_max),
      };

      await onboardingAPI.complete(submitData);
      router.push('/dashboard');
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail;
      if (Array.isArray(errorMsg)) {
        // Pydantic validation errors
        const messages = errorMsg.map((e: any) => e.msg).join(', ');
        setError(messages || 'Validation failed');
      } else if (typeof errorMsg === 'string') {
        setError(errorMsg);
      } else {
        setError('Failed to complete onboarding');
      }
    } finally {
      setLoading(false);
    }
  };

  const nextStep = () => {
    if (step < 4) setStep(step + 1);
  };

  const prevStep = () => {
    if (step > 1) setStep(step - 1);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {/* Progress Bar */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              {[1, 2, 3, 4].map((s) => (
                <div
                  key={s}
                  className={`flex-1 h-2 mx-1 rounded ${
                    s <= step ? 'bg-blue-600' : 'bg-gray-200'
                  }`}
                />
              ))}
            </div>
            <p className="text-sm text-gray-600 text-center">
              Step {step} of 4
            </p>
          </div>

          {error && (
            <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          {/* Step 1: Academic Background */}
          {step === 1 && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold mb-6 text-gray-900">Academic Background</h2>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-900">
                  Current Education Level
                </label>
                <select
                  className="w-full px-4 py-3 border rounded-lg text-gray-900"
                  value={formData.current_education_level}
                  onChange={(e) =>
                    setFormData({ ...formData, current_education_level: e.target.value })
                  }
                  required
                >
                  <option value="">Select...</option>
                  <option value="High School">High School</option>
                  <option value="Bachelor's">Bachelor's</option>
                  <option value="Master's">Master's</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-900">
                  Degree / Major
                </label>
                <input
                  type="text"
                  className="w-full px-4 py-3 border rounded-lg text-gray-900"
                  value={formData.degree_major}
                  onChange={(e) =>
                    setFormData({ ...formData, degree_major: e.target.value })
                  }
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-900">
                    Graduation Year
                  </label>
                  <input
                    type="number"
                    className="w-full px-4 py-3 border rounded-lg text-gray-900"
                    value={formData.graduation_year}
                    onChange={(e) =>
                      setFormData({ ...formData, graduation_year: parseInt(e.target.value) })
                    }
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-900">
                    GPA (out of 4.0)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    className="w-full px-4 py-3 border rounded-lg text-gray-900"
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
              <h2 className="text-2xl font-bold mb-6 text-gray-900">Study Goals</h2>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-900">
                  Intended Degree
                </label>
                <select
                  className="w-full px-4 py-3 border rounded-lg text-gray-900"
                  value={formData.intended_degree}
                  onChange={(e) =>
                    setFormData({ ...formData, intended_degree: e.target.value })
                  }
                  required
                >
                  <option value="">Select...</option>
                  <option value="Bachelor's">Bachelor's</option>
                  <option value="Master's">Master's</option>
                  <option value="MBA">MBA</option>
                  <option value="PhD">PhD</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-900">
                  Field of Study
                </label>
                <input
                  type="text"
                  className="w-full px-4 py-3 border rounded-lg text-gray-900"
                  value={formData.field_of_study}
                  onChange={(e) =>
                    setFormData({ ...formData, field_of_study: e.target.value })
                  }
                  placeholder="e.g., Computer Science, Business Analytics"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-900">
                  Target Intake Year
                </label>
                <input
                  type="number"
                  className="w-full px-4 py-3 border rounded-lg text-gray-900"
                  value={formData.target_intake_year}
                  onChange={(e) =>
                    setFormData({ ...formData, target_intake_year: parseInt(e.target.value) })
                  }
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-900">
                  Preferred Countries
                </label>
                <div className="grid grid-cols-2 gap-3 mt-2">
                  {['USA', 'UK', 'Canada', 'Germany', 'Australia', 'Netherlands'].map(
                    (country) => (
                      <button
                        key={country}
                        type="button"
                        onClick={() => handleCountryToggle(country)}
                        className={`px-4 py-2 rounded-lg border-2 transition ${
                          formData.preferred_countries.includes(country)
                            ? 'bg-blue-600 text-white border-blue-600'
                            : 'bg-white text-gray-700 border-gray-300 hover:border-blue-400'
                        }`}
                      >
                        {country}
                      </button>
                    )
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Step 3: Budget */}
          {step === 3 && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold mb-6 text-gray-900">Budget & Funding</h2>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-900">
                    Min Budget (per year in USD)
                  </label>
                  <input
                    type="number"
                    className="w-full px-4 py-3 border rounded-lg text-gray-900"
                    value={formData.budget_min}
                    onChange={(e) =>
                      setFormData({ ...formData, budget_min: e.target.value })
                    }
                    placeholder="e.g., 20000"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-900">
                    Max Budget (per year in USD)
                  </label>
                  <input
                    type="number"
                    className="w-full px-4 py-3 border rounded-lg text-gray-900"
                    value={formData.budget_max}
                    onChange={(e) =>
                      setFormData({ ...formData, budget_max: e.target.value })
                    }
                    placeholder="e.g., 50000"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-900">
                  Funding Plan
                </label>
                <select
                  className="w-full px-4 py-3 border rounded-lg text-gray-900"
                  value={formData.funding_plan}
                  onChange={(e) =>
                    setFormData({ ...formData, funding_plan: e.target.value })
                  }
                  required
                >
                  <option value="">Select...</option>
                  <option value="SELF_FUNDED">Self-Funded</option>
                  <option value="SCHOLARSHIP_DEPENDENT">Scholarship Dependent</option>
                  <option value="LOAN_DEPENDENT">Loan Dependent</option>
                </select>
              </div>
            </div>
          )}

          {/* Step 4: Exams & Readiness */}
          {step === 4 && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold mb-6 text-gray-900">Exams & Readiness</h2>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-900">
                  IELTS / TOEFL Status
                </label>
                <select
                  className="w-full px-4 py-3 border rounded-lg mb-2 text-gray-900"
                  value={formData.ielts_toefl_status}
                  onChange={(e) =>
                    setFormData({ ...formData, ielts_toefl_status: e.target.value })
                  }
                >
                  <option value="NOT_STARTED">Not Started</option>
                  <option value="IN_PROGRESS">In Progress</option>
                  <option value="COMPLETED">Completed</option>
                </select>
                {formData.ielts_toefl_status === 'COMPLETED' && (
                  <input
                    type="number"
                    step="0.5"
                    className="w-full px-4 py-3 border rounded-lg text-gray-900"
                    placeholder="Score (e.g., 7.5)"
                    value={formData.ielts_toefl_score}
                    onChange={(e) =>
                      setFormData({ ...formData, ielts_toefl_score: e.target.value })
                    }
                  />
                )}
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-900">
                  GRE / GMAT Status
                </label>
                <select
                  className="w-full px-4 py-3 border rounded-lg mb-2 text-gray-900"
                  value={formData.gre_gmat_status}
                  onChange={(e) =>
                    setFormData({ ...formData, gre_gmat_status: e.target.value })
                  }
                >
                  <option value="NOT_STARTED">Not Started</option>
                  <option value="IN_PROGRESS">In Progress</option>
                  <option value="COMPLETED">Completed</option>
                </select>
                {formData.gre_gmat_status === 'COMPLETED' && (
                  <input
                    type="number"
                    className="w-full px-4 py-3 border rounded-lg text-gray-900"
                    placeholder="Score (e.g., 320)"
                    value={formData.gre_gmat_score}
                    onChange={(e) =>
                      setFormData({ ...formData, gre_gmat_score: e.target.value })
                    }
                  />
                )}
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-900">
                  SOP Status
                </label>
                <select
                  className="w-full px-4 py-3 border rounded-lg text-gray-900"
                  value={formData.sop_status}
                  onChange={(e) =>
                    setFormData({ ...formData, sop_status: e.target.value })
                  }
                >
                  <option value="NOT_STARTED">Not Started</option>
                  <option value="IN_PROGRESS">Draft</option>
                  <option value="COMPLETED">Ready</option>
                </select>
              </div>
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="mt-8 flex justify-between">
            <button
              onClick={prevStep}
              disabled={step === 1}
              className="px-6 py-3 bg-gray-200 text-gray-900 rounded-lg font-semibold disabled:opacity-50"
            >
              Previous
            </button>

            {step < 4 ? (
              <button
                onClick={nextStep}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700"
              >
                Next
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="px-6 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 disabled:bg-gray-400"
              >
                {loading ? 'Completing...' : 'Complete Onboarding'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
