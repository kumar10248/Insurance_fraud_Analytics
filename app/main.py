from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator, root_validator
from datetime import datetime
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Any
from model import InsuranceFraudModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Insurance Fraud Detection API")

try:
    model = InsuranceFraudModel('models/fraud_model.keras')
except Exception as e:
    logger.error(f"Model loading failed: {e}")
    raise

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClaimRequest(BaseModel):
    # Policy Information
    policy_bind_date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    policy_state: str = Field(default="CA")
    policy_csl: str = Field(default="100/300")
    policy_deductable: float = Field(default=500.0)
    policy_annual_premium: float = Field(default=1000.0)
    umbrella_limit: int = Field(default=0)
    
    # Insured Information
    insured_sex: str = Field(default="MALE")
    insured_education_level: str = Field(default="High School")
    insured_occupation: str = Field(default="Professional")
    insured_relationship: str = Field(default="Self")
    insured_zip: int = Field(default=90001)
    months_as_customer: int = Field(default=12)
    
    # Incident Information
    incident_date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    incident_type: str = Field(default="Single Vehicle Collision")
    collision_type: str = Field(default="Front Collision")
    incident_severity: str = Field(default="Minor Damage")
    authorities_contacted: str = Field(default="Police")
    incident_state: str = Field(default="CA")
    incident_city: str = Field(default="Los Angeles")
    incident_location: str = Field(default="Highway")
    number_of_vehicles_involved: int = Field(default=1)
    
    # Claim Details
    bodily_injuries: int = Field(default=0)
    witnesses: int = Field(default=0)
    police_report_available: str = Field(default="NO")
    total_claim_amount: float = Field(...)
    injury_claim: float = Field(default=0.0)
    property_claim: float = Field(default=0.0)
    vehicle_claim: float = Field(default=0.0)
    
    # Additional Features
    age: int = Field(default=30)
    capital_gains: float = Field(default=0.0, alias="capital-gains")
    capital_loss: float = Field(default=0.0, alias="capital-loss")
    incident_hour_of_the_day: int = Field(default=12)
    insured_hobbies: str = Field(default="reading")
    
    # Vehicle Information
    auto_make: str = Field(default="Honda")
    auto_model: str = Field(default="Civic")
    auto_year: int = Field(default=2020)

    @validator('total_claim_amount')
    def validate_total_claim(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Total claim amount must be positive")
        return v

    @validator('age')
    def validate_age(cls, v: int) -> int:
        if v < 16 or v > 100:
            raise ValueError("Age must be between 16 and 100")
        return v

    @validator('incident_hour_of_the_day')
    def validate_hour(cls, v: int) -> int:
        if v < 0 or v > 23:
            raise ValueError("Hour must be between 0 and 23")
        return v

    def to_dataframe(self) -> pd.DataFrame:
        data = self.dict(by_alias=True)
        
        # Add dummy columns
        data['policy_number'] = 'DUMMY'
        data['_c39'] = 0
        
        # Create DataFrame
        df = pd.DataFrame([data])
        
        # Ensure column names match training data
        df = df.rename(columns={
            'capital_gains': 'capital-gains',
            'capital_loss': 'capital-loss'
        })
        
        return df

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "policy_state": "CA",
                "total_claim_amount": 15000.0,
                "capital-gains": 0.0,
                "capital-loss": 0.0,
                "insured_zip": 90001,
                "months_as_customer": 12,
                "number_of_vehicles_involved": 1
            }
        }

def get_risk_factors(claim_df: pd.DataFrame, fraud_probability: float) -> List[Dict]:
    risk_factors = []
    
    if claim_df['total_claim_amount'].iloc[0] > 50000:
        risk_factors.append({
            "factor": "High Claim Amount",
            "severity": "High",
            "description": "Total claim amount is unusually high"
        })
    
    if claim_df['bodily_injuries'].iloc[0] > 2:
        risk_factors.append({
            "factor": "Multiple Injuries",
            "severity": "Medium",
            "description": "Multiple people reported injured"
        })
    
    if claim_df['police_report_available'].iloc[0] == 'NO':
        risk_factors.append({
            "factor": "No Police Report",
            "severity": "Medium",
            "description": "No police report filed"
        })
    
    if fraud_probability > 0.7:
        risk_factors.append({
            "factor": "High Risk Score",
            "severity": "High",
            "description": "ML model indicates high fraud probability"
        })
    
    return risk_factors

@app.post("/api/predict")
async def predict_fraud(claim: ClaimRequest):
    try:
        claim_df = claim.to_dataframe()
        logger.debug(f"Input features: {claim_df.columns.tolist()}")
        
        prediction = model.predict(claim_df)
        fraud_probability = float(prediction[0])
        
        response = {
            "fraud_probability": fraud_probability,
            "is_fraudulent": bool(fraud_probability > 0.5),
            "risk_factors": get_risk_factors(claim_df, fraud_probability),
            "timestamp": datetime.now().isoformat()
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics")
async def get_analytics():
    try:
        data = pd.read_csv('insurance_claims.csv')
        
        return {
            "total_claims": len(data),
            "fraudulent_claims": len(data[data['fraud_reported'] == 'Y']),
            "avg_claim_amount": float(data['total_claim_amount'].mean()),
            "fraud_by_make": data[data['fraud_reported'] == 'Y']['auto_make'].value_counts().to_dict(),
            "fraud_by_type": data[data['fraud_reported'] == 'Y']['incident_type'].value_counts().to_dict()
        }
        
    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)