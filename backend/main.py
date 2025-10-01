"""
FastAPI server for Real-Time Crop Disease Detection
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import numpy as np
from PIL import Image
import io
import json
import os
from typing import Dict, Any
import logging

# Import our custom modules
from model_utils import load_model, preprocess_image
from disease_treatments import get_treatment_suggestion

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Crop Disease Detection API",
    description="API for detecting crop diseases from uploaded images",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to store the loaded model
model = None

@app.on_event("startup")
async def load_model_on_startup():
    """Load the trained model when the server starts"""
    global model
    try:
        model_path = os.path.join(os.path.dirname(__file__), "..", "models", "model.h5")
        model = load_model(model_path)
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise e

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Crop Disease Detection API is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    """
    Predict crop disease from uploaded image
    
    Args:
        file: Uploaded image file
        
    Returns:
        JSON response with disease prediction and treatment suggestion
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image data
        image_data = await file.read()
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Preprocess image
        processed_image = preprocess_image(image)
        
        # Make prediction
        if model is None:
            raise HTTPException(status_code=500, detail="Model not loaded")
        
        predictions = model.predict(processed_image)
        
        # Get the class with highest probability
        class_index = np.argmax(predictions[0])
        confidence = float(predictions[0][class_index])
        
        # Map class index to disease name - Comprehensive list
        disease_names = [
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
        
        disease_name = disease_names[class_index] if class_index < len(disease_names) else "Unknown Disease"
        
        # Get treatment suggestion
        treatment = get_treatment_suggestion(disease_name)
        
        # Prepare response
        response = {
            "disease_name": disease_name,
            "confidence_score": round(confidence * 100, 2),
            "treatment_suggestion": treatment
        }
        
        logger.info(f"Prediction completed: {disease_name} (confidence: {confidence:.2f})")
        
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
