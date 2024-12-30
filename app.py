from flask import Flask, request, jsonify
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Load the trained model and scaler
model = load_model('insurance_fraud_model.h5')
scaler = joblib.load('scaler.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the features from the request
        data = request.get_json()

        # Convert the features to a NumPy array
        features = np.array(data['features']).reshape(1, -1)

        # Ensure the features match the expected number of columns (39)
        if features.shape[1] != 39:
            return jsonify({"error": f"Expected 39 features, but got {features.shape[1]} features."}), 400
        
        # Scale the features using the loaded scaler
        scaled_features = scaler.transform(features)

        # Make prediction
        prediction = model.predict(scaled_features)

        # Convert the result from float32 to standard Python float for serialization
        prediction_value = float(prediction[0])  # Extract the first value from the prediction

        # Return the result
        response = {
            "fraud_probability": prediction_value,
            "result": "Fraud" if prediction_value > 0.5 else "Legitimate"
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
