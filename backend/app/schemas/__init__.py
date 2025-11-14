"""
Schemas package initialization.
"""
from app.schemas.schemas import (
    FacilitySchema,
    CourseBase,
    CourseResponse,
    CollegeBase,
    CollegeListResponse,
    CollegeDetailResponse,
    CollegeSearchParams,
    SearchResponse,
    ComparisonRequest,
    ComparisonResponse,
    RecommendationRequest,
    RecommendationResponse,
    ErrorResponse
)

__all__ = [
    "FacilitySchema",
    "CourseBase",
    "CourseResponse",
    "CollegeBase",
    "CollegeListResponse",
    "CollegeDetailResponse",
    "CollegeSearchParams",
    "SearchResponse",
    "ComparisonRequest",
    "ComparisonResponse",
    "RecommendationRequest",
    "RecommendationResponse",
    "ErrorResponse"
]
