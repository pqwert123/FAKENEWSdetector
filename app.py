from flask import Flask, render_template, request, jsonify
import pickle, os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # allows big text input up to 5MB

# Load model and vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))


# Frontend route
@app.route('/')
def home():
    return render_template('index.html')

# Backend API route (for JSON POST)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Case 1: if form data (HTML form)
        if request.form.get("news"):
            text = request.form['news']
        else:
            # Case 2: if JSON (frontend JS)
            data = request.get_json()
            text = data.get('text', '')

        if not text.strip():
            return jsonify({"error": "No input text"}), 400

        # Predict
        vect = vectorizer.transform([text])
        pred = model.predict(vect)[0]

        # Confidence
        confidence = None
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(vect)
            classes = list(model.classes_)
            idx = classes.index(pred)
            confidence = round(float(prob[0][idx]), 2)

        # If JSON request → return JSON
        if request.is_json:
            return jsonify({"label": pred, "confidence": confidence})
        else:
            # If form → render HTML
            return render_template('index.html', prediction=pred, text=text, confidence=confidence)
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

