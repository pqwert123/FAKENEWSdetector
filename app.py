from flask import Flask, render_template, request, jsonify
import pickle, os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Allow up to 5 MB text input
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  

# Load model and vectorizer safely
try:
    model = pickle.load(open("model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
except Exception as e:
    print("❌ Error loading model/vectorizer:", e)
    model, vectorizer = None, None


# =========================
# Frontend route
# =========================
@app.route('/')
def home():
    return render_template('index.html')


# =========================
# Backend API (JSON POST)
# =========================
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # --- Step 1: Input Extraction ---
        text = None

        # If form data (from HTML form)
        if request.form.get("news"):
            text = request.form["news"]

        # Else if raw JSON input
        elif request.is_json:
            data = request.get_json(silent=True)
            if not data:
                return jsonify({"error": "Invalid or empty JSON body"}), 400
            text = data.get("text", "")

        else:
            return jsonify({"error": "Unsupported input format"}), 400

        # --- Step 2: Input Validation ---
        if not text or not text.strip():
            return jsonify({"error": "No input text provided"}), 400

        if model is None or vectorizer is None:
            return jsonify({"error": "Model not loaded properly"}), 500

        # --- Step 3: Prediction ---
        vect = vectorizer.transform([text])
        pred = model.predict(vect)[0]
        pred = str(pred)

        # --- Step 4: Confidence ---
        confidence = None
        if hasattr(model, "predict_proba"):
            try:
                prob = model.predict_proba(vect)
                classes = list(model.classes_)
                idx = classes.index(pred)
                confidence = float(prob[0][idx])
            except Exception:
                confidence = None

        # --- Step 5: Return JSON safely ---
        return jsonify({
            "label": pred,
            "confidence": round(confidence, 2) if confidence is not None else None
        })

    except Exception as e:
        print("❌ Error in /predict:", e)
        return jsonify({"error": str(e)}), 500


# =========================
# Run the app
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


