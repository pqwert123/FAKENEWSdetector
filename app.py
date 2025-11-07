# ===============================================
# Fake News Detection Web App
# Developed by: Pratima Sahu
# College: Madhav Institute of Technology and Science (EEIoT)
# ===============================================

from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Initialize Flask App
app = Flask(__name__, template_folder='./templates', static_folder='./static')

# Load Trained Model and Vectorizer
try:
    model = pickle.load(open('model.pkl', 'rb'))
    vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
    print("✅ Model and Vectorizer loaded successfully!")
except Exception as e:
    print("⚠️ Error loading model/vectorizer:", e)

# Initialize NLP Tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# ========== Text Preprocessing Function ==========
def clean_text(news):
    news = re.sub(r'[^a-zA-Z\\s]', '', news)
    news = news.lower()
    tokens = nltk.word_tokenize(news)
    filtered = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(filtered)

# ========== Prediction Function ==========
def predict_news(news_text):
    processed = clean_text(news_text)
    vector_input = vectorizer.transform([processed])
    prediction = model.predict(vector_input)[0]

    # Confidence
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(vector_input)[0]
        confidence = float(np.max(probs))
    else:
        confidence = 0.85  # fallback

    label = "FAKE" if prediction == 1 else "REAL"
    return label, round(confidence * 100, 2)


# ========== ROUTES ==========

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict_page')
def predict_page():
    return render_template('prediction.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text.strip():
            return jsonify({'label': 'Invalid Input', 'confidence': 0.0})

        label, confidence = predict_news(text)
        return jsonify({'label': label, 'confidence': confidence})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({'label': 'Error', 'confidence': 0.0})


if __name__ == '__main__':
    app.run(debug=True)



