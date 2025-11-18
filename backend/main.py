"""
FastAPI Application Entry Point
College Recommendation System Backend API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.colleges import router as colleges_router

# Create FastAPI application
app = FastAPI(
    title="College Recommendation System API",
    description="""
    A comprehensive API for searching, comparing, and getting recommendations for engineering colleges in India.
    
    **Features:**
    - 🔍 Search 2,619 colleges with advanced filters
    - 📚 Browse 2,781 courses across 13 categories
    - ⚖️ Compare up to 4 colleges side-by-side
    - 🎯 Get personalized recommendations based on budget, location, and preferences
    - 📊 View detailed college profiles with facilities, courses, and rankings
    
    **Data Coverage:**
    - 2,619 engineering colleges across India
    - 189 NIRF-ranked colleges (including all top 50)
    - 1,477 Computer Science courses
    - 180 colleges with detailed facility information
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(colleges_router)


@app.get("/")
def root():
    """
    Root endpoint - API health check.
    """
    return {
        "message": "College Recommendation System API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "endpoints": {
            "search": "/api/colleges/search",
            "details": "/api/colleges/{college_id}",
            "compare": "/api/colleges/compare",
            "recommendations": "/api/colleges/recommendations",
            "statistics": "/api/colleges/stats/overview"
        }
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
