from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import pandas as pd
import sys

# Add project root (parent of backend/) to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from ml_model.url_features import extract_url_features


app = Flask(__name__)
CORS(app)

# === Load trained model ===
model_path = os.path.join('ml_model', 'malware_url_model.pkl')
try:
    model = joblib.load(model_path)
    print(f"✓ Model loaded successfully from {model_path}")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    model = None


@app.route("/predict_url", methods=["POST"])
def predict_url():
    """Accept a raw URL and return whether it's malicious or safe with confidence."""
    if model is None:
        return jsonify({"error": "Model not loaded. Please train the model first."}), 500
    
    try:
        data = request.get_json()
        raw_url = data.get("url", "")
        if not raw_url:
            return jsonify({"error": "Missing 'url' field"}), 400

        # 🔹 Extract numerical features
        features = extract_url_features(raw_url)
        df = pd.DataFrame([features])

        # 🔹 Predict label and probability
        pred = model.predict(df)[0]
        prob = model.predict_proba(df)[0]  # [prob_safe, prob_malicious]

        result = "malicious" if pred == 1 else "safe"
        confidence = float(prob[1]) if pred == 1 else float(prob[0])  # Confidence in the prediction

        return jsonify({
            "url": raw_url,
            "result": result,
            "confidence": round(confidence, 3),
            "probabilities": {
                "safe": round(float(prob[0]), 3),
                "malicious": round(float(prob[1]), 3)
            },
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/debug_features", methods=["POST"])
def debug_features():
    """Debug endpoint to see extracted features without prediction"""
    try:
        data = request.get_json()
        raw_url = data.get("url", "")
        if not raw_url:
            return jsonify({"error": "Missing 'url' field"}), 400
        
        features = extract_url_features(raw_url)
        
        return jsonify({
            "url": raw_url,
            "features": features
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/model_info", methods=["GET"])
def model_info():
    """Get information about the loaded model"""
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        return jsonify({
            "model_type": type(model).__name__,
            "n_features": model.n_features_in_,
            "feature_names": list(model.feature_names_in_) if hasattr(model, 'feature_names_in_') else "Not available",
            "n_classes": int(model.n_classes_),
            "classes": model.classes_.tolist()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Malicious URL Detection API",
        "status": "running",
        "model_loaded": model is not None,
        "endpoints": {
            "POST /predict_url": "Predict if a URL is malicious",
            "POST /debug_features": "Extract features from a URL",
            "GET /model_info": "Get model information",
            "GET /": "API status"
        }
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)