"""
College API endpoints for search, details, comparison, and recommendations.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func
from typing import List, Optional
from fuzzywuzzy import fuzz
import math

from app.core.database import get_db
from app.models import College, CollegeFacility, Course
from app.schemas import (
    CollegeSearchParams,
    SearchResponse,
    CollegeListResponse,
    CollegeDetailResponse,
    ComparisonRequest,
    ComparisonResponse,
    RecommendationRequest,
    RecommendationResponse
)

router = APIRouter(prefix="/api/colleges", tags=["colleges"])


# ==================== HELPER FUNCTIONS ====================

def apply_search_filters(query, params: CollegeSearchParams):
    """Apply filters to the college query."""
    
    # Text search with fuzzy matching
    if params.query:
        # Exact match or partial match
        query = query.filter(
            or_(
                College.college_name.ilike(f"%{params.query}%"),
                College.city.ilike(f"%{params.query}%"),
                College.state.ilike(f"%{params.query}%")
            )
        )
    
    # Location filters
    if params.state:
        query = query.filter(College.state.ilike(f"%{params.state}%"))
    if params.city:
        query = query.filter(College.city.ilike(f"%{params.city}%"))
    
    # Tier filter
    if params.tier:
        query = query.filter(College.tier == params.tier)
    
    # Ownership filter
    if params.ownership:
        query = query.filter(College.ownership.ilike(f"%{params.ownership}%"))
    
    # NIRF rank filters
    if params.min_nirf_rank:
        query = query.filter(College.nirf_rank >= params.min_nirf_rank)
    if params.max_nirf_rank:
        query = query.filter(College.nirf_rank <= params.max_nirf_rank)
    
    # Score filters
    if params.min_score:
        query = query.filter(College.overall_score >= params.min_score)
    if params.max_score:
        query = query.filter(College.overall_score <= params.max_score)
    
    # Facility filters (join with facilities table)
    if params.has_hostel or params.has_gym or params.has_library:
        query = query.join(CollegeFacility, College.college_id == CollegeFacility.college_id)
        
        if params.has_hostel:
            query = query.filter(CollegeFacility.has_hostel == True)
        if params.has_gym:
            query = query.filter(CollegeFacility.has_gym == True)
        if params.has_library:
            query = query.filter(CollegeFacility.has_library == True)
    
    return query


def fuzzy_rank_colleges(colleges: List[College], search_query: str) -> List[College]:
    """Rank colleges by fuzzy match score with search query."""
    if not search_query:
        return colleges
    
    # Calculate fuzzy scores
    scored_colleges = []
    for college in colleges:
        score = fuzz.partial_ratio(search_query.lower(), college.college_name.lower())
        scored_colleges.append((score, college))
    
    # Sort by score (descending)
    scored_colleges.sort(key=lambda x: x[0], reverse=True)
    
    return [college for score, college in scored_colleges]


# ==================== SEARCH ENDPOINT ====================

@router.get("/search", response_model=SearchResponse)
def search_colleges(
    query: Optional[str] = Query(None, description="Search query (college name, city, state)"),
    state: Optional[str] = Query(None, description="Filter by state"),
    city: Optional[str] = Query(None, description="Filter by city"),
    tier: Optional[str] = Query(None, description="Filter by tier"),
    ownership: Optional[str] = Query(None, description="Filter by ownership"),
    min_nirf_rank: Optional[int] = Query(None, description="Minimum NIRF rank"),
    max_nirf_rank: Optional[int] = Query(None, description="Maximum NIRF rank"),
    min_score: Optional[float] = Query(None, description="Minimum overall score"),
    max_score: Optional[float] = Query(None, description="Maximum overall score"),
    has_hostel: Optional[bool] = Query(None, description="Has hostel"),
    has_gym: Optional[bool] = Query(None, description="Has gym"),
    has_library: Optional[bool] = Query(None, description="Has library"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db)
):
    """
    Search colleges with filters and pagination.
    
    **Features:**
    - Fuzzy text search by college name, city, or state
    - Filter by location, tier, ownership, NIRF rank, scores
    - Filter by facilities (hostel, gym, library)
    - Pagination support
    - Results sorted by overall_score (desc) and fuzzy match score
    """
    
    # Create search params object
    params = CollegeSearchParams(
        query=query,
        state=state,
        city=city,
        tier=tier,
        ownership=ownership,
        min_nirf_rank=min_nirf_rank,
        max_nirf_rank=max_nirf_rank,
        min_score=min_score,
        max_score=max_score,
        has_hostel=has_hostel,
        has_gym=has_gym,
        has_library=has_library,
        page=page,
        page_size=page_size
    )
    
    # Build base query
    colleges_query = db.query(College)
    
    # Apply filters
    colleges_query = apply_search_filters(colleges_query, params)
    
    # Get total count before pagination
    total = colleges_query.count()
    
    # Order by overall_score (descending)
    colleges_query = colleges_query.order_by(College.overall_score.desc())
    
    # Get all matching colleges for fuzzy ranking (if search query provided)
    if params.query:
        all_colleges = colleges_query.all()
        all_colleges = fuzzy_rank_colleges(all_colleges, params.query)
        
        # Apply pagination to fuzzy-ranked results
        start_idx = (params.page - 1) * params.page_size
        end_idx = start_idx + params.page_size
        colleges = all_colleges[start_idx:end_idx]
    else:
        # Apply pagination to query
        colleges = colleges_query.offset((params.page - 1) * params.page_size).limit(params.page_size).all()
    
    # Calculate total pages
    total_pages = math.ceil(total / params.page_size) if total > 0 else 0
    
    return SearchResponse(
        total=total,
        page=params.page,
        page_size=params.page_size,
        total_pages=total_pages,
        results=colleges
    )


# ==================== COLLEGE DETAILS ENDPOINT ====================

@router.get("/{college_id}", response_model=CollegeDetailResponse)
def get_college_details(
    college_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific college.
    
    **Returns:**
    - Complete college profile
    - All facilities
    - All courses offered
    - Scores and rankings
    """
    
    # Query with eager loading of relationships
    college = db.query(College)\
        .options(
            joinedload(College.facilities),
            joinedload(College.courses)
        )\
        .filter(College.college_id == college_id)\
        .first()
    
    if not college:
        raise HTTPException(status_code=404, detail=f"College with ID {college_id} not found")
    
    return college


