export interface Message {
  id: string
  type: 'user' | 'bot'
  content: string
  timestamp: Date
  colleges?: College[]
  isLoading?: boolean
}

export interface College {
  college_id: number
  college_name: string
  state: string
  city: string
  ownership?: string
  tier?: string
  nirf_rank?: number
  overall_score?: number
  average_fees?: number
  has_hostel?: boolean
  has_library?: boolean
  has_gym?: boolean
  courses?: Course[]
}

export interface Course {
  course_id: number
  course_name: string
  course_category: string
  duration_years?: number
}

export interface NLPQueryResponse {
  query: string
  intent: string
  sub_intent: string
  entities: {
    colleges: string[]
    courses: string[]
    cities: string[]
    states: string[]
    budget: number | null
    tier: string | null
    nirf_rank: { min: number; max: number } | null
    facilities: string[]
    ownership: string | null
  }
  api_params: Record<string, any>
  suggested_endpoint: string
  confidence: number
  friendly_message: string
}

export interface SearchResponse {
  total: number
  page: number
  page_size: number
  total_pages: number
  results: College[]
}

export interface CollegeDetailResponse extends College {
  facilities?: {
    has_hostel: boolean
    has_library: boolean
    has_gym: boolean
    has_sports_complex: boolean
    has_cafeteria: boolean
    has_medical_facilities: boolean
  }
  courses?: Course[]
}
