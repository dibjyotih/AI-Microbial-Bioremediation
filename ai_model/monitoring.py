import pandas as pd
import os

# Load microbial database
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
csv_path = os.path.join(base_dir, 'data', 'microbial_db.csv')
microbial_db = pd.read_csv(csv_path)

def monitor_degradation(plastic_type, microbe, elapsed_time, pH, temp):
    """
    Simulate microbial degradation of plastic over time.

    Returns:
        dict: {
            'progress': float (0 to 1),
            'message': str
        }
    """
    try:
        match = microbial_db.query(
            "plastic_type == @plastic_type and microbe == @microbe"
        )

        if match.empty:
            return {'progress': 0, 'message': f"No data for {microbe} degrading {plastic_type}"}

        row = match.iloc[0]
        efficiency = row['efficiency']
        degradation_time = row['degradation_time']
        optimal_pH = row['optimal_pH']
        optimal_temp = row['optimal_temp']

        # Compute degradation modifiers
        pH_factor = max(0, 1 - abs(pH - optimal_pH) * 0.1)
        temp_factor = max(0, 1 - abs(temp - optimal_temp) * 0.05)

        base_progress = efficiency * (elapsed_time / degradation_time)
        adjusted_progress = base_progress * pH_factor * temp_factor
        progress = min(max(adjusted_progress, 0), efficiency)

        return {
            'progress': round(progress, 4),
            'message': f"{microbe} has degraded {progress * 100:.1f}% of {plastic_type} in {elapsed_time} days"
        }

    except Exception as e:
        return {'progress': 0, 'message': f"Error: {str(e)}"}

if __name__ == "__main__":
    print(monitor_degradation("PET", "Ideonella sakaiensis", 30, 7.2, 32)["message"])
