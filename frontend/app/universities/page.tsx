'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { universitiesAPI, profileAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store';

interface University {
  id: number;
  name: string;
  country: string;
  world_ranking?: number;
  tuition_fee_min?: number;
  tuition_fee_max?: number;
  application_fee?: number;
  acceptance_rate?: number;
  website?: string;
}

interface ShortlistedUniversity {
  id: number;
  university_id: number;
  category: string;
  is_locked: boolean;
  university: University;
}

export default function UniversitiesPage() {
  const router = useRouter();
  const { isAuthenticated, logout } = useAuthStore();
  const [universities, setUniversities] = useState<University[]>([]);
  const [shortlistedUniversities, setShortlistedUniversities] = useState<ShortlistedUniversity[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [countryFilter, setCountryFilter] = useState('');
  const [preferredCountries, setPreferredCountries] = useState<string[]>([]);
  const [showAllCountries, setShowAllCountries] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/auth/login');
      return;
    }
    loadProfileCountries();
    loadShortlisted();
  }, [isAuthenticated]);

  const loadProfileCountries = async () => {
    try {
      const res = await profileAPI.get();
      let countries: string[] = [];
      
      if (res.data.preferred_countries) {
        if (typeof res.data.preferred_countries === 'string') {
          try {
            countries = JSON.parse(res.data.preferred_countries);
          } catch {
            countries = [];
          }
        } else {
          countries = res.data.preferred_countries;
        }
      }
      
      setPreferredCountries(countries);
      
      // Load universities with country filter
      if (countries.length > 0 && !showAllCountries) {
        loadUniversitiesByCountries(countries);
      } else {
        loadUniversities();
      }
    } catch (error) {
      console.error('Failed to load profile:', error);
      loadUniversities(); // Fallback to all universities
    }
  };

  const loadUniversities = async () => {
    try {
      const res = await universitiesAPI.search({});
      setUniversities(res.data);
    } catch (error) {
      console.error('Failed to load universities:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadUniversitiesByCountries = async (countries: string[]) => {
    try {
      const res = await universitiesAPI.search({});
      // Filter universities by preferred countries
      const filtered = res.data.filter((uni: University) => 
        countries.includes(uni.country)
      );
      setUniversities(filtered);
    } catch (error) {
      console.error('Failed to load universities:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleAllCountries = () => {
    setShowAllCountries(!showAllCountries);
    setLoading(true);
    if (!showAllCountries) {
      loadUniversities();
    } else {
      loadUniversitiesByCountries(preferredCountries);
    }
  };

  const loadShortlisted = async () => {
    try {
      const res = await universitiesAPI.getShortlisted();
      setShortlistedUniversities(res.data);
    } catch (error) {
      console.error('Failed to load shortlisted universities:', error);
    }
  };

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  const handleShortlist = async (universityId: number, universityName: string) => {
    try {
      // Default to TARGET category
      await universitiesAPI.shortlist({ university_id: universityId, category: 'TARGET' });
      alert(`${universityName} has been shortlisted!`);
      loadShortlisted(); // Reload shortlisted universities
    } catch (error: any) {
      console.error('Failed to shortlist university:', error);
      alert(error.response?.data?.detail || 'Failed to shortlist university');
    }
  };

  const handleLock = async (universityId: number, universityName: string) => {
    const confirmed = confirm(
      ` Lock ${universityName}?\n\n` +
      `Locking a university shows your commitment and unlocks application-specific guidance.\n\n` +
      `This will:\n` +
      `• Move you to the "Preparing Applications" stage\n` +
      `• Generate tailored application tasks\n` +
      `• Enable application-specific AI guidance\n\n` +
      `You can unlock later if needed.`
    );

    if (!confirmed) return;

    try {
      await universitiesAPI.lock(universityId);
      
      // Reload shortlisted to get updated count
      await loadShortlisted();
      
      // Count locked universities
      const lockedCount = shortlistedUniversities.filter(u => u.is_locked).length + 1;
      
      if (lockedCount >= 3) {
        alert(
          ` ${universityName} has been locked.\n\n` +
          `You have locked 3 universities. You can now use the AI Counselor.`
        );
      } else {
        const remaining = 3 - lockedCount;
        alert(
          ` ${universityName} has been locked.\n\n` +
          `${lockedCount} / 3 universities locked.\n\n` +
          `Lock ${remaining} more ${remaining === 1 ? 'university' : 'universities'} to access the AI Counselor.`
        );
      }
    } catch (error: any) {
      console.error('Failed to lock university:', error);
      alert(error.response?.data?.detail || 'Failed to lock university');
    }
  };

  const handleUnlock = async (universityId: number, universityName: string) => {
    const confirmed = confirm(`Unlock ${universityName}? You can lock it again later.`);
    if (!confirmed) return;

    try {
      await universitiesAPI.unlock(universityId);
      alert(`${universityName} has been unlocked.`);
      loadShortlisted();
    } catch (error: any) {
      console.error('Failed to unlock university:', error);
      alert(error.response?.data?.detail || 'Failed to unlock university');
    }
  };

  const handleRemoveFromShortlist = async (universityId: number, universityName: string) => {
    const confirmed = confirm(`Remove ${universityName} from shortlist?`);
    if (!confirmed) return;

    try {
      await universitiesAPI.removeShortlist(universityId);
      alert(`${universityName} has been removed from shortlist.`);
      loadShortlisted();
    } catch (error: any) {
      console.error('Failed to remove from shortlist:', error);
      alert(error.response?.data?.detail || 'Failed to remove from shortlist');
    }
  };

  const isShortlisted = (universityId: number) => {
    return shortlistedUniversities.find(s => s.university_id === universityId);
  };

  const filteredUniversities = universities.filter((uni) => {
    const matchesSearch = uni.name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCountry = !countryFilter || uni.country === countryFilter;
    return matchesSearch && matchesCountry;
  });

  const countries = Array.from(new Set(universities.map((u) => u.country)));

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
                className="text-cyan-400 font-semibold px-3 py-2 rounded-lg bg-white/10"
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

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header Section */}
        <div className="mb-8">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-5xl font-bold text-white mb-2"> Discover Universities</h1>
              <p className="text-gray-300 text-lg">Find your perfect study destination</p>
            </div>
            {preferredCountries.length > 0 && (
              <button
                onClick={handleToggleAllCountries}
                className={`px-6 py-3 rounded-lg font-semibold transition transform hover:scale-105 ${
                  showAllCountries
                    ? 'bg-gradient-to-r from-orange-500 to-orange-600 text-white shadow-lg shadow-orange-500/50'
                    : 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg shadow-blue-500/50'
                }`}
              >
                {showAllCountries ? ' Show Preferred Regions' : ' Show All Countries'}
              </button>
            )}
          </div>

          {/* Filter Info Banner */}
          {preferredCountries.length > 0 && !showAllCountries && (
            <div className="bg-gradient-to-r from-blue-500/20 to-cyan-500/20 border border-blue-400/50 rounded-lg p-4 mb-6 backdrop-blur-sm">
              <p className="text-white">
                <span className="font-semibold"> Showing universities from your preferred regions:</span>
                <span className="ml-2 text-blue-200">{preferredCountries.join(', ')} • {universities.length} universities found</span>
              </p>
            </div>
          )}
        </div>

        {/* Search and Filter Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="md:col-span-2">
            <label className="block text-white font-semibold mb-2"> Search Universities</label>
            <input
              type="text"
              placeholder="Search by name..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            />
          </div>
          <div>
            <label className="block text-white font-semibold mb-2"> Filter by Country</label>
            <select
              value={countryFilter}
              onChange={(e) => setCountryFilter(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            >
              <option value="">All Countries</option>
              {countries.map((country) => (
                <option key={country} value={country}>
                  {country}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Universities Grid */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
              <p className="text-gray-400">Loading universities...</p>
            </div>
          </div>
        ) : filteredUniversities.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-400 text-lg">No universities found. Try adjusting your filters.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredUniversities.map((uni) => {
              const shortlisted = isShortlisted(uni.id);
              return (
                <div
                  key={uni.id}
                  className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 hover:border-blue-400/50 hover:bg-white/15 transition hover:shadow-lg hover:shadow-blue-500/10 transform hover:scale-[1.02]"
                >
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-2xl font-bold text-white">{uni.name}</h3>
                        {shortlisted && (
                          <span className="px-3 py-1 bg-green-500/30 border border-green-400/50 text-green-300 text-xs font-semibold rounded-full">
                             Shortlisted
                          </span>
                        )}
                        {shortlisted?.is_locked && (
                          <span className="px-3 py-1 bg-blue-500/30 border border-blue-400/50 text-blue-300 text-xs font-semibold rounded-full">
                             Locked
                          </span>
                        )}
                      </div>
                      <div className="flex items-center gap-4 flex-wrap mt-3">
                        <span className="text-cyan-300 font-semibold"> {uni.country}</span>
                        {uni.world_ranking && (
                          <span className="text-yellow-300 font-semibold"> Rank #{uni.world_ranking}</span>
                        )}
                        {uni.acceptance_rate && (
                          <span className="text-orange-300 font-semibold"> {uni.acceptance_rate}% Acceptance</span>
                        )}
                      </div>
                    </div>
                    <div className="text-right">
                      {uni.tuition_fee_min && uni.tuition_fee_max && (
                        <div>
                          <p className="text-2xl font-bold text-green-400">
                            ${uni.tuition_fee_min.toLocaleString()} - ${uni.tuition_fee_max.toLocaleString()}
                          </p>
                          <p className="text-sm text-gray-400">per year</p>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex gap-3 flex-wrap mt-6 pt-4 border-t border-white/10">
                    {uni.website && (
                      <a
                        href={uni.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-4 py-2 bg-white/10 hover:bg-white/20 text-blue-300 hover:text-blue-200 rounded-lg text-sm font-medium transition border border-white/20"
                      >
                         Visit Website
                      </a>
                    )}
                    {!shortlisted ? (
                      <button
                        onClick={() => handleShortlist(uni.id, uni.name)}
                        className="px-4 py-2 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg text-sm font-medium hover:shadow-lg hover:shadow-green-500/50 transition"
                      >
                        + Shortlist
                      </button>
                    ) : shortlisted.is_locked ? (
                      <>
                        <button
                          onClick={() => handleUnlock(uni.id, uni.name)}
                          className="px-4 py-2 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-lg text-sm font-medium hover:shadow-lg hover:shadow-orange-500/50 transition"
                        >
                           Unlock
                        </button>
                        <button
                          onClick={() => handleRemoveFromShortlist(uni.id, uni.name)}
                          className="px-4 py-2 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg text-sm font-medium hover:shadow-lg hover:shadow-red-500/50 transition"
                        >
                          × Remove
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          onClick={() => handleLock(uni.id, uni.name)}
                          className="px-4 py-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg text-sm font-medium hover:shadow-lg hover:shadow-blue-500/50 transition"
                        >
                           Lock University
                        </button>
                        <button
                          onClick={() => handleRemoveFromShortlist(uni.id, uni.name)}
                          className="px-4 py-2 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg text-sm font-medium hover:shadow-lg hover:shadow-red-500/50 transition"
                        >
                          × Remove
                        </button>
                      </>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
