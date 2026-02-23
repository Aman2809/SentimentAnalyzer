import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load ANN model
model = load_model("savedPackages/ann_model_glove_trainable.keras")

# Load tokenizer
with open("savedPackages/ann_tokenizer_glove_trainable.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Same MAX_LEN used during training
MAX_LEN = 100

# Flask app
app = Flask(__name__)

# Predict function
def predict_sentiment(text):
    sequence = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=MAX_LEN)
    prediction = model.predict(padded)[0]  # e.g., [0.12, 0.35, 0.53]
    labels = ["Negative", "Neutral", "Positive"]
    result = {label: float(f"{score:.4f}") for label, score in zip(labels, prediction)}
    return result

@app.route("/")
def index():
    return render_template("ann_index.html")

@app.route("/predict", methods=["POST"])
def predict():
    input_text = request.json["text"]
    result = predict_sentiment(input_text)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
