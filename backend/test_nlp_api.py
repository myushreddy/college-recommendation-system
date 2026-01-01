"""
Test NLP API Endpoints
Tests the natural language query processing functionality
"""
import requests
import json


BASE_URL = "http://localhost:8000"


def test_nlp_health():
    """Test NLP health check."""
    print("\n1. Testing NLP Health Check...")
    response = requests.get(f"{BASE_URL}/api/nlp/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✅ PASSED")


def test_nlp_examples():
    """Test NLP examples endpoint."""
    print("\n2. Testing NLP Examples...")
    response = requests.get(f"{BASE_URL}/api/nlp/examples")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Number of examples: {len(data['examples'])}")
    print(f"Supported intents: {len(data['supported_intents'])}")
    print(f"Supported entities: {len(data['supported_entities'])}")
    assert response.status_code == 200
    print("✅ PASSED")


def test_simple_search_query():
    """Test simple search query."""
    print("\n3. Testing Simple Search Query...")
    query = "Find CS colleges in Karnataka"
    response = requests.post(
        f"{BASE_URL}/api/nlp/query",
        json={"query": query}
    )
    print(f"Query: {query}")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Intent: {data['intent']}")
    print(f"Sub-Intent: {data['sub_intent']}")
    print(f"Confidence: {data['confidence']:.2f}")
    print(f"Entities: {json.dumps(data['entities'], indent=2)}")
    print(f"API Params: {json.dumps(data['api_params'], indent=2)}")
    print(f"Suggested Endpoint: {data['suggested_endpoint']}")
    print(f"Friendly Message: {data['friendly_message']}")
    assert response.status_code == 200
    assert data['intent'] == 'search'
    assert 'Karnataka' in data['entities']['states']
    assert 'Computer Science' in data['entities']['courses']
    print("✅ PASSED")


def test_budget_search_query():
    """Test search with budget constraint."""
    print("\n4. Testing Budget Search Query...")
    query = "Show me engineering colleges in Mumbai under 2 lakhs"
    response = requests.post(
        f"{BASE_URL}/api/nlp/query",
        json={"query": query}
    )
    print(f"Query: {query}")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Intent: {data['intent']}")
    print(f"Confidence: {data['confidence']:.2f}")
    print(f"Extracted Budget: {data['entities']['budget']}")
    print(f"API Params: {json.dumps(data['api_params'], indent=2)}")
    assert response.status_code == 200
    assert data['entities']['budget'] == 200000
    print("✅ PASSED")


def test_compare_query():
    """Test college comparison query."""
    print("\n5. Testing Comparison Query...")
    query = "Compare IIT Bombay and IIT Delhi"
    response = requests.post(
        f"{BASE_URL}/api/nlp/query",
        json={"query": query}
    )
    print(f"Query: {query}")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Intent: {data['intent']}")
    print(f"Confidence: {data['confidence']:.2f}")
    print(f"Colleges: {data['entities']['colleges']}")
    print(f"Suggested Endpoint: {data['suggested_endpoint']}")
    assert response.status_code == 200
    assert data['intent'] == 'compare'
    assert len(data['entities']['colleges']) >= 2
    print("✅ PASSED")


def test_recommendation_query():
    """Test recommendation query."""
    print("\n6. Testing Recommendation Query...")
    query = "Recommend me affordable ECE colleges in Tamil Nadu"
    response = requests.post(
        f"{BASE_URL}/api/nlp/query",
        json={"query": query}
    )
    print(f"Query: {query}")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Intent: {data['intent']}")
    print(f"Confidence: {data['confidence']:.2f}")
    print(f"Entities: {json.dumps(data['entities'], indent=2)}")
    print(f"API Params: {json.dumps(data['api_params'], indent=2)}")
    assert response.status_code == 200
    assert data['intent'] == 'recommend'
    print("✅ PASSED")


def test_info_query():
    """Test information query."""
    print("\n7. Testing Info Query...")
    query = "Tell me about NIT Trichy fees and placements"
    response = requests.post(
        f"{BASE_URL}/api/nlp/query",
        json={"query": query}
    )
    print(f"Query: {query}")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Intent: {data['intent']}")
    print(f"Confidence: {data['confidence']:.2f}")
    print(f"Colleges: {data['entities']['colleges']}")
    print(f"Info Type: {data['api_params'].get('info_type')}")
    assert response.status_code == 200
    assert data['intent'] == 'info'
    print("✅ PASSED")


def test_complex_query():
    """Test complex multi-filter query."""
    print("\n8. Testing Complex Query...")
    query = "Find government CS colleges in Karnataka with hostel under 3 lakhs in top 50 NIRF"
    response = requests.post(
        f"{BASE_URL}/api/nlp/query",
        json={"query": query}
    )
    print(f"Query: {query}")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Intent: {data['intent']}")
    print(f"Confidence: {data['confidence']:.2f}")
    print(f"Entities: {json.dumps(data['entities'], indent=2)}")
    print(f"API Params: {json.dumps(data['api_params'], indent=2)}")
    assert response.status_code == 200
    assert data['entities']['ownership'] == 'Government'
    assert 'hostel' in data['entities']['facilities']
    assert data['entities']['budget'] == 300000
    print("✅ PASSED")


def test_greeting_query():
    """Test greeting query."""
    print("\n9. Testing Greeting Query...")
    query = "Hello, can you help me find colleges?"
    response = requests.post(
        f"{BASE_URL}/api/nlp/query",
        json={"query": query}
    )
    print(f"Query: {query}")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Intent: {data['intent']}")
    print(f"Confidence: {data['confidence']:.2f}")
    print(f"Friendly Message: {data['friendly_message']}")
    assert response.status_code == 200
    assert data['intent'] == 'greeting'
    print("✅ PASSED")


def test_tier_query():
    """Test tier-based query."""
    print("\n10. Testing Tier Query...")
    query = "Show me tier 1 colleges for mechanical engineering"
    response = requests.post(
        f"{BASE_URL}/api/nlp/query",
        json={"query": query}
    )
    print(f"Query: {query}")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Intent: {data['intent']}")
    print(f"Confidence: {data['confidence']:.2f}")
    print(f"Tier: {data['entities']['tier']}")
    print(f"Courses: {data['entities']['courses']}")
    print(f"API Params: {json.dumps(data['api_params'], indent=2)}")
    assert response.status_code == 200
    assert data['entities']['tier'] == 'Tier 1'
    print("✅ PASSED")


def run_all_tests():
    """Run all NLP tests."""
    print("=" * 60)
    print("NLP API ENDPOINT TESTS")
    print("=" * 60)
    
    tests = [
        test_nlp_health,
        test_nlp_examples,
        test_simple_search_query,
        test_budget_search_query,
        test_compare_query,
        test_recommendation_query,
        test_info_query,
        test_complex_query,
        test_greeting_query,
        test_tier_query
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 60)
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED!")
    else:
        print(f"⚠️ {failed} test(s) failed")


if __name__ == "__main__":
    run_all_tests()
