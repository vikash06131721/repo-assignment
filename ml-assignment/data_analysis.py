import pandas as pd
import json
import numpy as np
from datetime import datetime, timedelta
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

def parse_date(date_str):
    """Parse date string in DD.MM.YYYY format"""
    if not date_str or pd.isna(date_str) or date_str == "":
        return None
    try:
        return datetime.strptime(date_str, '%d.%m.%Y')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return None

def calculate_features(application_date, contracts_json):
    """Calculate features for a single application"""
    features = {}
    
    # Parse application date
    app_date = pd.to_datetime(application_date)
    if app_date.tz is not None:
        app_date = app_date.tz_localize(None)  # Remove timezone info
    
    # Parse contracts
    if pd.isna(contracts_json) or contracts_json == "":
        contracts = []
    else:
        try:
            contracts = json.loads(contracts_json)
            # Ensure all contracts are dictionaries
            contracts = [c for c in contracts if isinstance(c, dict)]
        except json.JSONDecodeError:
            contracts = []
    
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

def analyze_data():
    """Analyze the data structure and calculate features"""
    # Read the data
    df = pd.read_csv('ml-assignment/data.csv')
    
    print("Data Analysis Report")
    print("=" * 50)
    print(f"Data shape: {df.shape}")
    print(f"Column names: {df.columns.tolist()}")
    print(f"Null values in contracts: {df['contracts'].isnull().sum()}")
    
    # Analyze contract structure
    all_contracts = []
    for i, contracts in enumerate(df['contracts']):
        if pd.notna(contracts) and contracts.strip():
            try:
                contracts_list = json.loads(contracts)
                # Only add dict contracts
                all_contracts.extend([c for c in contracts_list if isinstance(c, dict)])
            except json.JSONDecodeError:
                continue
    
    print(f"Total contracts across all rows: {len(all_contracts)}")
    
    # Analyze contract fields
    if all_contracts:
        print("\nContract fields analysis:")
        all_fields = set()
        for contract in all_contracts:
            if isinstance(contract, dict):
                all_fields.update(contract.keys())
            else:
                print(f"Warning: Contract is not a dict: {type(contract)} - {contract}")
        
        print(f"All contract fields: {all_fields}")
        
        # Analyze banks
        banks = [contract.get('bank', '') for contract in all_contracts if contract.get('bank', '')]
        print(f"Unique banks: {sorted(set(banks))}")
        
        # Analyze date formats
        dates = [contract.get('claim_date', '') for contract in all_contracts if contract.get('claim_date', '')]
        print(f"Sample claim_dates: {dates[:5]}")
        
        contract_dates = [contract.get('contract_date', '') for contract in all_contracts if contract.get('contract_date', '')]
        print(f"Sample contract_dates: {contract_dates[:5]}")
    
    # Calculate features for first few rows
    print("\nFeature Calculation Examples:")
    print("=" * 50)
    
    for i in range(min(5, len(df))):
        row = df.iloc[i]
        if pd.notna(row['contracts']) and row['contracts'].strip():
            features = calculate_features(row['application_date'], row['contracts'])
            print(f"Row {i} (ID: {row['id']}):")
            for feature, value in features.items():
                print(f"  {feature}: {value}")
            print()
    
    # Calculate features for all rows
    print("Calculating features for all rows...")
    feature_results = []
    
    for i, row in df.iterrows():
        features = calculate_features(row['application_date'], row['contracts'])
        result = {
            'id': row['id'],
            'application_date': row['application_date'],
            **features
        }
        feature_results.append(result)
    
    # Create results DataFrame
    results_df = pd.DataFrame(feature_results)
    
    print("\nFeature Statistics:")
    print("=" * 50)
    for feature in ['tot_claim_cnt_l180d', 'disb_bank_loan_wo_tbc', 'day_sinlastloan']:
        print(f"{feature}:")
        print(f"  Mean: {results_df[feature].mean():.2f}")
        print(f"  Median: {results_df[feature].median():.2f}")
        print(f"  Min: {results_df[feature].min()}")
        print(f"  Max: {results_df[feature].max()}")
        print(f"  Special values (-1, -3): {(results_df[feature] < 0).sum()}")
        print()
    
    # Save results
    results_df.to_csv('feature_results.csv', index=False)
    print("Results saved to feature_results.csv")
    
    return results_df

if __name__ == "__main__":
    results = analyze_data() 