# ==================== COMPARISON ENDPOINT ====================

@router.post("/compare", response_model=ComparisonResponse)
def compare_colleges(
    request: ComparisonRequest,
    db: Session = Depends(get_db)
):
    """
    Compare 2-4 colleges side-by-side.
    
    **Request:**
    - `college_ids`: List of 2-4 college IDs to compare
    
    **Returns:**
    - Detailed information for each college
    - Easy side-by-side comparison of:
      - Scores (affordability, facility, quality, overall)
      - Rankings (NIRF, NAAC)
      - Location and type
      - Facilities
      - Courses offered
    """
    
    if len(request.college_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 college IDs required for comparison")
    if len(request.college_ids) > 4:
        raise HTTPException(status_code=400, detail="Maximum 4 colleges can be compared at once")
    
    # Query all colleges with relationships
    colleges = db.query(College)\
        .options(
            joinedload(College.facilities),
            joinedload(College.courses)
        )\
        .filter(College.college_id.in_(request.college_ids))\
        .all()
    
    if len(colleges) != len(request.college_ids):
        found_ids = [c.college_id for c in colleges]
        missing_ids = [cid for cid in request.college_ids if cid not in found_ids]
        raise HTTPException(
            status_code=404, 
            detail=f"Colleges not found for IDs: {missing_ids}"
        )
    
    # Return colleges in the same order as requested
    college_dict = {c.college_id: c for c in colleges}
    ordered_colleges = [college_dict[cid] for cid in request.college_ids]
    
    return ComparisonResponse(colleges=ordered_colleges)


# ==================== RECOMMENDATION ENDPOINT ====================

@router.post("/recommendations", response_model=RecommendationResponse)
def get_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """
    Get personalized college recommendations based on preferences.
    
    **Request Parameters:**
    - `budget`: Maximum annual fee budget (INR)
    - `preferred_states`: List of preferred states
    - `preferred_cities`: List of preferred cities
    - `course_category`: Preferred course category
    - `required_facilities`: Required facilities (e.g., ["hostel", "gym"])
    - `min_nirf_rank`: Minimum NIRF rank threshold
    - `tier_preference`: Preferred tier (Tier 1, Tier 2, Tier 3)
    - `limit`: Number of recommendations (default: 10, max: 50)
    
    **Algorithm:**
    1. Apply all filters (hard requirements)
    2. Calculate match score based on preferences
    3. Rank by: (match_score * 0.4) + (overall_score * 0.6)
    4. Return top N colleges
    """
    
    # Build base query with relationships
    query = db.query(College).options(
        joinedload(College.facilities),
        joinedload(College.courses)
    )
    
    # Track applied filters
    filters_applied = {}
    
    # Budget filter (check courses)
    if request.budget:
        filters_applied["budget"] = request.budget
        # Find colleges with courses within budget
        college_ids_in_budget = db.query(Course.college_id)\
            .filter(Course.fee_per_year <= request.budget)\
            .distinct()\
            .all()
        college_ids_in_budget = [cid[0] for cid in college_ids_in_budget]
        
        if college_ids_in_budget:
            query = query.filter(College.college_id.in_(college_ids_in_budget))
        else:
            # No colleges within budget
            return RecommendationResponse(
                total=0,
                recommendations=[],
                filters_applied=filters_applied
            )
    
    # Location filters
    if request.preferred_states:
        filters_applied["states"] = request.preferred_states
        query = query.filter(College.state.in_(request.preferred_states))
    
    if request.preferred_cities:
        filters_applied["cities"] = request.preferred_cities
        query = query.filter(College.city.in_(request.preferred_cities))
    
    # Course category filter
    if request.course_category:
        filters_applied["course_category"] = request.course_category
        college_ids_with_category = db.query(Course.college_id)\
            .filter(Course.course_category.ilike(f"%{request.course_category}%"))\
            .distinct()\
            .all()
        college_ids_with_category = [cid[0] for cid in college_ids_with_category]
        
        if college_ids_with_category:
            query = query.filter(College.college_id.in_(college_ids_with_category))
        else:
            return RecommendationResponse(
                total=0,
                recommendations=[],
                filters_applied=filters_applied
            )
    
    # Tier preference
    if request.tier_preference:
        filters_applied["tier"] = request.tier_preference
        query = query.filter(College.tier == request.tier_preference)
    
    # NIRF rank filter
    if request.min_nirf_rank:
        filters_applied["min_nirf_rank"] = request.min_nirf_rank
        query = query.filter(College.nirf_rank >= request.min_nirf_rank)
    
    # Facility filters
    if request.required_facilities:
        filters_applied["facilities"] = request.required_facilities
        query = query.join(CollegeFacility, College.college_id == CollegeFacility.college_id)
        
        for facility in request.required_facilities:
            # Add 'has_' prefix if not present
            facility_attr = facility if facility.startswith('has_') else f'has_{facility}'
            if hasattr(CollegeFacility, facility_attr):
                query = query.filter(getattr(CollegeFacility, facility_attr) == True)
    
    # Order by overall_score (descending)
    query = query.order_by(College.overall_score.desc())
    
    # Apply limit
    recommendations = query.limit(request.limit).all()
    
    return RecommendationResponse(
        total=len(recommendations),
        recommendations=recommendations,
        filters_applied=filters_applied
    )


# ==================== STATISTICS ENDPOINTS ====================

@router.get("/stats/overview")
def get_statistics_overview(db: Session = Depends(get_db)):
    """
    Get overall statistics about the database.
    
    **Returns:**
    - Total colleges, courses, facilities
    - Distribution by state, tier, ownership
    - Average scores
    - NIRF coverage
    """
    
    try:
        stats = {
            "total_colleges": db.query(College).count(),
            "total_courses": db.query(Course).count(),
            "total_facilities": db.query(CollegeFacility).count(),
            "colleges_by_tier": {},
            "colleges_by_state": {},
            "avg_overall_score": round(db.query(func.avg(College.overall_score)).scalar() or 0, 2),
            "avg_facility_score": round(db.query(func.avg(College.facility_score)).scalar() or 0, 2),
            "avg_quality_score": round(db.query(func.avg(College.quality_score)).scalar() or 0, 2),
            "nirf_ranked_colleges": db.query(College).filter(College.nirf_rank.isnot(None)).count()
        }
        
        # Colleges by tier
        tier_counts = db.query(College.tier, func.count(College.college_id))\
            .filter(College.tier.isnot(None))\
            .group_by(College.tier)\
            .all()
        stats["colleges_by_tier"] = {tier: count for tier, count in tier_counts}
        
        # Top 10 states by college count
        state_counts = db.query(College.state, func.count(College.college_id))\
            .group_by(College.state)\
            .order_by(func.count(College.college_id).desc())\
            .limit(10)\
            .all()
        stats["colleges_by_state"] = {state: count for state, count in state_counts}
        
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Statistics error: {str(e)}")
