"""
CyberSense Backend API
Flask application for cyberbullying detection
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import joblib
import numpy as np
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# CORS configuration - allow your Vercel frontend
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "http://localhost:5173",
            "https://*.vercel.app",
            "https://your-frontend-domain.vercel.app"  # Replace with actual domain
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Global variables for models
model = None
tfidf_vectorizer = None
svd_model = None
svd_scaler = None
tb_scaler = None

def load_models():
    """Load all required models and scalers"""
    global model, tfidf_vectorizer, svd_model, svd_scaler, tb_scaler
    
    try:
        model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        
        # Check if models exist
        model_path = os.path.join(model_dir, 'best_model.joblib')
        if not os.path.exists(model_path):
            logger.warning(f"Model not found at {model_path}. Using dummy model for demo.")
            return False
        
        # Load models
        model = joblib.load(model_path)
        logger.info("Main model loaded successfully")
        
        # Try to load other components (optional)
        try:
            tfidf_vectorizer = joblib.load(os.path.join(model_dir, 'tfidf_vectorizer.joblib'))
            logger.info("TF-IDF vectorizer loaded")
        except FileNotFoundError:
            logger.warning("TF-IDF vectorizer not found")
        
        try:
            svd_model = joblib.load(os.path.join(model_dir, 'svd_truncated.joblib'))
            svd_scaler = joblib.load(os.path.join(model_dir, 'svd_scaler.joblib'))
            tb_scaler = joblib.load(os.path.join(model_dir, 'tb_scaler.joblib'))
            logger.info("SVD components loaded")
        except FileNotFoundError:
            logger.warning("SVD components not found")
        
        return True
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        return False

def preprocess_text(text):
    """
    Basic text preprocessing
    For full preprocessing, import from preprocessing.py
    """
    import re
    
    if not isinstance(text, str):
        text = str(text)
    
    # Basic cleaning
    text = text.lower()
    text = re.sub(r'http\S+|www\.\S+', '', text)  # Remove URLs
    text = re.sub(r'@\w+', '', text)  # Remove mentions
    text = re.sub(r'#\w+', '', text)  # Remove hashtags
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special chars
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    
    return text

def predict_text(text):
    """
    Predict if text is cyberbullying
    Returns: dict with prediction and confidence
    """
    try:
        # Preprocess text
        cleaned_text = preprocess_text(text)
        
        if not cleaned_text:
            return {
                'error': 'Text is empty after preprocessing',
                'prediction': 'unknown',
                'confidence': 0.0
            }
        
        # If models are loaded, use them
        if model is not None and tfidf_vectorizer is not None:
            # Transform text
            text_tfidf = tfidf_vectorizer.transform([cleaned_text])
            
            # Make prediction
            prediction = model.predict(text_tfidf)[0]
            proba = model.predict_proba(text_tfidf)[0]
            confidence = float(max(proba))
            
            result = {
                'prediction': 'cyberbullying' if prediction == 1 else 'not_cyberbullying',
                'confidence': confidence,
                'cleaned_text': cleaned_text
            }
        else:
            # Demo mode - simple keyword detection
            cyberbullying_keywords = [
                'hate', 'stupid', 'idiot', 'kill', 'die', 'ugly', 
                'loser', 'dumb', 'fat', 'worthless', 'disgusting'
            ]
            
            text_lower = cleaned_text.lower()
            has_keywords = any(keyword in text_lower for keyword in cyberbullying_keywords)
            
            result = {
                'prediction': 'cyberbullying' if has_keywords else 'not_cyberbullying',
                'confidence': 0.75 if has_keywords else 0.85,
                'cleaned_text': cleaned_text,
                'demo_mode': True,
                'note': 'Using keyword-based demo. Train and upload models for ML predictions.'
            }
        
        return result
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return {
            'error': str(e),
            'prediction': 'error',
            'confidence': 0.0
        }

# Routes
@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'CyberSense API',
        'version': '1.0.0',
        'models_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Detailed health check"""
    return jsonify({
        'status': 'healthy',
        'models': {
            'main_model': model is not None,
            'tfidf_vectorizer': tfidf_vectorizer is not None,
            'svd_model': svd_model is not None
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict if text contains cyberbullying
    
    Request body:
    {
        "text": "Your text here"
    }
    
    Response:
    {
        "prediction": "cyberbullying" or "not_cyberbullying",
        "confidence": 0.95,
        "timestamp": "2024-01-01T12:00:00"
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing text field in request body',
                'example': {'text': 'Your text here'}
            }), 400
        
        text = data['text']
        
        # Validate input
        if not text or not isinstance(text, str):
            return jsonify({'error': 'Text must be a non-empty string'}), 400
        
        if len(text) > 5000:
            return jsonify({'error': 'Text too long (max 5000 characters)'}), 400
        
        # Make prediction
        result = predict_text(text)
        
        # Add metadata
        result['timestamp'] = datetime.now().isoformat()
        result['original_text'] = text[:100] + '...' if len(text) > 100 else text
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Request error: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/batch-predict', methods=['POST'])
def batch_predict():
    """
    Predict multiple texts at once
    
    Request body:
    {
        "texts": ["text1", "text2", "text3"]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'texts' not in data:
            return jsonify({'error': 'Missing texts field in request body'}), 400
        
        texts = data['texts']
        
        if not isinstance(texts, list):
            return jsonify({'error': 'texts must be an array'}), 400
        
        if len(texts) > 100:
            return jsonify({'error': 'Maximum 100 texts per batch'}), 400
        
        # Process each text
        results = []
        for idx, text in enumerate(texts):
            result = predict_text(text)
            result['index'] = idx
            results.append(result)
        
        return jsonify({
            'results': results,
            'count': len(results),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            'GET /',
            'GET /api/health',
            'POST /api/predict',
            'POST /api/batch-predict'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': str(e)
    }), 500

# Initialize models on startup
with app.app_context():
    logger.info("Starting CyberSense API...")
    models_loaded = load_models()
    if models_loaded:
        logger.info("✓ Models loaded successfully")
    else:
        logger.warning("⚠ Running in demo mode (models not loaded)")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
