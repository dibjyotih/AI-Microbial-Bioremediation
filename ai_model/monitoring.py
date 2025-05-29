import pandas as pd

def monitor_degradation(plastic_type, microbe, elapsed_time):
    """
    Simulate monitoring of plastic degradation progress.
    
    Args:
        plastic_type (str): Type of plastic (e.g., PE, PET, PP)
        microbe (str): Name of the microbe
        elapsed_time (float): Time elapsed (days)
    
    Returns:
        dict: Estimated degradation progress (e.g., {'progress': 0.5, 'message': '...'})
    """
    try:
        microbial_db = pd.read_csv('data/microbial_db.csv')
        record = microbial_db[(microbial_db['plastic_type'] == plastic_type) & 
                            (microbial_db['microbe'] == microbe)]
        
        if record.empty:
            return {'progress': 0, 'message': f"No data for {microbe} degrading {plastic_type}"}
        
        efficiency = record.iloc[0]['efficiency']
        degradation_time = record.iloc[0]['degradation_time']
        
        progress = min(efficiency * (elapsed_time / degradation_time), efficiency)
        message = f"{microbe} has degraded {progress*100:.1f}% of {plastic_type} in {elapsed_time} days"
        
        return {'progress': progress, 'message': message}
    
    except FileNotFoundError:
        return {'progress': 0, 'message': "Error: microbial_db.csv not found"}
    except Exception as e:
        return {'progress': 0, 'message': f"Error: {str(e)}"}

if __name__ == "__main__":
    result = monitor_degradation('PET', 'Ideonella sakaiensis', 30)
    print(result['message'])