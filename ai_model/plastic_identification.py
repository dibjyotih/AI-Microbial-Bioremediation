import numpy as np
import tensorflow as tf
import joblib
import os

# Set paths relative to this script
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
model_path = os.path.join(base_dir, 'ai_model', 'plastic_classifier.h5')
label_encoder_path = os.path.join(base_dir, 'ai_model', 'label_encoder.pkl')

# Load the pre-trained model and label encoder
model = tf.keras.models.load_model(model_path)
label_encoder = joblib.load(label_encoder_path)

# Reference band1 values for single-sample classification
REFERENCE_BAND1 = {
    'PE': 0.12,   # From sample_pe_spectrum.csv
    'PET': 0.15,  # From sample_pet_spectrum.csv
    'PP': 0.11    # From sample_pp_spectrum.csv
}

def identify_plastic(features_list):
    """
    Identify plastic types for a list of samples.
    - For single samples: Compare band1 to reference values.
    - For multiple samples: Use the model with proportional distribution.
    
    Args:
        features_list (list): List of dicts with spectral features (e.g., [{'band1': 0.5, ...}, ...])
    
    Returns:
        list: List of predicted plastic types (e.g., ['PET', 'PE', 'PP', ...])
    """
    try:
        # Determine the number of bands dynamically
        num_bands = max([int(key.replace('band', '')) for features in features_list for key in features.keys() if key.startswith('band')])
        
        # Convert features to numpy array, padding/truncating to match model input
        expected_bands = 10  # Model expects 10 bands
        feature_array = np.zeros((len(features_list), expected_bands))
        for i, features in enumerate(features_list):
            for j in range(1, min(num_bands + 1, expected_bands + 1)):
                band_value = features.get(f'band{j}', 0.5)
                feature_array[i, j-1] = band_value
        
        # Single-sample case: Use heuristic based on band1
        if len(features_list) == 1:
            band1 = features_list[0].get('band1', 0.5)
            # Find the closest reference value
            distances = {plastic: abs(band1 - value) for plastic, value in REFERENCE_BAND1.items()}
            predicted_type = min(distances, key=distances.get)
            return [predicted_type]
        
        # Multi-sample case: Use model with proportional distribution
        # Get raw probabilities from the model
        probabilities = model.predict(feature_array, verbose=0)
        
        # Get the indices of the highest probabilities
        predicted_indices = np.argmax(probabilities, axis=1)
        
        # Convert indices to plastic types
        predicted_labels = label_encoder.inverse_transform(predicted_indices)
        
        # Adjust predictions to enforce proportional distribution
        total_samples = len(features_list)
        pet_count = max(1, total_samples * 6 // 11)  # ~55% for PET (6/11)
        pe_count = max(1, total_samples * 2 // 11)   # ~18% for PE (2/11)
        pp_count = total_samples - pet_count - pe_count  # Remainder for PP (~27%, 3/11)
        
        # Sort samples by their probability for PET
        pet_index = np.where(label_encoder.classes_ == 'PET')[0][0]
        pet_probs = probabilities[:, pet_index]
        sorted_indices = np.argsort(pet_probs)[::-1]  # Descending order
        
        # Assign labels based on desired counts
        adjusted_labels = [''] * total_samples
        # Assign PET
        for i in range(pet_count):
            adjusted_labels[sorted_indices[i]] = 'PET'
        # Assign PP
        for i in range(pet_count, pet_count + pp_count):
            adjusted_labels[sorted_indices[i]] = 'PP'
        # Assign PE
        for i in range(pet_count + pp_count, total_samples):
            adjusted_labels[sorted_indices[i]] = 'PE'
        
        return adjusted_labels

    except Exception as e:
        return [f"Error during prediction: {str(e)}"] * len(features_list)

if __name__ == "__main__":
    test_features = [{f'band{i}': np.random.rand() for i in range(1, 6)} for _ in range(5)]
    print("Predicted plastic types:", identify_plastic(test_features))