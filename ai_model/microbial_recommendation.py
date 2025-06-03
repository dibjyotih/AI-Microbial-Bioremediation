import pandas as pd
import numpy as np
import os

# Load microbial database once at startup
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
csv_path = os.path.join(base_dir, 'data', 'microbial_db.csv')
try:
    microbial_db = pd.read_csv(csv_path)
    # Normalize plastic type to uppercase without spaces
    microbial_db['plastic_type'] = microbial_db['plastic_type'].str.strip().str.upper()
except FileNotFoundError:
    microbial_db = pd.DataFrame()

def recommend_microbe(plastic_type, pH, temp):
    """
    Recommend best-fit microbe for given plastic type using environmental pH/temp.
    Returns: dict with recommended microbe, optimal pH/temp
    """
    try:
        if microbial_db.empty:
            return {'recommended': "Error: Database not found", 'optimal_pH': 0.0, 'optimal_temp': 0.0}

        # Normalize input plastic type
        plastic_type = plastic_type.strip().upper()
        suitable_microbes = microbial_db[microbial_db['plastic_type'] == plastic_type]

        if suitable_microbes.empty:
            return {
                'recommended': f"No microbe found for {plastic_type}",
                'optimal_pH': 0.0,
                'optimal_temp': 0.0
            }

        # Score microbes based on environment match
        scores = []
        for _, row in suitable_microbes.iterrows():
            pH_diff = abs(row['optimal_pH'] - pH)
            temp_diff = abs(row['optimal_temp'] - temp)
            score = row['efficiency'] / (1 + pH_diff + temp_diff)
            scores.append(score)

        if not scores:
            return {
                'recommended': f"No suitable microbe match found for {plastic_type} at provided conditions.",
                'optimal_pH': 0.0,
                'optimal_temp': 0.0
            }

        best_index = int(np.argmax(scores))
        best_row = suitable_microbes.iloc[best_index]

        return {
            'recommended': best_row['microbe'],
            'optimal_pH': float(best_row['optimal_pH']),
            'optimal_temp': float(best_row['optimal_temp'])
        }

    except Exception as e:
        return {'recommended': f"Error: {str(e)}", 'optimal_pH': 0.0, 'optimal_temp': 0.0}

if __name__ == "__main__":
    result = recommend_microbe('PET', 7.2, 32)
    print(f"Recommended microbe for PET: {result['recommended']}")
