"""
app.py
------
Stateless Flask backend for PhandaSnap, optimized for Google Cloud Run.
"""

import os
import re
import base64
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from generator import generate_script
from audio import generate_audio_bytes
from logger import log_generation

app = Flask(__name__)
CORS(app)

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    store_name = data.get("store_name", "").strip()
    promo_end = data.get("promo_end", "").strip()
    promos = [p.strip() for p in data.get("promos", []) if p.strip()]
    language = data.get("language", "English").strip() or "English"
    scenario = data.get("scenario", "General Hustle").strip() or "General Hustle"
    audience = data.get("audience", "General Public").strip() or "General Public"
    tone = data.get("tone", "Hype").strip() or "Hype"

    if not store_name or not promo_end or not promos:
        return jsonify({"error": "Store name, promo end date, and at least one deal are required."}), 400

    try:
        # 1. Generate Script
        caption, voiceover = generate_script(store_name, promo_end, promos, language, scenario, audience, tone)

        # 2. Generate Audio Bytes
        audio_bytes = generate_audio_bytes(voiceover)
        audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')

        # 3. Log the generation
        log_generation(store_name, language, scenario, audience, tone)

        return jsonify({
            "caption": caption,
            "audio_b64": f"data:audio/wav;base64,{audio_b64}",
            "filename": f"{slugify(store_name)}_assets"
        })
    except Exception as e:
        print(f"Error during generation: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Get port from environment variable or default to 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
