"""
Training script for fine-tuning MobileNetV2 on PlantVillage dataset
"""

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
    "image_size": (224, 224),
    "batch_size": 32,
    "epochs": 50,
    "learning_rate": 0.001,
    "num_classes": 85,  # Expanded number of disease classes
    "data_dir": "data/comprehensive_crop_diseases",  # Path to comprehensive dataset
    "model_save_path": "../models/comprehensive_model.h5",
    "class_names": [
        # CEREALS - Wheat (4)
        "Wheat Rust", "Wheat Blast", "Wheat Scab", "Wheat Healthy",
        # CEREALS - Rice (4)
        "Rice Blast", "Rice Brown Spot", "Rice Bacterial Blight", "Rice Healthy",
        # CEREALS - Corn (5)
        "Corn Northern Leaf Blight", "Corn Common Rust", "Corn Gray Leaf Spot", "Corn Southern Rust", "Corn Healthy",
        # CEREALS - Barley (3)
        "Barley Scald", "Barley Net Blotch", "Barley Healthy",
        # VEGETABLES - Tomato (10)
        "Tomato Bacterial Spot", "Tomato Early Blight", "Tomato Late Blight", "Tomato Leaf Mold",
        "Tomato Septoria Leaf Spot", "Tomato Spider Mites", "Tomato Target Spot",
        "Tomato Yellow Leaf Curl Virus", "Tomato Mosaic Virus", "Tomato Healthy",
        # VEGETABLES - Potato (5)
        "Potato Early Blight", "Potato Late Blight", "Potato Scab", "Potato Blackleg", "Potato Healthy",
        # VEGETABLES - Pepper (3)
        "Pepper Bacterial Spot", "Pepper Anthracnose", "Pepper Healthy",
        # VEGETABLES - Cucumber (4)
        "Cucumber Downy Mildew", "Cucumber Powdery Mildew", "Cucumber Anthracnose", "Cucumber Healthy",
        # VEGETABLES - Lettuce (3)
        "Lettuce Downy Mildew", "Lettuce Bacterial Soft Rot", "Lettuce Healthy",
        # VEGETABLES - Carrot (3)
        "Carrot Leaf Blight", "Carrot Root Rot", "Carrot Healthy",
        # FRUITS - Apple (4)
        "Apple Scab", "Apple Fire Blight", "Apple Powdery Mildew", "Apple Healthy",
        # FRUITS - Citrus (4)
        "Citrus Canker", "Citrus Greening", "Citrus Melanose", "Citrus Healthy",
        # FRUITS - Grape (4)
        "Grape Downy Mildew", "Grape Powdery Mildew", "Grape Black Rot", "Grape Healthy",
        # FRUITS - Strawberry (4)
        "Strawberry Powdery Mildew", "Strawberry Gray Mold", "Strawberry Anthracnose", "Strawberry Healthy",
        # LEGUMES - Soybean (3)
        "Soybean Rust", "Soybean Bacterial Blight", "Soybean Healthy",
        # LEGUMES - Bean (3)
        "Bean Anthracnose", "Bean Rust", "Bean Healthy",
        # ROOT CROPS - Sweet Potato (2)
        "Sweet Potato Scab", "Sweet Potato Healthy",
        # ROOT CROPS - Cassava (3)
        "Cassava Mosaic Disease", "Cassava Brown Streak Disease", "Cassava Healthy"
    ]
}

