# College Recommendation System - Backend API

A FastAPI-based REST API for searching, comparing, and getting personalized recommendations for engineering colleges in India.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 15+
- Database: `college_recommendation` (already set up)

### Installation

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
# Copy .env.example to .env (already done)
# Edit .env if needed to change database credentials
```

4. **Run the server:**
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

5. **Access the API:**
- **Swagger Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **API Root:** http://localhost:8000/

---

## 📚 API Endpoints

### 1. **Search Colleges** `GET /api/colleges/search`

Search and filter colleges with pagination.

**Query Parameters:**
- `query` (string): Search text (college name, city, state)
- `state` (string): Filter by state
- `city` (string): Filter by city
- `tier` (string): Filter by tier (Tier 1, Tier 2, Tier 3)
- `ownership` (string): Filter by ownership (Government, Private, etc.)
- `min_nirf_rank` (int): Minimum NIRF rank
- `max_nirf_rank` (int): Maximum NIRF rank
- `min_score` (float): Minimum overall score (0-100)
- `max_score` (float): Maximum overall score (0-100)
- `has_hostel` (bool): Filter by hostel availability
- `has_gym` (bool): Filter by gym availability
- `has_library` (bool): Filter by library availability
- `page` (int): Page number (default: 1)
- `page_size` (int): Results per page (default: 20, max: 100)

**Example:**
```bash
curl "http://localhost:8000/api/colleges/search?state=Karnataka&tier=Tier%201&page=1&page_size=10"
```

**Response:**
```json
{
  "total": 150,
  "page": 1,
  "page_size": 10,
  "total_pages": 15,
  "results": [
    {
      "college_id": 1,
      "college_name": "IIT Madras",
      "state": "Tamil Nadu",
      "city": "Chennai",
      "tier": "Tier 1",
      "nirf_rank": 1,
      "overall_score": 95.5,
      ...
    }
  ]
}
```

---

### 2. **Get College Details** `GET /api/colleges/{college_id}`

Get complete information about a specific college.

**Example:**
```bash
curl "http://localhost:8000/api/colleges/1"
```

**Response:**
```json
{
  "college_id": 1,
  "college_name": "IIT Madras",
  "state": "Tamil Nadu",
  "city": "Chennai",
  "facilities": {
    "hostel": true,
    "library": true,
    "gym": true,
    "sports": true,
    ...
  },
  "courses": [
    {
      "course_id": 1,
      "course_name": "B.Tech Computer Science",
      "fee_per_year": 200000,
      "course_category": "Computer Science & IT"
    }
  ],
  ...
}
```

---

### 3. **Compare Colleges** `POST /api/colleges/compare`

Compare 2-4 colleges side-by-side.

**Request Body:**
```json
{
  "college_ids": [1, 2, 3]
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/colleges/compare" \
  -H "Content-Type: application/json" \
  -d '{"college_ids": [1, 2, 3]}'
```

**Response:**
```json
{
  "colleges": [
    {
      "college_id": 1,
      "college_name": "IIT Madras",
      "overall_score": 95.5,
      "facilities": {...},
      "courses": [...]
    },
    {
      "college_id": 2,
      "college_name": "IIT Delhi",
      "overall_score": 94.8,
      "facilities": {...},
      "courses": [...]
    }
  ]
}
```

---

### 4. **Get Recommendations** `POST /api/colleges/recommendations`

Get personalized college recommendations.

**Request Body:**
```json
{
  "budget": 200000,
  "preferred_states": ["Karnataka", "Tamil Nadu"],
  "preferred_cities": ["Bangalore", "Chennai"],
  "course_category": "Computer Science",
  "required_facilities": ["hostel", "gym"],
  "min_nirf_rank": 50,
  "tier_preference": "Tier 1",
  "limit": 10
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/colleges/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 200000,
    "preferred_states": ["Karnataka"],
    "course_category": "Computer Science",
    "limit": 5
  }'
```

**Response:**
```json
{
  "total": 5,
  "recommendations": [
    {
      "college_id": 10,
      "college_name": "PES University",
      "state": "Karnataka",
      "overall_score": 88.5,
      "facilities": {...},
      "courses": [...]
    }
  ],
  "filters_applied": {
    "budget": 200000,
    "states": ["Karnataka"],
    "course_category": "Computer Science"
  }
}
```

---

### 5. **Get Statistics** `GET /api/colleges/stats/overview`

Get overall database statistics.

**Example:**
```bash
curl "http://localhost:8000/api/colleges/stats/overview"
```

**Response:**
```json
{
  "total_colleges": 2619,
  "total_courses": 2781,
  "total_facilities": 180,
  "colleges_by_tier": {
    "Tier 1": 250,
    "Tier 2": 800,
    "Tier 3": 1500
  },
  "avg_overall_score": 72.5,
  "nirf_ranked_colleges": 189
}
```

---

## 🗂️ Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration
├── .env.example           # Example environment file
└── app/
    ├── __init__.py
    ├── api/
    │   ├── __init__.py
    │   └── colleges.py    # College endpoints
    ├── core/
    │   ├── __init__.py
    │   ├── config.py      # Settings and configuration
    │   └── database.py    # Database connection
    ├── models/
    │   ├── __init__.py
    │   └── models.py      # SQLAlchemy models
    └── schemas/
        ├── __init__.py
        └── schemas.py     # Pydantic schemas
```

---

## 🔧 Configuration

Edit `backend/.env` to configure:

```env
# Database
DATABASE_URL=postgresql://postgres:Ayush@123@localhost:5432/college_recommendation

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 🧪 Testing the API

### Using Swagger UI (Recommended)
1. Start the server: `python main.py`
2. Open: http://localhost:8000/docs
3. Try out endpoints interactively

### Using curl

**Search for CS colleges in Karnataka:**
```bash
curl "http://localhost:8000/api/colleges/search?state=Karnataka&query=Computer"
```

**Get college details:**
```bash
curl "http://localhost:8000/api/colleges/1"
```

**Get recommendations:**
```bash
curl -X POST "http://localhost:8000/api/colleges/recommendations" \
  -H "Content-Type: application/json" \
  -d '{"budget": 300000, "preferred_states": ["Tamil Nadu"], "limit": 5}'
```

---

## 📊 Database Schema

The API uses the following tables:
- **colleges** (2,619 records) - Main college data
- **college_facilities** (180 records) - Facility information
- **courses** (2,781 records) - Course offerings
- **course_features** - Course features (empty, for future use)

---

## 🚀 Features

✅ **Search with Fuzzy Matching** - Finds colleges even with typos  
✅ **Advanced Filtering** - Location, tier, NIRF rank, facilities, scores  
✅ **Side-by-Side Comparison** - Compare up to 4 colleges  
✅ **Personalized Recommendations** - Based on budget, location, preferences  
✅ **Pagination Support** - Handles large result sets efficiently  
✅ **Comprehensive Statistics** - Database overview and insights  
✅ **Interactive Documentation** - Swagger UI and ReDoc  
✅ **CORS Enabled** - Ready for frontend integration  

---

## 📝 Next Steps

1. **Test all endpoints** using Swagger UI
2. **Integrate with frontend** (React/Next.js)
3. **Add NLP layer** for chatbot queries
4. **Implement caching** (Redis) for better performance
5. **Add authentication** (JWT) if needed

---

## 🐛 Troubleshooting

**Database connection error:**
- Verify PostgreSQL is running
- Check credentials in `.env`
- Ensure `college_recommendation` database exists

**Import errors:**
- Install dependencies: `pip install -r requirements.txt`
- Verify Python version: `python --version` (3.8+)

**Port already in use:**
- Change `API_PORT` in `.env`
- Or kill process: `netstat -ano | findstr :8000`

---

**API is ready! 🎉**

Access the documentation at: http://localhost:8000/docs
