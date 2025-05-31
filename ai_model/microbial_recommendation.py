import pandas as pd
import numpy as np
import os

# Load microbial_db.csv once at startup
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
csv_path = os.path.join(base_dir, 'data', 'microbial_db.csv')
try:
    microbial_db = pd.read_csv(csv_path)
except FileNotFoundError:
    microbial_db = pd.DataFrame()  # Empty DataFrame to prevent crashes

def recommend_microbe(plastic_type, pH, temp):
    """
    Recommend the best microbe for a given plastic type based on pH and temperature.
    
    Args:
        plastic_type (str): Type of plastic (e.g., PE, PET, PP)
        pH (float): Environmental pH
        temp (float): Environmental temperature (°C)
    
    Returns:
        dict: {'recommended': str, 'optimal_pH': float, 'optimal_temp': float}
    """
    try:
        if microbial_db.empty:
            return {'recommended': "Error: microbial_db.csv not found", 'optimal_pH': 0.0, 'optimal_temp': 0.0}

        suitable_microbes = microbial_db[microbial_db['plastic_type'] == plastic_type]
        
        if suitable_microbes.empty:
            return {
                'recommended': f"No suitable microbe found for {plastic_type}",
                'optimal_pH': 0.0,
                'optimal_temp': 0.0
            }
        
        scores = []
        for _, row in suitable_microbes.iterrows():
            pH_diff = abs(row['optimal_pH'] - pH)
            temp_diff = abs(row['optimal_temp'] - temp)
            score = row['efficiency'] / (1 + pH_diff + temp_diff)
            scores.append(score)
        
        best_index = np.argmax(scores)
        best_row = suitable_microbes.iloc[best_index]
        return {
            'recommended': best_row['microbe'],
            'optimal_pH': float(best_row['optimal_pH']),
            'optimal_temp': float(best_row['optimal_temp'])
        }
    
    except Exception as e:
        return {
            'recommended': f"Error: {str(e)}",
            'optimal_pH': 0.0,
            'optimal_temp': 0.0
        }

if __name__ == "__main__":
    plastic = 'PET'
    pH = 7.2
    temp = 32
    result = recommend_microbe(plastic, pH, temp)
    print(f"Recommended microbe for {plastic}: {result['recommended']}")