def create_model(num_classes: int, input_shape: tuple = (224, 224, 3)):
    """
    Create MobileNetV2 model for crop disease classification
    
    Args:
        num_classes: Number of output classes
        input_shape: Input image shape
        
    Returns:
        Compiled Keras model
    """
    # Load pre-trained MobileNetV2
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=input_shape
    )
    
    # Freeze base model layers
    base_model.trainable = False
    
    # Add custom classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    # Create the model
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Compile the model
    model.compile(
        optimizer=Adam(learning_rate=CONFIG["learning_rate"]),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def create_data_generators(data_dir: str, image_size: tuple, batch_size: int):
    """
    Create data generators for training and validation
    
    Args:
        data_dir: Path to dataset directory
        image_size: Target image size
        batch_size: Batch size for training
        
    Returns:
        Tuple of (train_generator, validation_generator)
    """
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        shear_range=0.2,
        fill_mode='nearest',
        validation_split=0.2  # Use 20% for validation
    )
    
    # No augmentation for validation
    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )
    
    # Training generator
    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    # Validation generator
    val_generator = val_datagen.flow_from_directory(
        data_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    return train_generator, val_generator

def train_model():
    """
    Train the MobileNetV2 model on PlantVillage dataset
    """
    logger.info("Starting model training...")
    
    # Check if data directory exists
    if not os.path.exists(CONFIG["data_dir"]):
        logger.warning(f"Data directory {CONFIG['data_dir']} not found. Creating dummy data for demonstration.")
        create_dummy_dataset()
    
    # Create model
    logger.info("Creating model...")
    model = create_model(CONFIG["num_classes"], CONFIG["image_size"] + (3,))
    
    # Print model summary
    model.summary()
    
    # Create data generators
    logger.info("Creating data generators...")
    train_generator, val_generator = create_data_generators(
        CONFIG["data_dir"],
        CONFIG["image_size"],
        CONFIG["batch_size"]
    )
    
    # Create callbacks
    callbacks = [
        ModelCheckpoint(
            CONFIG["model_save_path"],
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        EarlyStopping(
            monitor='val_accuracy',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Train the model
    logger.info("Starting training...")
    history = model.fit(
        train_generator,
        epochs=CONFIG["epochs"],
        validation_data=val_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save class names
    class_names_path = os.path.join(os.path.dirname(CONFIG["model_save_path"]), "class_names.json")
    with open(class_names_path, 'w') as f:
        json.dump(CONFIG["class_names"], f)
    
    logger.info(f"Training completed! Model saved to {CONFIG['model_save_path']}")
    
    return history

def create_dummy_dataset():
    """
    Create a dummy dataset for demonstration purposes
    """
    logger.info("Creating dummy dataset for demonstration...")
    
    # Create directory structure
    os.makedirs(CONFIG["data_dir"], exist_ok=True)
    
    # Create dummy images for each class
    for i, class_name in enumerate(CONFIG["class_names"]):
        class_dir = os.path.join(CONFIG["data_dir"], class_name)
        os.makedirs(class_dir, exist_ok=True)
        
        # Create 10 dummy images per class
        for j in range(10):
            # Create a random image
            dummy_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
            
            # Save as image
            from PIL import Image
            img = Image.fromarray(dummy_image)
            img_path = os.path.join(class_dir, f"dummy_{j}.jpg")
            img.save(img_path)
    
    logger.info("Dummy dataset created successfully!")

def fine_tune_model(model_path: str, epochs: int = 10):
    """
    Fine-tune the pre-trained model by unfreezing some layers
    
    Args:
        model_path: Path to the saved model
        epochs: Number of epochs for fine-tuning
    """
    logger.info("Starting fine-tuning...")
    
    # Load the model
    model = tf.keras.models.load_model(model_path)
    
    # Unfreeze some layers for fine-tuning
    for layer in model.layers[-20:]:  # Unfreeze last 20 layers
        layer.trainable = True
    
    # Recompile with lower learning rate
    model.compile(
        optimizer=Adam(learning_rate=CONFIG["learning_rate"] * 0.1),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Create data generators
    train_generator, val_generator = create_data_generators(
        CONFIG["data_dir"],
        CONFIG["image_size"],
        CONFIG["batch_size"]
    )
    
    # Fine-tune
    history = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=val_generator,
        verbose=1
    )
    
    # Save fine-tuned model
    fine_tuned_path = model_path.replace('.h5', '_fine_tuned.h5')
    model.save(fine_tuned_path)
    
    logger.info(f"Fine-tuning completed! Model saved to {fine_tuned_path}")
    
    return history

if __name__ == "__main__":
    # Create models directory
    os.makedirs(os.path.dirname(CONFIG["model_save_path"]), exist_ok=True)
    
    # Train the model
    history = train_model()
    
    # Optional: Fine-tune the model
    # fine_tune_history = fine_tune_model(CONFIG["model_save_path"])
    
    logger.info("Training script completed!")
