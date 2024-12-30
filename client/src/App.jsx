import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [formData, setFormData] = useState({
    policy_bind_date: '',
    policy_state: '',
    policy_csl: '',
    policy_deductable: 0,
    policy_annual_premium: 0,
    umbrella_limit: 0,
    insured_sex: '',
    incident_date: '',
    incident_type: '',
    collision_type: '',
    incident_severity: '',
    authorities_contacted: '',
    incident_state: '',
    incident_city: '',
    incident_location: '',
    bodily_injuries: 0,
    witnesses: 0,
    police_report_available: '',
    total_claim_amount: 0,
    injury_claim: 0,
    property_damage: '',
    property_claim: 0,
    vehicle_claim: 0,
    auto_make: '',
    auto_model: '',
    auto_year: 0
  });

  const result = ["Y", "N"];
  const [output, setOutput] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/analytics');
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setOutput(!output);
    try {
      const response = await axios.post('http://localhost:8000/api/predict', formData);
      setPrediction(response.data);
      await fetchAnalytics();
    } catch (error) {
      console.error('Error making prediction:', error);
    }
    setLoading(false);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]:
        typeof prevData[name] === 'number' ? parseFloat(value) || 0 : value
    }));
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-blue-600 text-white p-4">
        <h1 className="text-2xl font-bold">Insurance Fraud Detection System</h1>
      </nav>

      <div className="container mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Analytics Dashboard */}
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-semibold mb-4">Analytics Dashboard</h2>
            {analytics && (
              <div className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-blue-50 p-4 rounded">
                    <h3 className="text-sm text-gray-600">Total Claims</h3>
                    <p className="text-2xl font-bold">{analytics.total_claims}</p>
                  </div>
                  <div className="bg-red-50 p-4 rounded">
                    <h3 className="text-sm text-gray-600">Fraud Rate</h3>
                    <p className="text-2xl font-bold">
                      {((analytics.fraudulent_claims * 100) / analytics.total_claims).toFixed(1)}%
                    </p>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-2">Fraud by Vehicle Make</h3>
                  <Bar
                    data={{
                      labels: Object.keys(analytics.fraud_by_make),
                      datasets: [
                        {
                          label: 'Fraudulent Claims',
                          data: Object.values(analytics.fraud_by_make),
                          backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        },
                      ],
                    }}
                  />
                </div>
              </div>
            )}
          </div>

          {/* Claim Form */}
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-semibold mb-4">Submit New Claim</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                {Object.keys(formData).map((key) => (
                  <div key={key} className="flex flex-col">
                    <label className="text-sm text-gray-600">
                      {key} ({typeof formData[key]})
                    </label>
                    <input
                      type={typeof formData[key] === 'number' ? 'number' : 'text'}
                      name={key}
                      value={formData[key]}
                      onChange={handleInputChange}
                      className="p-2 border rounded"

                    />
                  </div>
                ))}
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:bg-blue-300"
              >
                {loading ? 'Analyzing...' : 'Analyze Claim'}
              </button>
            </form>
            {output && (
              <div>
                <p className="text-[100px] text-black">{result[Math.floor(Math.random() * result.length)]}</p>
              </div>
            )}

            {prediction && (
              <div
                className={`mt-4 p-4 rounded ${prediction.is_fraudulent ? 'bg-red-100' : 'bg-green-100'
                  }`}
              >
                <h3 className="font-semibold mb-2">Prediction Result</h3>
                <p className="mb-2">
                  Fraud Probability: {(prediction.fraud_probability * 100).toFixed(1)}%
                </p>
                <p className="mb-4">
                  Status: {prediction.is_fraudulent ? 'Suspicious' : 'Legitimate'}
                </p>

                {prediction.risk_factors.length > 0 && (
                  <div>
                    <h4 className="font-semibold mb-2">Risk Factors:</h4>
                    <ul className="list-disc pl-5">
                      {prediction.risk_factors.map((factor, index) => (
                        <li key={index} className="mb-1">
                          <span className="font-medium">{factor.factor}</span>: {factor.description}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
