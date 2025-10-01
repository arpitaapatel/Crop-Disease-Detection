"""
Disease treatment suggestions based on disease names
"""

import json
import os
from typing import Dict, Any

def load_treatments_database() -> Dict[str, Any]:
    """
    Load disease treatments from JSON file
    
    Returns:
        Dictionary containing disease treatments
    """
    try:
        # Try to load comprehensive database first
        comprehensive_path = os.path.join(os.path.dirname(__file__), "..", "knowledge_base", "comprehensive_disease_treatments.json")
        
        if os.path.exists(comprehensive_path):
            with open(comprehensive_path, 'r') as f:
                comprehensive_data = json.load(f)
                # Flatten the hierarchical structure
                return flatten_disease_database(comprehensive_data)
        
        # Fallback to original database
        knowledge_base_path = os.path.join(os.path.dirname(__file__), "..", "knowledge_base", "disease_treatments.json")
        
        if os.path.exists(knowledge_base_path):
            with open(knowledge_base_path, 'r') as f:
                return json.load(f)
        else:
            # Return default treatments if file doesn't exist
            return get_default_treatments()
            
    except Exception as e:
        print(f"Error loading treatments database: {str(e)}")
        return get_default_treatments()

def flatten_disease_database(comprehensive_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Flatten the hierarchical disease database into a flat structure
    
    Args:
        comprehensive_data: Hierarchical disease database
        
    Returns:
        Flattened dictionary with disease names as keys
    """
    flattened = {}
    
    for category, crops in comprehensive_data.items():
        for crop, diseases in crops.items():
            for disease_name, disease_info in diseases.items():
                flattened[disease_name] = disease_info
    
    return flattened

def get_default_treatments() -> Dict[str, Any]:
    """
    Get default disease treatments
    
    Returns:
        Dictionary with default disease treatments
    """
    return {
        "Tomato Bacterial Spot": {
            "description": "Bacterial spot is a common disease of tomato caused by Xanthomonas vesicatoria",
            "treatment": "Apply copper-based fungicides, improve air circulation, avoid overhead watering, remove infected plant debris",
            "prevention": "Use disease-free seeds, practice crop rotation, maintain proper spacing between plants"
        },
        "Tomato Early Blight": {
            "description": "Early blight is caused by the fungus Alternaria solani",
            "treatment": "Apply fungicides containing chlorothalonil or copper, remove infected leaves, improve air circulation",
            "prevention": "Mulch around plants, avoid overhead watering, practice crop rotation"
        },
        "Tomato Late Blight": {
            "description": "Late blight is caused by the oomycete Phytophthora infestans",
            "treatment": "Apply fungicides containing chlorothalonil or copper, remove infected plants immediately",
            "prevention": "Avoid overhead watering, ensure good drainage, practice crop rotation"
        },
        "Tomato Leaf Mold": {
            "description": "Leaf mold is caused by the fungus Passalora fulva",
            "treatment": "Apply fungicides, improve air circulation, reduce humidity",
            "prevention": "Use resistant varieties, maintain proper spacing, avoid overhead watering"
        },
        "Tomato Septoria Leaf Spot": {
            "description": "Septoria leaf spot is caused by the fungus Septoria lycopersici",
            "treatment": "Apply fungicides containing chlorothalonil, remove infected leaves",
            "prevention": "Practice crop rotation, avoid overhead watering, maintain clean garden"
        },
        "Tomato Spider Mites": {
            "description": "Spider mites are tiny arachnids that feed on plant sap",
            "treatment": "Apply insecticidal soap or neem oil, increase humidity, remove heavily infested leaves",
            "prevention": "Regular monitoring, maintain proper humidity, avoid over-fertilization"
        },
        "Tomato Target Spot": {
            "description": "Target spot is caused by the fungus Corynespora cassiicola",
            "treatment": "Apply fungicides, improve air circulation, remove infected leaves",
            "prevention": "Practice crop rotation, maintain proper spacing, avoid overhead watering"
        },
        "Tomato Yellow Leaf Curl Virus": {
            "description": "Yellow leaf curl virus is transmitted by whiteflies",
            "treatment": "Control whitefly populations, remove infected plants, apply systemic insecticides",
            "prevention": "Use resistant varieties, control weeds, monitor for whiteflies"
        },
        "Tomato Mosaic Virus": {
            "description": "Mosaic virus is transmitted by aphids and mechanical means",
            "treatment": "Remove infected plants, control aphid populations, disinfect tools",
            "prevention": "Use disease-free seeds, control aphids, practice good hygiene"
        },
        "Tomato Healthy": {
            "description": "The tomato plant appears healthy with no visible disease symptoms",
            "treatment": "Continue current care practices, monitor regularly for any changes",
            "prevention": "Maintain proper watering, fertilization, and pest management"
        },
        "Potato Early Blight": {
            "description": "Early blight in potatoes is caused by Alternaria solani",
            "treatment": "Apply fungicides containing chlorothalonil, remove infected foliage",
            "prevention": "Practice crop rotation, maintain proper spacing, avoid overhead watering"
        },
        "Potato Late Blight": {
            "description": "Late blight in potatoes is caused by Phytophthora infestans",
            "treatment": "Apply fungicides containing chlorothalonil or copper, remove infected plants",
            "prevention": "Avoid overhead watering, ensure good drainage, practice crop rotation"
        },
        "Potato Healthy": {
            "description": "The potato plant appears healthy with no visible disease symptoms",
            "treatment": "Continue current care practices, monitor regularly for any changes",
            "prevention": "Maintain proper watering, fertilization, and pest management"
        },
        "Corn Northern Leaf Blight": {
            "description": "Northern leaf blight is caused by the fungus Exserohilum turcicum",
            "treatment": "Apply fungicides containing azoxystrobin or propiconazole",
            "prevention": "Use resistant varieties, practice crop rotation, maintain proper spacing"
        },
        "Corn Common Rust": {
            "description": "Common rust is caused by the fungus Puccinia sorghi",
            "treatment": "Apply fungicides containing azoxystrobin or propiconazole",
            "prevention": "Use resistant varieties, practice crop rotation, avoid overhead watering"
        },
        "Corn Gray Leaf Spot": {
            "description": "Gray leaf spot is caused by the fungus Cercospora zeae-maydis",
            "treatment": "Apply fungicides containing azoxystrobin or propiconazole",
            "prevention": "Use resistant varieties, practice crop rotation, maintain proper spacing"
        },
        "Corn Healthy": {
            "description": "The corn plant appears healthy with no visible disease symptoms",
            "treatment": "Continue current care practices, monitor regularly for any changes",
            "prevention": "Maintain proper watering, fertilization, and pest management"
        }
    }

def get_treatment_suggestion(disease_name: str) -> str:
    """
    Get treatment suggestion for a specific disease
    
    Args:
        disease_name: Name of the disease
        
    Returns:
        Treatment suggestion string
    """
    treatments_db = load_treatments_database()
    
    if disease_name in treatments_db:
        disease_info = treatments_db[disease_name]
        return f"{disease_info['description']}\n\nTreatment: {disease_info['treatment']}\n\nPrevention: {disease_info['prevention']}"
    else:
        return f"No specific treatment information available for {disease_name}. Please consult with a local agricultural extension service or plant pathologist for proper diagnosis and treatment recommendations."
