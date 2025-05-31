import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore
from ai_model.plastic_identification import identify_plastic
from ai_model.microbial_recommendation import recommend_microbe
from ai_model.monitoring import monitor_degradation

app = Flask(__name__)
CORS(app)  # Allow frontend to connect

@app.route('/identify_plastic', methods=['POST'])
def identify_plastic_endpoint():
    """
    API endpoint to identify plastic type from features.
    Expects JSON: {'band1': float, 'band2': float, ..., 'band10': float}
    """
    try:
        data = request.get_json()
        if not data or not all(f'band{i}' in data for i in range(1, 11)):
            return jsonify({'error': 'Missing spectral bands'}), 400
        
        plastic_type = identify_plastic(data)
        return jsonify({'plastic_type': plastic_type})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommend_microbe', methods=['POST'])
def recommend_microbe_endpoint():
    """
    API endpoint to recommend a microbe.
    Expects JSON: {'plastic_type': str, 'pH': float, 'temp': float}
    """
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['plastic_type', 'pH', 'temp']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        result = recommend_microbe(data['plastic_type'], data['pH'], data['temp'])
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/monitor_degradation', methods=['POST'])
def monitor_degradation_endpoint():
    """
    API endpoint to monitor degradation progress.
    Expects JSON: {'plastic_type': str, 'microbe': str, 'elapsed_time': float, 'pH': float, 'temp': float}
    """
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['plastic_type', 'microbe', 'elapsed_time', 'pH', 'temp']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        result = monitor_degradation(data['plastic_type'], data['microbe'], data['elapsed_time'], data['pH'], data['temp'])
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)