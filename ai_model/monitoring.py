import pandas as pd
import os

# Load microbial_db.csv once at startup
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
csv_path = os.path.join(base_dir, 'data', 'microbial_db.csv')
microbial_db = pd.read_csv(csv_path)

def monitor_degradation(plastic_type, microbe, elapsed_time, pH, temp):
    """
    Simulate monitoring of plastic degradation progress.
    
    Args:
        plastic_type (str): Type of plastic (e.g., PE, PET, PP)
        microbe (str): Name of the microbe
        elapsed_time (float): Time elapsed (days)
        pH (float): Environmental pH
        temp (float): Environmental temperature (°C)
    
    Returns:
        dict: Estimated degradation progress (e.g., {'progress': 0.5, 'message': '...'})
    """
    try:
        record = microbial_db[(microbial_db['plastic_type'] == plastic_type) & 
                            (microbial_db['microbe'] == microbe)]
        
        if record.empty:
            return {'progress': 0, 'message': f"No data for {microbe} degrading {plastic_type}"}
        
        record = record.iloc[0]
        efficiency = record['efficiency']
        degradation_time = record['degradation_time']
        optimal_pH = record['optimal_pH']
        optimal_temp = record['optimal_temp']
        
        # Adjust progress based on pH and temp deviation from optimal
        pH_factor = 1 - abs(pH - optimal_pH) * 0.1
        temp_factor = 1 - abs(temp - optimal_temp) * 0.05
        base_progress = efficiency * (elapsed_time / degradation_time)
        adjusted_progress = base_progress * pH_factor * temp_factor
        progress = min(max(adjusted_progress, 0), efficiency)
        
        message = f"{microbe} has degraded {progress*100:.1f}% of {plastic_type} in {elapsed_time} days"
        return {'progress': progress, 'message': message}
    
    except Exception as e:
        return {'progress': 0, 'message': f"Error: {str(e)}"}

if __name__ == "__main__":
    result = monitor_degradation('PET', 'Ideonella sakaiensis', 30, 7.2, 32)
    print(result['message'])