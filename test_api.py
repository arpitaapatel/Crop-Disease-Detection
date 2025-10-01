#!/usr/bin/env python3
"""
Test script for Crop Disease Detection API
"""

import requests
import json
import os
from PIL import Image
import numpy as np
import io

API_BASE_URL = "http://localhost:8000"

def create_test_image():
    """Create a test image for API testing"""
    # Create a random RGB image
    image_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    image = Image.fromarray(image_array)
    
    # Save to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def test_predict_endpoint():
    """Test the predict endpoint"""
    print("🔍 Testing predict endpoint...")
    try:
        # Create test image
        test_image = create_test_image()
        
        # Prepare files for upload
        files = {'file': ('test_image.jpg', test_image, 'image/jpeg')}
        
        # Make request
        response = requests.post(f"{API_BASE_URL}/predict", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction successful:")
            print(f"   Disease: {data['disease_name']}")
            print(f"   Confidence: {data['confidence_score']}%")
            print(f"   Treatment: {data['treatment_suggestion'][:100]}...")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Starting API tests...")
    print(f"API Base URL: {API_BASE_URL}")
    print("-" * 50)
    
    # Test health endpoint
    health_ok = test_health_endpoint()
    print()
    
    # Test predict endpoint
    predict_ok = test_predict_endpoint()
    print()
    
    # Summary
    print("-" * 50)
    if health_ok and predict_ok:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("❌ Some tests failed. Check the API server.")
    
    return health_ok and predict_ok

if __name__ == "__main__":
    main()
