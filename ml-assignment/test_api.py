import requests
import json
import pandas as pd
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:5002"

def test_health_check():
    """Test the health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_calculate_features_structured():
    """Test the structured endpoint with properly formatted data"""
    # Example structured data
    request_data = {
        "id": "test_123",
        "application_date": "2024-02-12T19:24:29.135000",
        "contracts": [
            {
                "contract_id": "522530",
                "bank": "003",
                "summa": "500000000",
                "loan_summa": "0",
                "claim_date": "13.02.2020",
                "claim_id": "609965",
                "contract_date": "17.02.2020"
            },
            {
                "contract_id": "",
                "bank": "014",
                "summa": "",
                "loan_summa": "",
                "claim_date": "28.08.2020",
                "claim_id": "F00013731",
                "contract_date": ""
            },
            {
                "contract_id": "35163",
                "bank": "053",
                "summa": "510000000",
                "loan_summa": "0",
                "claim_date": "15.12.2020",
                "claim_id": "35163",
                "contract_date": "21.12.2020"
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/calculate-features", json=request_data)
    print("Structured Endpoint Test:")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("Features calculated:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    else:
        print(f"Error: {response.text}")
    print()

def test_calculate_features_from_csv():
    """Test with actual data from the CSV file"""
    # Read a sample from the CSV
    df = pd.read_csv('ml-assignment/data.csv')
    
    # Find first row with non-empty contracts
    sample_row = None
    for i, row in df.iterrows():
        if pd.notna(row['contracts']) and row['contracts'].strip():
            sample_row = row
            break
    
    if sample_row is None:
        print("No valid sample data found in CSV")
        return
    
    # Prepare data for JSON endpoint
    request_data = {
        "id": str(sample_row['id']),
        "application_date": sample_row['application_date'],
        "contracts": sample_row['contracts']
    }
    
    response = requests.post(f"{BASE_URL}/calculate-features-from-json", json=request_data)
    print("CSV Data Test:")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("Features calculated from CSV data:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    else:
        print(f"Error: {response.text}")
    print()

def test_edge_cases():
    """Test edge cases"""
    print("Testing Edge Cases:")
    
    # Test with no contracts
    request_data = {
        "id": "edge_case_1",
        "application_date": "2024-02-12T19:24:29.135000",
        "contracts": []
    }
    
    response = requests.post(f"{BASE_URL}/calculate-features", json=request_data)
    print("No contracts test:")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        for key, value in result.items():
            print(f"  {key}: {value}")
    print()
    
    # Test with empty contracts string
    request_data = {
        "id": "edge_case_2",
        "application_date": "2024-02-12T19:24:29.135000",
        "contracts": ""
    }
    
    response = requests.post(f"{BASE_URL}/calculate-features-from-json", json=request_data)
    print("Empty contracts string test:")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        for key, value in result.items():
            print(f"  {key}: {value}")
    print()

def main():
    """Run all tests"""
    print("FastAPI ML Feature Engineering Service - Test Suite")
    print("=" * 60)
    
    try:
        test_health_check()
        test_calculate_features_structured()
        test_calculate_features_from_csv()
        test_edge_cases()
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the FastAPI server is running with: python main.py")
        print("Or run: uvicorn main:app --reload")

if __name__ == "__main__":
    main() 