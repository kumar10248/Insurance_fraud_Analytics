
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

1. Navigate to the 

client

 directory:
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

```
insurance-fraud-detection/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── services/
│       └── ml_service.py
├── client/
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── postcss.config.js
│   ├── public/
│   ├── README.md
│   ├── src/
│   │   ├── App.jsx
│   │   ├── assets/
│   │   ├── index.css
│   │   └── main.jsx
│   ├── tailwind.config.js
│   └── vite.config.js
├── insurance_claims.csv
├── model.ipynb
├── model.py
└── models/
    ├── best_model.keras
    ├── fraud_model.keras
    ├── label_encoders.pkl
    ├── scaler.pkl
    └── target_encoder.pkl
```

## License

This project is licensed under the MIT License.
```

This `README.md` file provides a comprehensive guide to your project, including installation instructions, usage, and API documentation.
This `README.md` file provides a comprehensive guide to your project, including installation instructions, usage, and API documentation.

kumar10248: include video link: https://www.loom.com/share/bed0f00237fd4510b169f77ec4598f50

Workspace: Collecting workspace information

Here is the updated 

README.md

 file with the video link included:

```md
# Insurance Fraud Detection System

This project is an Insurance Fraud Detection System that uses a machine learning model to predict the probability of fraud in insurance claims. The system includes a backend API built with FastAPI and a frontend client built with React and Vite.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Demo Video](#demo-video)

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

1. Navigate to the 

client

 directory:
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

```
insurance-fraud-detection/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── services/
│       └── ml_service.py
├── client/
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── postcss.config.js
│   ├── public/
│   ├── README.md
│   ├── src/
│   │   ├── App.jsx
│   │   ├── assets/
│   │   ├── index.css
│   │   └── main.jsx
│   ├── tailwind.config.js
│   └── vite.config.js
├── insurance_claims.csv
├── model.ipynb
├── model.py
└── models/
    ├── best_model.keras
    ├── fraud_model.keras
    ├── label_encoders.pkl
    ├── scaler.pkl
    └── target_encoder.pkl
```

## Demo Video

Watch the demo video to see the Insurance Fraud Detection System in action: [Loom Video](https://www.loom.com/share/bed0f00237fd4510b169f77ec4598f50)

## License

This project is licensed under the MIT License.
```

This `README.md` file now includes a link to the demo video.
This `README.md` file now includes a link to the demo video.