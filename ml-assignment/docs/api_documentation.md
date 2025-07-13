# ML Feature Engineering API Documentation

## Table of Contents
1. [Problem Description](#problem-description)
2. [Solution Overview](#solution-overview)
3. [How to Start the API Services](#how-to-start-the-api-services)
4. [How to Use the API](#how-to-use-the-api)
5. [API Endpoints](#api-endpoints)
6. [Testing the API](#testing-the-api)
7. [Troubleshooting](#troubleshooting)

---

## Problem Description

### The Challenge
Financial institutions need to calculate specific machine learning features from contract data to assess risk and make lending decisions. The original challenge involved:

1. **Complex Data Processing**: Processing financial contract data with various date formats and data types
2. **Feature Engineering**: Calculating three critical features:
   - `tot_claim_cnt_l180d`: Number of claims in the last 180 days
   - `disb_bank_loan_wo_tbc`: Sum of disbursed loans excluding TBC banks
   - `day_sinlastloan`: Days since the last loan
3. **Data Validation**: Ensuring data integrity and handling edge cases
4. **Scalability**: Processing multiple contracts per application efficiently
5. **Integration**: Providing a reliable API interface for ML pipelines

### Business Impact
- **Risk Assessment**: Accurate feature calculation for credit risk models
- **Decision Speed**: Real-time feature generation for loan applications
- **Data Quality**: Consistent feature engineering across applications
- **Compliance**: Standardized calculations for regulatory requirements

---

## Solution Overview

### How We Solved the Problem

We developed a comprehensive FastAPI-based solution that addresses all the challenges:

#### 1. **FastAPI Framework**
- **High Performance**: Asynchronous processing for concurrent requests
- **Automatic Documentation**: Built-in OpenAPI/Swagger documentation
- **Type Safety**: Pydantic models for request/response validation
- **Easy Integration**: RESTful API design

#### 2. **Robust Data Processing**
- **Date Handling**: Flexible date parsing for DD.MM.YYYY and ISO formats
- **Data Validation**: Comprehensive input validation with error handling
- **Edge Case Management**: Special values for missing/invalid data
- **Type Conversion**: Automatic type conversion and validation

#### 3. **Feature Engineering Logic**
- **tot_claim_cnt_l180d**: Filters claims within 180 days using date arithmetic
- **disb_bank_loan_wo_tbc**: Excludes TBC banks and sums valid loan amounts
- **day_sinlastloan**: Calculates days difference from most recent contract

#### 4. **Interactive Documentation**
- **Beautiful UI**: Modern, responsive documentation interface
- **Live API Testing**: Interactive API tester with real-time validation
- **Code Examples**: Sample requests in Python, JavaScript, and cURL
- **Server Monitoring**: Real-time API server status indicator

#### 5. **Development Tools**
- **Hot Reload**: Automatic server restart during development
- **Error Handling**: Comprehensive error messages and logging
- **CORS Support**: Cross-origin requests for browser-based testing

---

## How to Start the API Services

### Prerequisites
- Python 3.8 or higher
- Conda package manager
- Node.js and npm

### Step 1: Environment Setup
```bash
# Navigate to project directory
cd ml-assignment

# Create and activate conda environment
conda create -n new_nlp python=3.8
conda activate new_nlp

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Install Documentation Dependencies
```bash
# Navigate to docs directory
cd docs

# Install Node.js dependencies
npm install
```

### Step 3: Start the Main API Server
```bash
# Navigate back to project root
cd ..

# Activate conda environment
conda activate new_nlp

# Start the FastAPI server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected Output:**
```
INFO:     Started server process [18766]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 4: Start the Documentation Server
```bash
# Open a new terminal window
# Navigate to docs directory
cd tatia/docs

# Start the documentation server
npm start
```

**Expected Output:**
```
> ml-feature-api-docs@1.0.0 start
> node server.js

📚 Documentation server running at http://localhost:5002
🌐 Access docs at: http://localhost:5002/docs
```

### Step 5: Verify Both Services Are Running
- **Main API**: http://localhost:8000/health
- **Documentation**: http://localhost:5002/docs
- **FastAPI Docs**: http://localhost:8000/docs

---

## How to Use the API

### 1. Health Check
**Purpose**: Verify the API is running properly

**Request:**
```bash
curl -X GET http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "ML Feature Engineering Service"
}
```

### 2. Calculate Features (Structured Format)
**Purpose**: Calculate features from structured JSON data

**Request:**
```bash
curl -X POST "http://localhost:8000/calculate-features" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "application_123",
    "application_date": "2024-02-12T19:24:29.135000",
    "contracts": [
      {
        "contract_id": "CONTRACT_001",
        "bank": "003",
        "summa": "1000000",
        "loan_summa": "800000",
        "claim_date": "10.01.2024",
        "claim_id": "CLAIM_001",
        "contract_date": "15.01.2024"
      }
    ]
  }'
```

**Response:**
```json
{
  "id": "application_123",
  "application_date": "2024-02-12T19:24:29.135000",
  "tot_claim_cnt_l180d": 1,
  "disb_bank_loan_wo_tbc": 800000.0,
  "day_sinlastloan": 28
}
```

### 3. Calculate Features (JSON String Format)
**Purpose**: Calculate features from CSV-like JSON string data

**Request:**
```bash
curl -X POST "http://localhost:8000/calculate-features-from-json" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "application_123",
    "application_date": "2024-02-12 19:24:29.135000+00:00",
    "contracts": "[{\"contract_id\": \"CONTRACT_001\", \"bank\": \"003\", \"summa\": 1000000, \"loan_summa\": 800000, \"claim_date\": \"10.01.2024\", \"claim_id\": \"CLAIM_001\", \"contract_date\": \"15.01.2024\"}]"
  }'
```

### 4. Python Example
```python
import requests
import json

# API configuration
API_BASE_URL = "http://localhost:8000"

# Example data
data = {
    "id": "python_test_001",
    "application_date": "2024-02-12T19:24:29.135000",
    "contracts": [
        {
            "contract_id": "CONTRACT_001",
            "bank": "003",
            "summa": "1000000",
            "loan_summa": "800000",
            "claim_date": "10.01.2024",
            "claim_id": "CLAIM_001",
            "contract_date": "15.01.2024"
        }
    ]
}

# Send request
try:
    response = requests.post(f"{API_BASE_URL}/calculate-features", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print("✓ Features calculated successfully:")
        print(f"  - Total claims (180d): {result['tot_claim_cnt_l180d']}")
        print(f"  - Disbursed loans (no TBC): {result['disb_bank_loan_wo_tbc']}")
        print(f"  - Days since last loan: {result['day_sinlastloan']}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"  Response: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"✗ Connection error: {e}")
```

### 5. JavaScript Example
```javascript
const axios = require('axios');

// API configuration
const API_BASE_URL = 'http://localhost:8000';

// Example data
const data = {
    id: 'javascript_test_001',
    application_date: '2024-02-12T19:24:29.135000',
    contracts: [
        {
            contract_id: 'CONTRACT_001',
            bank: '003',
            summa: '1000000',
            loan_summa: '800000',
            claim_date: '10.01.2024',
            claim_id: 'CLAIM_001',
            contract_date: '15.01.2024'
        }
    ]
};

// Send request
axios.post(`${API_BASE_URL}/calculate-features`, data)
    .then(response => {
        console.log('✓ Features calculated successfully:');
        console.log(`  - Total claims (180d): ${response.data.tot_claim_cnt_l180d}`);
        console.log(`  - Disbursed loans (no TBC): ${response.data.disb_bank_loan_wo_tbc}`);
        console.log(`  - Days since last loan: ${response.data.day_sinlastloan}`);
    })
    .catch(error => {
        console.error('✗ Error:', error.response?.data || error.message);
    });
```

---

## API Endpoints

### 1. GET /health
**Description**: Health check endpoint
**Response**: Service status information

### 2. GET /
**Description**: Root endpoint with API information
**Response**: API welcome message and available endpoints

### 3. POST /calculate-features
**Description**: Calculate features from structured data
**Request Body**: ApplicationRequest model
**Response**: FeatureResponse model with calculated features

### 4. POST /calculate-features-from-json
**Description**: Calculate features from JSON string format
**Request Body**: Dictionary with JSON string contracts
**Response**: FeatureResponse model with calculated features

### Feature Descriptions

#### tot_claim_cnt_l180d
- **Purpose**: Count claims within 180 days before application date
- **Logic**: Filters claims where claim_date is within 180 days of application_date
- **Format**: claim_date in DD.MM.YYYY format
- **Special Values**: -3 if no claims found

#### disb_bank_loan_wo_tbc
- **Purpose**: Sum of disbursed loan amounts excluding TBC banks
- **Logic**: Excludes banks ['LIZ', 'LOM', 'MKO', 'SUG', null], sums loan_summa
- **Conditions**: Only includes loans where loan_summa > 0
- **Special Values**: -1 if no loans, -3 if no claims

#### day_sinlastloan
- **Purpose**: Days between last loan and application date
- **Logic**: Finds most recent contract_date, calculates difference
- **Format**: contract_date in DD.MM.YYYY format
- **Special Values**: -1 if no loans, -3 if no claims

---

## Testing the API

### 1. Interactive API Tester
**Access**: http://localhost:5002/docs

**Features**:
- **Real-time Status**: Green/red indicator for API server status
- **Endpoint Selection**: Dropdown menu with all available endpoints
- **Sample Data**: Pre-populated request bodies for testing
- **Live Testing**: Send requests and view formatted responses
- **Copy Functions**: Copy request/response data to clipboard

**How to Use**:
1. Open http://localhost:5002/docs in your browser
2. Verify "API server is online" status (green indicator)
3. Select an endpoint from the dropdown
4. Review the auto-populated request body
5. Click "Send Request"
6. View the formatted response

### 2. Manual Testing Steps

#### Test Health Endpoint
```bash
curl -X GET http://localhost:8000/health
# Expected: {"status":"healthy","service":"ML Feature Engineering Service"}
```

#### Test Feature Calculation
```bash
curl -X POST "http://localhost:8000/calculate-features" \
  -H "Content-Type: application/json" \
  -d '{"id":"test","application_date":"2024-02-12T19:24:29.135000","contracts":[]}'
# Expected: Feature response with special values for empty contracts
```

#### Test with Real Data
```bash
curl -X POST "http://localhost:8000/calculate-features" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "real_test",
    "application_date": "2024-02-12T19:24:29.135000",
    "contracts": [
      {
        "contract_id": "CONTRACT_001",
        "bank": "003",
        "summa": "1000000",
        "loan_summa": "800000",
        "claim_date": "10.01.2024",
        "claim_id": "CLAIM_001",
        "contract_date": "15.01.2024"
      }
    ]
  }'
```

### 3. Test Cases

#### Edge Case: No Contracts
```json
{
  "id": "no_contracts_test",
  "application_date": "2024-02-12T19:24:29.135000",
  "contracts": []
}
```
**Expected Result**: All features return -3 (no claims)

#### Edge Case: TBC Bank Only
```json
{
  "id": "tbc_only_test",
  "application_date": "2024-02-12T19:24:29.135000",
  "contracts": [
    {
      "contract_id": "TBC_CONTRACT",
      "bank": "LIZ",
      "summa": "1000000",
      "loan_summa": "800000",
      "claim_date": "10.01.2024",
      "claim_id": "TBC_CLAIM",
      "contract_date": "15.01.2024"
    }
  ]
}
```
**Expected Result**: disb_bank_loan_wo_tbc = 0 (TBC bank excluded)

#### Edge Case: Multiple Contracts
```json
{
  "id": "multiple_contracts_test",
  "application_date": "2024-02-12T19:24:29.135000",
  "contracts": [
    {
      "contract_id": "CONTRACT_001",
      "bank": "003",
      "summa": "1000000",
      "loan_summa": "800000",
      "claim_date": "10.01.2024",
      "claim_id": "CLAIM_001",
      "contract_date": "15.01.2024"
    },
    {
      "contract_id": "CONTRACT_002",
      "bank": "005",
      "summa": "500000",
      "loan_summa": "300000",
      "claim_date": "20.01.2024",
      "claim_id": "CLAIM_002",
      "contract_date": "25.01.2024"
    }
  ]
}
```
**Expected Result**: 
- tot_claim_cnt_l180d = 2 (both claims within 180 days)
- disb_bank_loan_wo_tbc = 1,100,000 (sum of both loans)
- day_sinlastloan = 18 (days since Jan 25, 2024)

---

## Troubleshooting

### Common Issues

#### 1. API Server Not Starting
**Problem**: `ModuleNotFoundError` or import errors
**Solution**:
```bash
# Ensure conda environment is activated
conda activate new_nlp

# Reinstall dependencies
pip install -r requirements.txt

# Check if FastAPI is installed
python -c "import fastapi; print('FastAPI installed')"
```

#### 2. Port Already in Use
**Problem**: `Address already in use` error
**Solution**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process (replace PID with actual process ID)
kill -9 <PID>

# Or use a different port
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

#### 3. Documentation Server Issues
**Problem**: npm dependencies not installed
**Solution**:
```bash
cd docs
rm -rf node_modules
npm install
npm start
```

#### 4. CORS Errors
**Problem**: Browser requests blocked
**Solution**:
- Ensure both servers are running
- Check main.py has CORS middleware configured
- Verify documentation server is on port 5002

#### 5. Date Format Errors
**Problem**: Date parsing failures
**Solution**:
- Use DD.MM.YYYY format for claim_date and contract_date
- Use ISO format for application_date: YYYY-MM-DDTHH:MM:SS.ffffff
- Ensure dates are strings, not integers

#### 6. Invalid JSON Format
**Problem**: JSON parsing errors
**Solution**:
- Validate JSON format using online tools
- Check for missing quotes, commas, or brackets
- Ensure proper escaping in JSON string format

### Debug Commands

#### Check API Status
```bash
curl -X GET http://localhost:8000/health -v
```

#### Test with Verbose Output
```bash
curl -X POST "http://localhost:8000/calculate-features" \
  -H "Content-Type: application/json" \
  -d '{"id":"debug","application_date":"2024-02-12T19:24:29.135000","contracts":[]}' \
  -v
```

#### View Server Logs
```bash
# Start with debug logging
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

### Performance Tips

1. **Batch Processing**: Send multiple applications in separate requests
2. **Connection Pooling**: Use connection pooling for high-volume requests
3. **Caching**: Cache frequent calculations if data doesn't change
4. **Monitoring**: Monitor response times and error rates

---

## Summary

This ML Feature Engineering API provides a robust solution for calculating financial features from contract data. The combination of FastAPI for the backend and a beautiful interactive documentation interface makes it easy to integrate, test, and maintain.

**Key Benefits**:
- ✅ **Fast Processing**: Efficient feature calculation
- ✅ **Easy Testing**: Interactive API tester
- ✅ **Comprehensive Documentation**: Clear examples and instructions
- ✅ **Error Handling**: Robust validation and error messages
- ✅ **Scalable**: Can handle multiple contracts and applications
- ✅ **Developer Friendly**: Hot reload and debugging support

For additional support, use the interactive documentation at http://localhost:5002/docs or refer to the FastAPI auto-documentation at http://localhost:8000/docs. 