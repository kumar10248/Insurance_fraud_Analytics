# app/services/ml_service.py
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MLService:
    def __init__(self):
        self._load_model()
        self._load_preprocessors()
        
    def _load_model(self):
        try:
            self.model = tf.keras.models.load_model('models/insurance_fraud_model.h5')
            logger.info("ML model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
            
    def _load_preprocessors(self):
        try:
            self.scaler = joblib.load('models/scaler.pkl')
            self.label_encoders = joblib.load('models/label_encoders.pkl')
            logger.info("Preprocessors loaded successfully")
        except Exception as e:
            logger.error(f"Error loading preprocessors: {str(e)}")
            raise
    
    def _preprocess_claim(self, claim_data: dict) -> np.ndarray:
        try:
            # Convert to DataFrame
            df = pd.DataFrame([claim_data])
            
            # Handle dates
            for date_col in ['policy_bind_date', 'incident_date']:
                df[date_col] = pd.to_datetime(df[date_col])
                df[f'{date_col}_year'] = df[date_col].dt.year
                df[f'{date_col}_month'] = df[date_col].dt.month
                df[f'{date_col}_day'] = df[date_col].dt.day
                df.drop(date_col, axis=1, inplace=True)
            
            # Encode categorical variables
            for col, encoder in self.label_encoders.items():
                if col in df.columns:
                    df[col] = encoder.transform(df[col].astype(str))
            
            # Scale features
            return self.scaler.transform(df)
        except Exception as e:
            logger.error(f"Error in preprocessing: {str(e)}")
            raise
    
    def predict(self, claim_data: dict) -> dict:
        try:
            # Preprocess the claim data
            features = self._preprocess_claim(claim_data)
            
            # Make prediction
            fraud_probability = float(self.model.predict(features)[0][0])
            
            # Determine risk factors
            risk_factors = self._analyze_risk_factors(claim_data, fraud_probability)
            
            return {
                'fraud_probability': fraud_probability,
                'is_fraudulent': fraud_probability > 0.5,
                'risk_factors': risk_factors
            }
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            raise
            
    def _analyze_risk_factors(self, claim_data: dict, fraud_probability: float) -> list:
        risk_factors = []
        
        # Check for high claim amounts
        if claim_data['total_claim_amount'] > 50000:
            risk_factors.append("High total claim amount")
            
        # Check for multiple vehicles
        if claim_data['number_of_vehicles_involved'] > 2:
            risk_factors.append("Multiple vehicles involved")
            
        # Check for bodily injuries
        if claim_data['bodily_injuries'] > 0:
            risk_factors.append("Bodily injuries reported")
            
        # Check for property damage
        if claim_data['property_damage'] == 'YES':
            risk_factors.append("Property damage reported")
            
        # Check for major incident severity
        if claim_data['incident_severity'] == 'Major Damage':
            risk_factors.append("Major damage reported")
            
        return risk_factors