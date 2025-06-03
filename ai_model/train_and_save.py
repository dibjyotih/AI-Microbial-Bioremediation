import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import joblib

# Create synthetic dataset
X = np.random.rand(500, 10)
y = np.random.choice(['PE', 'PET', 'PP'], size=500)

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Save label encoder
joblib.dump(le, 'label_encoder.pkl')

# Define and train model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu', input_shape=(10,)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X, y_encoded, epochs=5, batch_size=64, verbose=1)

# Save model
model.save('plastic_classifier.h5')
