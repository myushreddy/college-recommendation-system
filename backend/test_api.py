"""
Test script for College Recommendation API endpoints.
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def print_response(title, response):
    """Helper to print formatted responses."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except:
        print(response.text)
    print()


def test_root():
    """Test root endpoint."""
    response = requests.get(f"{BASE_URL}/")
    print_response("TEST 1: Root Endpoint", response)
    return response.status_code == 200


def test_health():
    """Test health check endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    print_response("TEST 2: Health Check", response)
    return response.status_code == 200


def test_statistics():
    """Test statistics endpoint."""
    response = requests.get(f"{BASE_URL}/api/colleges/stats/overview")
    print_response("TEST 3: Statistics Overview", response)
    return response.status_code == 200


def test_search_basic():
    """Test basic search."""
    response = requests.get(f"{BASE_URL}/api/colleges/search?page=1&page_size=5")
    print_response("TEST 4: Basic Search (First 5 Colleges)", response)
    return response.status_code == 200


def test_search_with_filters():
    """Test search with filters."""
    params = {
        "state": "Karnataka",
        "tier": "Tier 1",
        "page": 1,
        "page_size": 5
    }
    response = requests.get(f"{BASE_URL}/api/colleges/search", params=params)
    print_response("TEST 5: Search - Karnataka Tier 1 Colleges", response)
    return response.status_code == 200


def test_search_fuzzy():
    """Test fuzzy search."""
    params = {
        "query": "IIT",
        "page": 1,
        "page_size": 10
    }
    response = requests.get(f"{BASE_URL}/api/colleges/search", params=params)
    print_response("TEST 6: Fuzzy Search - 'IIT'", response)
    return response.status_code == 200


def test_college_details():
    """Test getting college details."""
    response = requests.get(f"{BASE_URL}/api/colleges/5516")
    print_response("TEST 7: College Details (ID=5516)", response)
    return response.status_code == 200


def test_compare_colleges():
    """Test college comparison."""
    payload = {
        "college_ids": [5516, 5517, 5518]
    }
    response = requests.post(f"{BASE_URL}/api/colleges/compare", json=payload)
    print_response("TEST 8: Compare Colleges (IDs: 5516, 5517, 5518)", response)
    return response.status_code == 200


def test_recommendations_basic():
    """Test basic recommendations."""
    payload = {
        "limit": 5
    }
    response = requests.post(f"{BASE_URL}/api/colleges/recommendations", json=payload)
    print_response("TEST 9: Basic Recommendations (Top 5)", response)
    return response.status_code == 200


def test_recommendations_with_filters():
    """Test recommendations with filters."""
    payload = {
        "budget": 200000,
        "preferred_states": ["Karnataka", "Tamil Nadu"],
        "course_category": "Computer Science",
        "required_facilities": ["hostel", "library"],
        "limit": 5
    }
    response = requests.post(f"{BASE_URL}/api/colleges/recommendations", json=payload)
    print_response("TEST 10: Personalized Recommendations (CS, Budget 2L, Karnataka/TN)", response)
    return response.status_code == 200


def run_all_tests():
    """Run all API tests."""
    print("\n" + "="*60)
    print("COLLEGE RECOMMENDATION API - TEST SUITE")
    print("="*60)
    
    tests = [
        ("Root Endpoint", test_root),
        ("Health Check", test_health),
        ("Statistics", test_statistics),
        ("Basic Search", test_search_basic),
        ("Search with Filters", test_search_with_filters),
        ("Fuzzy Search", test_search_fuzzy),
        ("College Details", test_college_details),
        ("College Comparison", test_compare_colleges),
        ("Basic Recommendations", test_recommendations_basic),
        ("Filtered Recommendations", test_recommendations_with_filters)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, "✅ PASS" if passed else "❌ FAIL"))
        except Exception as e:
            results.append((name, f"❌ ERROR: {str(e)}"))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for name, status in results:
        # Use ASCII-safe characters
        status_clean = status.replace("✅", "[PASS]").replace("❌", "[FAIL]")
        print(f"{name:<40} {status_clean}")
    
    passed = sum(1 for _, status in results if "PASS" in status or "✅" in status)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")
    print("="*60)


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
    except Exception as e:
        print(f"\n\nFatal error: {e}")
