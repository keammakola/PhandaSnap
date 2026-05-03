"""
app.py
------
Flask web frontend for the Hustle Engine Social Media Toolkit.
"""

import re
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from generator import generate_script
from audio import generate_audio

app = Flask(__name__)
OUTPUT_DIR = Path("outputs")


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

    if not store_name or not promo_end or not promos:
        return jsonify({"error": "Store name, promo end date, and at least one deal are required."}), 400

    slug = slugify(store_name)
    OUTPUT_DIR.mkdir(exist_ok=True)

    caption, voiceover = generate_script(store_name, promo_end, promos, language, scenario)

    caption_path = OUTPUT_DIR / f"{slug}_caption.txt"
    caption_path.write_text(caption, encoding="utf-8")

    audio_path = OUTPUT_DIR / f"{slug}_voiceover.wav"
    generate_audio(voiceover, str(audio_path))

    return jsonify({
        "caption": caption,
        "audio_url": f"/outputs/{slug}_voiceover.wav",
    })


@app.route("/outputs/<path:filename>")
def serve_output(filename):
    return send_from_directory(OUTPUT_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True)
