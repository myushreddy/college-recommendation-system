"""
Pydantic schemas for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ============= FACILITY SCHEMAS =============

class FacilitySchema(BaseModel):
    """Schema for college facilities."""
    has_hostel: bool = False
    has_library: bool = False
    has_sports: bool = False
    has_gym: bool = False
    has_cafeteria: bool = False
    has_medical: bool = False
    has_wifi: bool = False
    has_lab: bool = False
    has_auditorium: bool = False
    has_transport: bool = False
    facilities_text: Optional[str] = None
    
    class Config:
        from_attributes = True


# ============= COURSE SCHEMAS =============

class CourseBase(BaseModel):
    """Base course schema."""
    course_name: str
    degree_type: Optional[str] = None
    duration_years: Optional[int] = None
    fee_per_year: Optional[float] = None
    total_fee: Optional[float] = None
    course_category: Optional[str] = None


class CourseResponse(CourseBase):
    """Response schema for courses."""
    course_id: int
    college_id: int
    is_cs_related: bool = False
    is_electronics: bool = False
    is_mechanical: bool = False
    is_civil: bool = False
    is_chemical: bool = False
    is_aerospace: bool = False
    is_ai_ml: bool = False
    
    class Config:
        from_attributes = True


# ============= COLLEGE SCHEMAS =============

class CollegeBase(BaseModel):
    """Base college schema."""
    college_name: str
    state: str
    city: str
    ownership: Optional[str] = None
    college_type: Optional[str] = None
    nirf_rank: Optional[int] = None
    naac_grade: Optional[str] = None
    naac_score: Optional[float] = None
    tier: Optional[str] = None
    website: Optional[str] = None


class CollegeListResponse(CollegeBase):
    """Response schema for college list (search results)."""
    college_id: int
    affordability_score: Optional[float] = None
    facility_score: Optional[float] = None
    quality_score: Optional[float] = None
    overall_score: Optional[float] = None
    
    class Config:
        from_attributes = True


class CollegeDetailResponse(CollegeBase):
    """Response schema for detailed college information."""
    college_id: int
    affordability_score: Optional[float] = None
    facility_score: Optional[float] = None
    quality_score: Optional[float] = None
    overall_score: Optional[float] = None
    facilities: Optional[FacilitySchema] = None
    courses: List[CourseResponse] = []
    
    class Config:
        from_attributes = True


# ============= SEARCH SCHEMAS =============

class CollegeSearchParams(BaseModel):
    """Parameters for college search."""
    query: Optional[str] = Field(None, description="Search query (college name, partial match)")
    state: Optional[str] = Field(None, description="Filter by state")
    city: Optional[str] = Field(None, description="Filter by city")
    tier: Optional[str] = Field(None, description="Filter by tier (Tier 1, Tier 2, Tier 3)")
    ownership: Optional[str] = Field(None, description="Filter by ownership (Government, Private, etc.)")
    min_nirf_rank: Optional[int] = Field(None, description="Minimum NIRF rank")
    max_nirf_rank: Optional[int] = Field(None, description="Maximum NIRF rank")
    min_score: Optional[float] = Field(None, description="Minimum overall score (0-100)")
    max_score: Optional[float] = Field(None, description="Maximum overall score (0-100)")
    has_hostel: Optional[bool] = Field(None, description="Filter by hostel availability")
    has_gym: Optional[bool] = Field(None, description="Filter by gym availability")
    has_library: Optional[bool] = Field(None, description="Filter by library availability")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Results per page")


class SearchResponse(BaseModel):
    """Response schema for search results."""
    total: int
    page: int
    page_size: int
    total_pages: int
    results: List[CollegeListResponse]


# ============= COMPARISON SCHEMAS =============

class ComparisonRequest(BaseModel):
    """Request schema for college comparison."""
    college_ids: List[int] = Field(..., min_length=2, max_length=4, description="2-4 college IDs to compare")


class ComparisonResponse(BaseModel):
    """Response schema for college comparison."""
    colleges: List[CollegeDetailResponse]


# ============= RECOMMENDATION SCHEMAS =============

class RecommendationRequest(BaseModel):
    """Request schema for personalized recommendations."""
    budget: Optional[float] = Field(None, description="Maximum annual budget in INR")
    preferred_states: Optional[List[str]] = Field(None, description="Preferred states")
    preferred_cities: Optional[List[str]] = Field(None, description="Preferred cities")
    course_category: Optional[str] = Field(None, description="Preferred course category")
    required_facilities: Optional[List[str]] = Field(None, description="Required facilities (hostel, gym, etc.)")
    min_nirf_rank: Optional[int] = Field(None, description="Minimum NIRF rank threshold")
    tier_preference: Optional[str] = Field(None, description="Tier preference (Tier 1, Tier 2, Tier 3)")
    limit: int = Field(10, ge=1, le=50, description="Number of recommendations")


class RecommendationResponse(BaseModel):
    """Response schema for recommendations."""
    total: int
    recommendations: List[CollegeDetailResponse]
    filters_applied: dict


# ============= ERROR SCHEMAS =============

class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str
    error_code: Optional[str] = None
