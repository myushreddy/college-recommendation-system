"""
Test specific failing endpoints with error details.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("="*60)
print("Testing College Details Endpoint")
print("="*60)
response = requests.get(f"{BASE_URL}/api/colleges/1")
print(f"Status: {response.status_code}")
try:
    data = response.json()
    print(json.dumps(data, indent=2))
except:
    print(response.text)

print("\n" + "="*60)
print("Testing College Comparison Endpoint")
print("="*60)
payload = {"college_ids": [1, 2, 3]}
response = requests.post(f"{BASE_URL}/api/colleges/compare", json=payload)
print(f"Status: {response.status_code}")
try:
    data = response.json()
    print(json.dumps(data, indent=2))
except:
    print(response.text)
