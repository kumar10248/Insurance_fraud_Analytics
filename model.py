import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import logging
import os
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class InsuranceFraudModel:
    """Insurance fraud detection model using neural networks."""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model: Optional[Sequential] = None
        self.label_encoders: Dict[str, LabelEncoder] = {}
        self.scaler = StandardScaler()
        self.target_encoder = LabelEncoder()
        Path('models').mkdir(exist_ok=True)
        if model_path:
            self.load_model(model_path)

    def load_model(self, model_path: str) -> None:
        try:
            self.model = load_model(model_path)
            self.scaler = joblib.load('models/scaler.pkl')
            self.label_encoders = joblib.load('models/label_encoders.pkl')
            self.target_encoder = joblib.load('models/target_encoder.pkl')
            logger.info(f"Model loaded from {model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise

    def save_model(self) -> None:
        try:
            self.model.save('models/fraud_model.keras')
            joblib.dump(self.scaler, 'models/scaler.pkl')
            joblib.dump(self.label_encoders, 'models/label_encoders.pkl')
            joblib.dump(self.target_encoder, 'models/target_encoder.pkl')
            logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            processed_data = data.copy()

            # Handle dates
            date_columns = ['policy_bind_date', 'incident_date']
            for col in date_columns:
                processed_data[col] = pd.to_datetime(processed_data[col])
                processed_data[f'{col}_year'] = processed_data[col].dt.year
                processed_data[f'{col}_month'] = processed_data[col].dt.month
                processed_data[f'{col}_day'] = processed_data[col].dt.day
            processed_data.drop(date_columns, axis=1, inplace=True)

            # Drop unnecessary columns
            processed_data.drop(['policy_number', '_c39'], axis=1, inplace=True)

            # Handle missing values
            numeric_cols = processed_data.select_dtypes(include=[np.number]).columns
            processed_data[numeric_cols] = processed_data[numeric_cols].fillna(processed_data[numeric_cols].mean())

            categorical_cols = processed_data.select_dtypes(include=['object']).columns
            processed_data[categorical_cols] = processed_data[categorical_cols].fillna(processed_data[categorical_cols].mode().iloc[0])

            # Encode target
            if 'fraud_reported' in processed_data.columns:
                processed_data['fraud_reported'] = self.target_encoder.fit_transform(processed_data['fraud_reported'])

            # Encode categories
            for col in categorical_cols:
                if col != 'fraud_reported':
                    le = LabelEncoder()
                    processed_data[col] = le.fit_transform(processed_data[col])
                    self.label_encoders[col] = le

            return processed_data
        except Exception as e:
            logger.error(f"Error in preprocessing: {e}")
            raise

    def build_model(self, input_dim: int) -> Sequential:
        try:
            model = Sequential([
                Dense(256, activation='relu', input_dim=input_dim),
                BatchNormalization(),
                Dropout(0.3),
                Dense(128, activation='relu'),
                BatchNormalization(),
                Dropout(0.3),
                Dense(64, activation='relu'),
                BatchNormalization(),
                Dropout(0.3),
                Dense(32, activation='relu'),
                Dense(1, activation='sigmoid')
            ])

            model.compile(
                optimizer=tf.keras.optimizers.Adam(0.001),
                loss='binary_crossentropy',
                metrics=['accuracy', tf.keras.metrics.AUC()]
            )
            return model
        except Exception as e:
            logger.error(f"Error building model: {e}")
            raise

    def train(self, data_path: str, epochs: int = 50, batch_size: int = 32) -> Any:
        try:
            # Load and process data
            data = pd.read_csv(data_path)
            processed_data = self.preprocess_data(data)

            # Split data
            X = processed_data.drop('fraud_reported', axis=1)
            y = processed_data['fraud_reported'].values

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )

            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)

            # Build and train
            self.model = self.build_model(X_train.shape[1])
            
            class_weights = {
                0: len(y) / (2 * np.sum(y == 0)),
                1: len(y) / (2 * np.sum(y == 1))
            }

            callbacks = [
                tf.keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    patience=5,
                    restore_best_weights=True
                ),
                tf.keras.callbacks.ModelCheckpoint(
                    filepath='models/best_model.keras',
                    monitor='val_loss',
                    save_best_only=True
                )
            ]

            history = self.model.fit(
                X_train_scaled, y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_data=(X_test_scaled, y_test),
                class_weight=class_weights,
                callbacks=callbacks,
                verbose=1
            )

            self.save_model()
            return history

        except Exception as e:
            logger.error(f"Error in training: {e}")
            raise

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        try:
            if self.model is None:
                raise ValueError("Model not trained")
            
            processed_X = self.preprocess_data(X)
            if 'fraud_reported' in processed_X.columns:
                processed_X = processed_X.drop('fraud_reported', axis=1)
                
            X_scaled = self.scaler.transform(processed_X)
            return (self.model.predict(X_scaled) > 0.5).astype(int)
        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            raise

if __name__ == "__main__":
    try:
        model = InsuranceFraudModel()
        history = model.train('insurance_claims.csv')
        logger.info("Training completed successfully")
    except Exception as e:
        logger.error(f"Training failed: {e}")