import pandas as pd
import numpy as np

def recommend_microbe(plastic_type, pH, temp):
    """
    Recommend the best microbe for a given plastic type based on pH and temperature.
    
    Args:
        plastic_type (str): Type of plastic (e.g., PE, PET, PP)
        pH (float): Environmental pH
        temp (float): Environmental temperature (°C)
    
    Returns:
        str: Name of the recommended microbe or error message
    """
    try:
        microbial_db = pd.read_csv('data/microbial_db.csv')
        suitable_microbes = microbial_db[microbial_db['plastic_type'] == plastic_type]
        
        if suitable_microbes.empty:
            return f"No suitable microbe found for {plastic_type}"
        
        scores = []
        for _, row in suitable_microbes.iterrows():
            pH_diff = abs(row['optimal_pH'] - pH)
            temp_diff = abs(row['optimal_temp'] - temp)
            score = row['efficiency'] / (1 + pH_diff + temp_diff)
            scores.append(score)
        
        best_index = np.argmax(scores)
        best_microbe = suitable_microbes.iloc[best_index]['microbe']
        return best_microbe
    
    except FileNotFoundError:
        return "Error: microbial_db.csv not found in data/ directory"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    plastic = 'PET'
    pH = 7.2
    temp = 32
    microbe = recommend_microbe(plastic, pH, temp)
    print(f"Recommended microbe for {plastic}: {microbe}")