"""
Comprehensive System Health Check
Tests all components of the College Recommendation System
"""
import sys
import requests
from sqlalchemy import text
from app.core.database import engine

def test_database():
    """Test database connection and data integrity."""
    print("\n" + "="*60)
    print("DATABASE HEALTH CHECK")
    print("="*60)
    
    try:
        with engine.connect() as conn:
            # Test college count
            result = conn.execute(text("SELECT COUNT(*) FROM colleges"))
            college_count = result.scalar()
            print(f"✅ Colleges table: {college_count} records")
            
            # Test courses count
            result = conn.execute(text("SELECT COUNT(*) FROM courses"))
            course_count = result.scalar()
            print(f"✅ Courses table: {course_count} records")
            
            # Test facilities count
            result = conn.execute(text("SELECT COUNT(*) FROM college_facilities"))
            facility_count = result.scalar()
            print(f"✅ Facilities table: {facility_count} records")
            
            # Test NIRF colleges
            result = conn.execute(text("SELECT COUNT(*) FROM colleges WHERE nirf_rank IS NOT NULL"))
            nirf_count = result.scalar()
            print(f"✅ NIRF ranked colleges: {nirf_count} records")
            
            return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False


def test_nlp_modules():
    """Test NLP module imports."""
    print("\n" + "="*60)
    print("NLP MODULES HEALTH CHECK")
    print("="*60)
    
    try:
        from app.nlp.intent_classifier import IntentClassifier
        print("✅ IntentClassifier imported")
        
        from app.nlp.entity_extractor import EntityExtractor
        print("✅ EntityExtractor imported")
        
        from app.nlp.query_processor import QueryProcessor
        print("✅ QueryProcessor imported")
        
        # Test spaCy
        import spacy
        nlp = spacy.load('en_core_web_sm')
        print(f"✅ spaCy model loaded: en_core_web_sm")
        
        return True
    except Exception as e:
        print(f"❌ NLP module error: {e}")
        return False


def test_nlp_functionality():
    """Test NLP processing functionality."""
    print("\n" + "="*60)
    print("NLP FUNCTIONALITY TEST")
    print("="*60)
    
    try:
        from app.nlp.query_processor import QueryProcessor
        processor = QueryProcessor()
        
        # Test query 1
        result = processor.process("Find CS colleges in Karnataka under 2 lakhs")
        print(f"✅ Query 1 processed: Intent={result['intent']}, Confidence={result['confidence']}")
        
        # Test query 2
        result = processor.process("Compare IIT Bombay and IIT Delhi")
        print(f"✅ Query 2 processed: Intent={result['intent']}, Confidence={result['confidence']}")
        
        # Test query 3
        result = processor.process("Recommend affordable colleges in Tamil Nadu")
        print(f"✅ Query 3 processed: Intent={result['intent']}, Confidence={result['confidence']}")
        
        return True
    except Exception as e:
        print(f"❌ NLP functionality error: {e}")
        return False


def test_api_endpoints():
    """Test API endpoints."""
    print("\n" + "="*60)
    print("API ENDPOINTS HEALTH CHECK")
    print("="*60)
    
    base_url = "http://localhost:8000"
    all_passed = True
    
    # Test 1: Root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint (GET /)")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        all_passed = False
    
    # Test 2: Health check
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check (GET /health)")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        all_passed = False
    
    # Test 3: Statistics
    try:
        response = requests.get(f"{base_url}/api/colleges/stats/overview", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Statistics endpoint: {data['total_colleges']} colleges")
        else:
            print(f"❌ Statistics endpoint failed: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"❌ Statistics endpoint error: {e}")
        all_passed = False
    
    # Test 4: Search
    try:
        response = requests.get(f"{base_url}/api/colleges/search?state=Karnataka&page_size=5", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search endpoint: {data['total']} results")
        else:
            print(f"❌ Search endpoint failed: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"❌ Search endpoint error: {e}")
        all_passed = False
    
    # Test 5: College details
    try:
        response = requests.get(f"{base_url}/api/colleges/5516", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ College details: {data['college_name']}")
        else:
            print(f"❌ College details failed: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"❌ College details error: {e}")
        all_passed = False
    
    # Test 6: Compare
    try:
        response = requests.post(
            f"{base_url}/api/colleges/compare",
            json={"college_ids": [5516, 5517]},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Compare endpoint")
        else:
            print(f"❌ Compare endpoint failed: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"❌ Compare endpoint error: {e}")
        all_passed = False
    
    # Test 7: Recommendations
    try:
        response = requests.post(
            f"{base_url}/api/colleges/recommendations",
            json={"preferred_state": "Karnataka", "max_fee": 200000},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Recommendations endpoint")
        else:
            print(f"❌ Recommendations endpoint failed: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"❌ Recommendations endpoint error: {e}")
        all_passed = False
    
    # Test 8: NLP health
    try:
        response = requests.get(f"{base_url}/api/nlp/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ NLP health: {data['status']}")
        else:
            print(f"❌ NLP health failed: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"❌ NLP health error: {e}")
        all_passed = False
    
    # Test 9: NLP query
    try:
        response = requests.post(
            f"{base_url}/api/nlp/query",
            json={"query": "Find CS colleges in Karnataka"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ NLP query: Intent={data['intent']}")
        else:
            print(f"❌ NLP query failed: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"❌ NLP query error: {e}")
        all_passed = False
    
    # Test 10: NLP examples
    try:
        response = requests.get(f"{base_url}/api/nlp/examples", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ NLP examples: {len(data['examples'])} examples")
        else:
            print(f"❌ NLP examples failed: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"❌ NLP examples error: {e}")
        all_passed = False
    
    return all_passed


def main():
    """Run all health checks."""
    print("\n" + "="*60)
    print("COLLEGE RECOMMENDATION SYSTEM - HEALTH CHECK")
    print("="*60)
    
    results = {
        'Database': test_database(),
        'NLP Modules': test_nlp_modules(),
        'NLP Functionality': test_nlp_functionality(),
        'API Endpoints': test_api_endpoints()
    }
    
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    
    for component, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {component}: {'PASSED' if status else 'FAILED'}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL SYSTEMS OPERATIONAL!")
    else:
        print("⚠️  SOME SYSTEMS NEED ATTENTION")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
