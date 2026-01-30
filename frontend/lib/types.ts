export interface User {
  id: number;
  full_name: string;
  email: string;
  created_at: string;
}

export interface UserProfile {
  id: number;
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
  preferred_countries?: string;
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

export interface University {
  id: number;
  name: string;
  country: string;
  city?: string;
  ranking?: number;
  acceptance_rate?: number;
  tuition_fee_min: number;
  tuition_fee_max: number;
  fields_offered: string[];
  programs: string[];
  requirements: {
    ielts?: number;
    gre?: number;
    gpa?: number;
  };
  description: string;
  website_url?: string;
}

export interface ShortlistedUniversity {
  id: number;
  university_id: number;
  category: string;
  is_locked: boolean;
  fit_reason?: string;
  risk_factors?: string;
  acceptance_chance?: string;
  cost_level?: string;
  created_at: string;
  locked_at?: string;
  university: University;
}

export interface TodoItem {
  id: number;
  title: string;
  description?: string;
  priority: string;
  category: string;
  is_completed: boolean;
  due_date?: string;
  ai_generated: boolean;
  created_at: string;
}

export interface ChatMessage {
  id: number;
  role: string;
  message: string;
  action_type?: string;
  action_metadata?: string;
  created_at: string;
}

export interface Dashboard {
  user: User;
  profile: UserProfile;
  todos: TodoItem[];
  shortlisted_universities: ShortlistedUniversity[];
  locked_universities_count: number;
  committed_universities?: Array<{
    shortlisted_university: ShortlistedUniversity;
    tasks: TodoItem[];
    documents: any[];
  }>;
}
