import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder

def create_synthetic_data(n_samples=1000):
    """Generate synthetic spectral data for PE, PET, PP."""
    np.random.seed(42)
    features = np.random.rand(n_samples, 10)  # 10 mock spectral bands
    labels = np.random.choice(['PE', 'PET', 'PP'], n_samples)
    return features, labels

def build_model():
    """Build and compile a simple neural network."""
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(10,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(3, activation='softmax')  # 3 classes: PE, PET, PP
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def identify_plastic(features):
    """
    Identify plastic type using a trained TensorFlow model.
    
    Args:
        features (dict): Mock spectral features (e.g., {'band1': 0.5, ...})
    
    Returns:
        str: Plastic type (PE, PET, PP)
    """
    # Load or train model
    X, y = create_synthetic_data()
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    model = build_model()
    model.fit(X, y_encoded, epochs=10, batch_size=32, verbose=0)
    
    # Process input features
    feature_array = np.array([features.get(f'band{i}', 0.5) for i in range(1, 11)]).reshape(1, -1)
    prediction = model.predict(feature_array, verbose=0)
    plastic_type = le.inverse_transform([np.argmax(prediction)])[0]
    
    return plastic_type

if __name__ == "__main__":
    test_features = {f'band{i}': np.random.rand() for i in range(1, 11)}
    plastic_type = identify_plastic(test_features)
    print(f"Identified plastic: {plastic_type}")