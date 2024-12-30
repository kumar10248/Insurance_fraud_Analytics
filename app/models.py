# app/models.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ClaimInput(BaseModel):
    months_as_customer: int = Field(..., ge=0)
    age: int = Field(..., ge=16, le=120)
    policy_number: str
    policy_bind_date: str
    policy_state: str
    policy_csl: str
    policy_deductable: float
    policy_annual_premium: float
    umbrella_limit: int
    insured_zip: int
    insured_sex: str
    insured_education_level: str
    insured_occupation: str
    insured_hobbies: str
    insured_relationship: str
    capital_gains: float
    capital_loss: float
    incident_date: str
    incident_type: str
    collision_type: Optional[str]
    incident_severity: str
    authorities_contacted: str
    incident_state: str
    incident_city: str
    incident_location: str
    incident_hour_of_the_day: int = Field(..., ge=0, le=23)
    number_of_vehicles_involved: int = Field(..., ge=1)
    property_damage: str
    bodily_injuries: int
    witnesses: int
    police_report_available: str
    total_claim_amount: float
    injury_claim: float
    property_claim: float
    vehicle_claim: float
    auto_make: str
    auto_model: str
    auto_year: int = Field(..., ge=1900)

class PredictionResponse(BaseModel):
    claim_id: str
    prediction_timestamp: datetime
    fraud_probability: float
    is_fraudulent: bool
    risk_factors: list[str]
    total_claim_amount: float

class AnalyticsResponse(BaseModel):
    total_claims: int
    fraudulent_claims: int
    fraud_rate: float
    total_claim_amount: float
    average_claim_amount: float
    claims_by_state: dict
    fraud_by_vehicle_make: dict
    high_risk_indicators: list[str]