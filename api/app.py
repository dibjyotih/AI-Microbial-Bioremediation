import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_model.plastic_identification import identify_plastic
from ai_model.microbial_recommendation import recommend_microbe
from ai_model.monitoring import monitor_degradation
from collections import Counter

app = Flask(__name__)
CORS(app)

@app.route('/identify_plastic', methods=['POST'])
def identify_plastic_endpoint():
    try:
        start = time.time()
        data = request.get_json()

        # Case 1: Input is a list of samples
        if isinstance(data, list):
            if not data:
                return jsonify({'error': 'Empty input list'}), 400

            # Validate all samples have at least band1 and sequential bands
            for sample in data:
                if 'band1' not in sample:
                    return jsonify({'error': 'Each sample must have at least band1'}), 400
                bands = sorted([int(key.replace('band', '')) for key in sample.keys() if key.startswith('band')])
                if bands != list(range(1, len(bands) + 1)):
                    return jsonify({'error': 'Bands must be sequential starting from band1 (e.g., band1, band2, ...)'}), 400

            # Identify plastic types for all samples at once
            predictions = identify_plastic(data)

            # Single-sample case: Simplified response
            if len(data) == 1:
                plastic_type = predictions[0]
                env_pH, env_temp = 7.2, 32
                elapsed_days = 30

                microbe = recommend_microbe(plastic_type, env_pH, env_temp)
                if "Error" in microbe['recommended']:
                    result = {
                        'Plastic_Type': plastic_type,
                        'Recommended_Microbe': microbe['recommended'],
                        'Optimal_pH': str(microbe['optimal_pH']),
                        'Optimal_Temp': f"{microbe['optimal_temp']}°C",
                        'Degradation_Progress': "0%",
                        'Message': "Unable to monitor degradation due to recommendation error"
                    }
                else:
                    degradation = monitor_degradation(
                        plastic_type=plastic_type,
                        microbe=microbe['recommended'],
                        elapsed_time=elapsed_days,
                        pH=microbe['optimal_pH'],
                        temp=microbe['optimal_temp'],
                    )
                    result = {
                        'Plastic_Type': plastic_type,
                        'Recommended_Microbe': microbe['recommended'],
                        'Optimal_pH': str(microbe['optimal_pH']),
                        'Optimal_Temp': f"{microbe['optimal_temp']}°C",
                        'Degradation_Progress': f"{degradation['progress'] * 100:.1f}%",
                        'Message': degradation['message']
                    }

                duration = round((time.time() - start), 3)
                return jsonify({'result': result, 'duration_sec': duration})

            # Multi-sample case: Grouped report
            type_counts = Counter(predictions)
            env_pH, env_temp = 7.2, 32
            elapsed_days = 30
            report = []

            for plastic_type, count in type_counts.items():
                microbe = recommend_microbe(plastic_type, env_pH, env_temp)
                if "Error" in microbe['recommended']:
                    report.append({
                        'Plastic_Type': plastic_type,
                        'count': count,
                        'Recommended_Microbe': microbe['recommended'],
                        'Optimal_pH': str(microbe['optimal_pH']),
                        'Optimal_Temp': f"{microbe['optimal_temp']}°C",
                        'Degradation_Progress': "0%",
                        'Message': "Unable to monitor degradation due to recommendation error"
                    })
                    continue

                degradation = monitor_degradation(
                    plastic_type=plastic_type,
                    microbe=microbe['recommended'],
                    elapsed_time=elapsed_days,
                    pH=microbe['optimal_pH'],
                    temp=microbe['optimal_temp'],
                )

                report.append({
                    'Plastic_Type': plastic_type,
                    'count': count,
                    'Recommended_Microbe': microbe['recommended'],
                    'Optimal_pH': str(microbe['optimal_pH']),
                    'Optimal_Temp': f"{microbe['optimal_temp']}°C",
                    'Degradation_Progress': f"{degradation['progress'] * 100:.1f}%",
                    'Message': degradation['message']
                })

            duration = round((time.time() - start), 3)
            return jsonify({'report': report, 'duration_sec': duration})

        else:
            return jsonify({'error': 'Invalid input format'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommend_microbe', methods=['POST'])
def recommend_microbe_endpoint():
    try:
        data = request.get_json()
        required = ['plastic_type', 'pH', 'temp']
        if not data or not all(k in data for k in required):
            return jsonify({'error': f'Missing fields: {required}'}), 400

        result = recommend_microbe(data['plastic_type'], data['pH'], data['temp'])
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/monitor_degradation', methods=['POST'])
def monitor_degradation_endpoint():
    try:
        data = request.get_json()
        required = ['plastic_type', 'microbe', 'elapsed_time', 'pH', 'temp']
        if not data or not all(k in data for k in required):
            return jsonify({'error': f'Missing fields: {required}'}), 400

        result = monitor_degradation(
            data['plastic_type'],
            data['microbe'],
            data['elapsed_time'],
            data['pH'],
            data['temp']
        )
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)