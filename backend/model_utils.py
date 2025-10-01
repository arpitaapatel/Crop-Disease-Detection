"""
Model utilities for loading and preprocessing images
"""

import tensorflow as tf
import numpy as np
from PIL import Image
import os
import logging

logger = logging.getLogger(__name__)

def load_model(model_path: str):
    """
    Load the trained model from file
    
    Args:
        model_path: Path to the model file
        
    Returns:
        Loaded TensorFlow model
    """
    try:
        if not os.path.exists(model_path):
            logger.warning(f"Model file not found at {model_path}. Creating a dummy model for testing.")
            return create_dummy_model()
        
        model = tf.keras.models.load_model(model_path)
        logger.info(f"Model loaded successfully from {model_path}")
        return model
        
    except Exception as e:
        logger.error(f"Failed to load model from {model_path}: {str(e)}")
        logger.info("Creating a dummy model for testing")
        return create_dummy_model()

def create_dummy_model():
    """
    Create a dummy model for testing when the actual model is not available
    
    Returns:
        Dummy TensorFlow model
    """
    # Create a simple dummy model that returns random predictions
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(224, 224, 3)),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(85, activation='softmax')  # 85 comprehensive disease classes
    ])
    
    # Compile the model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    logger.info("Dummy model created for testing")
    return model

def preprocess_image(image: Image.Image, target_size: tuple = (224, 224)) -> np.ndarray:
    """
    Preprocess image for model inference
    
    Args:
        image: PIL Image object
        target_size: Target size for resizing (width, height)
        
    Returns:
        Preprocessed image array ready for model input
    """
    try:
        # Resize image
        image = image.resize(target_size)
        
        # Convert to numpy array
        image_array = np.array(image)
        
        # Normalize pixel values to [0, 1]
        image_array = image_array.astype(np.float32) / 255.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
        
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        raise e

def get_model_summary(model):
    """
    Print model summary
    
    Args:
        model: TensorFlow model
    """
    try:
        model.summary()
    except Exception as e:
        logger.error(f"Error printing model summary: {str(e)}")
