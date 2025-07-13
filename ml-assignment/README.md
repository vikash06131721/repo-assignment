# ML Feature Engineering FastAPI Service

This project implements a FastAPI web service that processes financial contract data and calculates specific features as defined in the assignment requirements.

## Assignment Overview

The task is to build a FastAPI service that:
- Accepts requests with application data containing contract information
- Processes the contracts JSON to compute required features
- Returns the calculated features as a response

## Features Implemented

Based on the `features.csv` specification, the service calculates three key features:

### 1. `tot_claim_cnt_l180d`
- **Description**: Number of claims made in the 180 days before the application_date
- **Logic**: Count claims where claim_date is within 180 days of application_date
- **Missing value**: -3 if no claims found

### 2. `disb_bank_loan_wo_tbc`
- **Description**: Sum of disbursed loans exposure without TBC loans
- **Logic**: Sum loan_summa for contracts where:
  - Bank is not in ['LIZ', 'LOM', 'MKO', 'SUG', null]
  - contract_date is not null (disbursed loans)
- **Missing values**: 
  - -1 if no loans at all
  - -3 if no claims at all

### 3. `day_sinlastloan`
- **Description**: Number of days since last loan
- **Logic**: Calculate days from contract_date of last loan (where summa is not null) to application_date
- **Missing values**:
  - -1 if no loans at all
  - -3 if no claims at all

## Project Structure

```
tatia/
├── ml-assignment/
│   ├── data.csv          # Source data with application and contract information
│   ├── features.csv      # Feature definitions and specifications
│   ├── features.xlsx     # Feature definitions in Excel format
│   └── ml_assignment.pdf # Assignment documentation
├── main.py               # FastAPI application
├── data_analysis.py      # Data analysis and feature calculation logic
├── test_api.py          # API testing script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Data Structure

The input data contains:
- `id`: Unique identifier for the application
- `application_date`: Date of the application
- `contracts`: JSON string containing array of contract objects

Each contract object has the following fields:
- `contract_id`: Contract identifier
- `bank`: Bank code
- `summa`: Contract sum amount
- `loan_summa`: Loan sum amount
- `claim_date`: Date of claim (DD.MM.YYYY format)
- `claim_id`: Claim identifier
- `contract_date`: Date of contract (DD.MM.YYYY format)

## Installation and Setup

1. **Activate the conda environment**:
   ```bash
   conda activate new_nlp
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Service

1. **Start the FastAPI server**:
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API documentation**:
   - **Beautiful Custom Docs**: http://localhost:5002/docs (recommended)


## Quick Start (Recommended)

For the easiest setup, use the provided startup scripts:

**Linux/macOS:**
```bash
./start_services.sh
```

**Windows:**
```cmd
start_services.bat
```

These scripts will:
- Start both the API server and documentation server
- Install dependencies automatically
- Open the documentation in your browser
- Provide health checks and status monitoring

## Manual Setup

### Running the Documentation Server

For the best documentation experience, run the custom documentation server:

1. **Navigate to the docs directory**:
   ```bash
   cd docs
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the documentation server**:
   ```bash
   npm start
   ```
   
   Or for development with auto-reload:
   ```bash
   npm run dev
   ```

4. **Access the documentation**:
   - Beautiful docs: http://localhost:5002/docs
   - Interactive API tester included
   - Code examples for Python, JavaScript, and cURL
   - Real-time server status monitoring

## API Endpoints

### GET `/`
Root endpoint with API information.

### GET `/health`
Health check endpoint.

### POST `/calculate-features`
Calculate features from structured application data.

**Request format**:
```json
{
  "id": "2925211.0",
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
    }
  ]
}
```

**Response format**:
```json
{
  "id": "2925211.0",
  "application_date": "2024-02-12T19:24:29.135000",
  "tot_claim_cnt_l180d": 57,
  "disb_bank_loan_wo_tbc": -3,
  "day_sinlastloan": 427
}
```

### POST `/calculate-features-from-json`
Alternative endpoint that accepts data in the same format as the CSV file.

**Request format**:
```json
{
  "id": "2925211.0",
  "application_date": "2024-02-12 19:24:29.135000+00:00",
  "contracts": "[{\"contract_id\": 522530, \"bank\": \"003\", \"summa\": 500000000, ...}]"
}
```

## Testing the Service

1. **Run data analysis** (to understand the data):
   ```bash
   conda activate new_nlp
   python data_analysis.py
   ```

2. **Run API tests**:
   ```bash
   # Start the server first (in another terminal)
   python main.py
   
   # Then run tests
   python test_api.py
   ```

## Example Usage

```python
import requests

# Example request
data = {
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
        }
    ]
}

response = requests.post("http://localhost:8000/calculate-features", json=data)
print(response.json())
```

## Data Analysis Results

Based on the analysis of the provided dataset:
- **Dataset size**: 1000 applications with 9220 total contracts
- **Missing contracts**: 505 applications have no contracts
- **Unique banks**: 27 different bank codes
- **Date format**: DD.MM.YYYY for claim_date and contract_date

### Feature Statistics
- `tot_claim_cnt_l180d`: Mean 2.06, ranges from -3 to 150
- `disb_bank_loan_wo_tbc`: Mean 768M, highly variable loan amounts
- `day_sinlastloan`: Mean 115.62 days, ranges from -3 to 1730 days

## Error Handling

The service includes comprehensive error handling for:
- Invalid date formats
- Missing or malformed JSON data
- Invalid numeric values
- Timezone-aware datetime processing

## Dependencies

- FastAPI: Web framework
- Uvicorn: ASGI server
- Pandas: Data manipulation
- Pydantic: Data validation
- NumPy: Numerical computations

## Documentation System

This project includes a beautiful, interactive documentation system:

### Features
- **🎨 Beautiful Design**: Modern UI with gradients and animations
- **🔧 Interactive API Tester**: Test endpoints directly from the browser
- **📊 Real-time Monitoring**: Server status and health checks
- **💻 Code Examples**: Ready-to-use examples in Python, JavaScript, and cURL
- **📱 Responsive Design**: Works on desktop and mobile
- **🎯 Copy-to-Clipboard**: One-click code copying

### Access Points
- **Beautiful Custom Docs**: http://localhost:5002/docs (recommended)
- **Interactive API Tester**: http://localhost:5002/docs#testing
- **FastAPI Auto Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Quick Start
```bash
# Linux/macOS
./start_services.sh

# Windows
start_services.bat
```

## Assignment Compliance

This solution fully implements the requirements:
✅ FastAPI service that accepts application data  
✅ Processes contracts JSON to compute required features  
✅ Returns calculated features as response  
✅ Handles all edge cases specified in features.csv  
✅ Proper data validation and error handling  
✅ Interactive API documentation  
✅ Comprehensive testing  
✅ Beautiful custom documentation system 