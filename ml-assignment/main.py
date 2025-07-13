from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

app = FastAPI(
    title="ML Feature Engineering Service",
    description="A FastAPI service that calculates financial features from contract data",
    version="1.0.0"
)

# Add CORS middleware to allow requests from the documentation server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5002", "http://127.0.0.1:5002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContractData(BaseModel):
    contract_id: Optional[str] = ""
    bank: Optional[str] = ""
    summa: Optional[str] = ""
    loan_summa: Optional[str] = ""
    claim_date: Optional[str] = ""
    claim_id: Optional[str] = ""
    contract_date: Optional[str] = ""

class ApplicationRequest(BaseModel):
    id: Optional[str] = None
    application_date: str
    contracts: List[ContractData]

class FeatureResponse(BaseModel):
    id: Optional[str] = None
    application_date: str
    tot_claim_cnt_l180d: int
    disb_bank_loan_wo_tbc: float
    day_sinlastloan: int

def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string in DD.MM.YYYY format"""
    if not date_str or date_str == "":
        return None
    try:
        return datetime.strptime(date_str, '%d.%m.%Y')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return None

def calculate_features(application_date: str, contracts: List[dict]) -> Dict[str, Any]:
    """Calculate features for a single application"""
    features = {}
    
    # Parse application date
    app_date = pd.to_datetime(application_date)
    if app_date.tz is not None:
        app_date = app_date.tz_localize(None)  # Remove timezone info
    
    # Feature 1: tot_claim_cnt_l180d
    # Number of claims made in the 180 days before the application_date
    claim_count = 0
    for contract in contracts:
        claim_date_str = contract.get('claim_date', '')
        if claim_date_str and claim_date_str != "":
            claim_date = parse_date(claim_date_str)
            if claim_date:
                days_diff = (app_date - claim_date).days
                if 0 <= days_diff <= 180:
                    claim_count += 1
    
    features['tot_claim_cnt_l180d'] = claim_count if claim_count > 0 else -3
    
    # Feature 2: disb_bank_loan_wo_tbc
    # Sum of disbursed loans exposure without TBC loans
    excluded_banks = ['LIZ', 'LOM', 'MKO', 'SUG', '', None]
    total_loan_exposure = 0
    has_loans = False
    
    for contract in contracts:
        bank = contract.get('bank', '')
        loan_summa = contract.get('loan_summa', '')
        contract_date = contract.get('contract_date', '')
        
        # Check if it's a valid loan (contract_date not null and bank not excluded)
        if contract_date and contract_date != "" and bank not in excluded_banks:
            if loan_summa and loan_summa != "":
                try:
                    loan_amount = float(loan_summa)
                    total_loan_exposure += loan_amount
                    has_loans = True
                except ValueError:
                    pass
    
    if has_loans:
        features['disb_bank_loan_wo_tbc'] = total_loan_exposure
    else:
        # Check if there are any claims at all
        has_claims = any(contract.get('claim_id', '') != '' for contract in contracts)
        features['disb_bank_loan_wo_tbc'] = -1 if not has_claims else -3
    
    # Feature 3: day_sinlastloan
    # Number of days since last loan
    last_loan_date = None
    
    for contract in contracts:
        summa = contract.get('summa', '')
        contract_date_str = contract.get('contract_date', '')
        
        if summa and summa != "" and contract_date_str and contract_date_str != "":
            contract_date = parse_date(contract_date_str)
            if contract_date:
                if last_loan_date is None or contract_date > last_loan_date:
                    last_loan_date = contract_date
    
    if last_loan_date:
        days_since_last_loan = (app_date - last_loan_date).days
        features['day_sinlastloan'] = days_since_last_loan
    else:
        # Check if there are any claims at all
        has_claims = any(contract.get('claim_id', '') != '' for contract in contracts)
        features['day_sinlastloan'] = -1 if not has_claims else -3
    
    return features

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "ML Feature Engineering Service",
        "description": "Submit application data to calculate financial features",
        "endpoints": {
            "POST /calculate-features": "Calculate features from application data",
            "GET /health": "Health check endpoint"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ML Feature Engineering Service"}

@app.post("/calculate-features", response_model=FeatureResponse)
async def calculate_application_features(request: ApplicationRequest):
    """
    Calculate features from application data
    
    This endpoint accepts application data with contracts and returns calculated features:
    - tot_claim_cnt_l180d: Number of claims in last 180 days
    - disb_bank_loan_wo_tbc: Sum of disbursed loans excluding TBC banks
    - day_sinlastloan: Days since last loan
    """
    try:
        # Convert contracts to dict format
        contracts_dict = [contract.dict() for contract in request.contracts]
        
        # Calculate features
        features = calculate_features(request.application_date, contracts_dict)
        
        # Prepare response
        response = FeatureResponse(
            id=request.id,
            application_date=request.application_date,
            tot_claim_cnt_l180d=features['tot_claim_cnt_l180d'],
            disb_bank_loan_wo_tbc=features['disb_bank_loan_wo_tbc'],
            day_sinlastloan=features['day_sinlastloan']
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating features: {str(e)}")

@app.post("/calculate-features-from-json")
async def calculate_features_from_json(data: Dict[str, Any]):
    """
    Alternative endpoint that accepts data in the same format as the CSV file
    
    Expected format:
    {
        "id": "2925211.0",
        "application_date": "2024-02-12 19:24:29.135000+00:00",
        "contracts": "[{\"contract_id\": 522530, \"bank\": \"003\", ...}]"
    }
    """
    try:
        # Extract data
        application_id = data.get('id')
        application_date = data.get('application_date')
        contracts_json = data.get('contracts', '')
        
        if not application_date:
            raise ValueError("application_date is required")
        
        # Parse contracts
        if contracts_json and contracts_json != "":
            try:
                contracts = json.loads(contracts_json)
                # Ensure all contracts are dictionaries
                contracts = [c for c in contracts if isinstance(c, dict)]
            except json.JSONDecodeError:
                contracts = []
        else:
            contracts = []
        
        # Calculate features
        features = calculate_features(application_date, contracts)
        
        # Prepare response
        response = {
            "id": application_id,
            "application_date": application_date,
            "tot_claim_cnt_l180d": features['tot_claim_cnt_l180d'],
            "disb_bank_loan_wo_tbc": features['disb_bank_loan_wo_tbc'],
            "day_sinlastloan": features['day_sinlastloan']
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating features: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002) 