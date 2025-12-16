"""
NLP Router
API endpoints for natural language query processing
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from ..nlp.query_processor import QueryProcessor

router = APIRouter(prefix="/api/nlp", tags=["NLP"])

# Initialize query processor
query_processor = QueryProcessor()


class QueryRequest(BaseModel):
    """Request model for NLP query."""
    query: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Find CS colleges in Karnataka under 2 lakhs"
            }
        }


class QueryResponse(BaseModel):
    """Response model for NLP query processing."""
    query: str
    intent: str
    sub_intent: str
    entities: Dict[str, Any]
    api_params: Dict[str, Any]
    suggested_endpoint: str
    confidence: float
    friendly_message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Find CS colleges in Karnataka under 2 lakhs",
                "intent": "search",
                "sub_intent": "search_cs",
                "entities": {
                    "courses": ["Computer Science"],
                    "states": ["Karnataka"],
                    "budget": 200000
                },
                "api_params": {
                    "state": "Karnataka",
                    "course_category": "Computer Science",
                    "max_fee": 200000
                },
                "suggested_endpoint": "/api/colleges/search",
                "confidence": 0.85,
                "friendly_message": "Searching for colleges in Karnataka for Computer Science under ₹2.0 lakhs..."
            }
        }


@router.post("/query", response_model=QueryResponse)
async def process_natural_language_query(request: QueryRequest):
    """
    Process a natural language query and return structured parameters.
    
    This endpoint uses NLP to understand the user's intent and extract
    relevant entities like college names, locations, courses, budget, etc.
    It then converts these into API parameters that can be used with other endpoints.
    
    Args:
        request: QueryRequest containing the natural language query
        
    Returns:
        QueryResponse with:
        - intent: Main intent (search, compare, recommend, info, greeting)
        - sub_intent: Specific sub-intent
        - entities: Extracted entities (colleges, cities, courses, budget, etc.)
        - api_params: Parameters ready for API calls
        - suggested_endpoint: Which endpoint to call next
        - confidence: Confidence score (0-1)
        - friendly_message: Human-readable response
        
    Example:
        POST /api/nlp/query
        {
            "query": "Show me top 10 IITs with good placement"
        }
        
        Response:
        {
            "intent": "search",
            "sub_intent": "search_placement",
            "entities": {
                "colleges": ["IIT"],
                "nirf_rank": {"min": 1, "max": 10}
            },
            "api_params": {
                "q": "IIT",
                "nirf_rank_max": 10
            },
            "suggested_endpoint": "/api/colleges/search",
            "confidence": 0.9,
            "friendly_message": "Searching for colleges..."
        }
    """
    try:
        # Process the query
        result = query_processor.process(request.query)
        
        # Generate friendly message
        friendly_message = query_processor.get_friendly_response(result)
        
        return QueryResponse(
            query=request.query,
            intent=result['intent'],
            sub_intent=result['sub_intent'],
            entities=result['entities'],
            api_params=result['api_params'],
            suggested_endpoint=result['suggested_endpoint'] or 'none',
            confidence=result['confidence'],
            friendly_message=friendly_message
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.get("/examples")
async def get_query_examples():
    """
    Get example queries that demonstrate NLP capabilities.
    
    Returns a list of example queries with their expected outputs.
    """
    examples = [
        {
            "query": "Find CS colleges in Karnataka under 2 lakhs",
            "intent": "search",
            "description": "Search for colleges with filters"
        },
        {
            "query": "Compare IIT Bombay and IIT Delhi",
            "intent": "compare",
            "description": "Compare specific colleges"
        },
        {
            "query": "Recommend me top engineering colleges",
            "intent": "recommend",
            "description": "Get personalized recommendations"
        },
        {
            "query": "Tell me about NIT Trichy fees and placements",
            "intent": "info",
            "description": "Get detailed college information"
        },
        {
            "query": "What are the best colleges for mechanical engineering?",
            "intent": "search",
            "description": "Search by specific branch"
        },
        {
            "query": "Show me government colleges in Tamil Nadu",
            "intent": "search",
            "description": "Filter by ownership and location"
        },
        {
            "query": "I want affordable colleges with hostel facilities",
            "intent": "search",
            "description": "Search with tier and facility filters"
        },
        {
            "query": "Which IITs are in the top 10 NIRF ranking?",
            "intent": "search",
            "description": "Filter by NIRF rank and college name"
        },
        {
            "query": "Compare top 3 colleges in Bangalore for CS",
            "intent": "search",
            "description": "Location and course-based search"
        },
        {
            "query": "Suggest me colleges for ECE under 3 lakhs in Mumbai",
            "intent": "recommend",
            "description": "Recommendation with multiple filters"
        }
    ]
    
    return {
        "examples": examples,
        "supported_intents": [
            "search - Find colleges based on criteria",
            "compare - Compare multiple colleges",
            "recommend - Get personalized recommendations",
            "info - Get detailed information about a college",
            "greeting - Conversational greeting"
        ],
        "supported_entities": [
            "college names (IIT, NIT, IIIT, etc.)",
            "cities (Bangalore, Mumbai, Delhi, etc.)",
            "states (Karnataka, Maharashtra, Tamil Nadu, etc.)",
            "courses (CS, ECE, Mechanical, Civil, etc.)",
            "budget (in lakhs or rupees)",
            "tier (Tier 1, Tier 2, Budget-Friendly, etc.)",
            "NIRF rank (top X, within top X)",
            "facilities (hostel, library, gym, sports, etc.)",
            "ownership (Government, Private)"
        ]
    }


@router.get("/health")
async def nlp_health_check():
    """Check if NLP services are working properly."""
    try:
        # Test with a simple query
        test_result = query_processor.process("Hello")
        
        return {
            "status": "healthy",
            "message": "NLP services are operational",
            "components": {
                "intent_classifier": "operational",
                "entity_extractor": "operational",
                "query_processor": "operational"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"NLP services error: {str(e)}",
            "components": {
                "intent_classifier": "unknown",
                "entity_extractor": "unknown",
                "query_processor": "error"
            }
        }
