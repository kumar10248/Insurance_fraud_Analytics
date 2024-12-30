# Insurance Fraud Detection System

This project is an Insurance Fraud Detection System that uses a machine learning model to predict the probability of fraud in insurance claims. The system includes a backend API built with FastAPI and a frontend client built with React and Vite.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)

## Features

- Predicts the probability of fraud in insurance claims.
- Provides risk factors associated with the prediction.
- Frontend client to interact with the API.
- Logging and error handling.

## Requirements

- Python 3.8+
- Node.js 14+
- npm 6+

## Installation

### Backend

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/insurance-fraud-detection.git
    cd insurance-fraud-detection
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the backend server:
    ```sh
    uvicorn app.main:app --reload
    ```

### Frontend

1. Navigate to the [client](http://_vscodecontentref_/1) directory:
    ```sh
    cd client
    ```

2. Install the required npm packages:
    ```sh
    npm install
    ```

3. Run the frontend development server:
    ```sh
    npm run dev
    ```

## Usage

1. Ensure the backend server is running.
2. Open your browser and navigate to `http://localhost:3000` to access the frontend client.
3. Use the frontend client to submit insurance claims and receive fraud predictions.

## API Documentation

### POST /api/predict

Predicts the probability of fraud in an insurance claim.

- **URL:** `/api/predict`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "claim": {
            "feature1": "value1",
            "feature2": "value2",
            ...
        }
    }
    ```
- **Response:**
    ```json
    {
        "fraud_probability": 0.85,
        "is_fraudulent": true,
        "risk_factors": [
            {
                "factor": "High Risk Score",
                "severity": "High",
                "description": "ML model indicates high fraud probability"
            }
        ],
        "timestamp": "2023-10-01T12:34:56.789Z"
    }
    ```

## Project Structure
