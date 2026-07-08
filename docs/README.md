# PhandaSnap Handover Guide

This folder contains the core documentation needed to hand over the PhandaSnap project to another developer or operator.

## What this project does
PhandaSnap is a Flask-based AI marketing assistant for township and small businesses. It helps users onboard their business, generate a rolling 14-day marketing calendar, create campaign assets, simulate local triggers, and interact with a WhatsApp-style operator assistant.

## Quick summary
- Backend: Python + Flask
- AI generation: Google Gemini
- Audio generation: Gemini TTS with fallback WAV output
- Persistence: JSON file-based storage in db.json
- Deployment: Docker, Firebase Hosting + Cloud Run, and Vercel

## Documentation index
- [setup.md](setup.md) — local environment setup and first run
- [architecture.md](architecture.md) — system structure and data flow
- [deployment.md](deployment.md) — hosting and deployment instructions
- [api-reference.md](api-reference.md) — backend endpoints and payloads
- [troubleshooting.md](troubleshooting.md) — common issues and fixes
- [designlanguage.md](designlanguage.md) — visual and product design direction

## Quick start
1. Install dependencies: `pip install -r requirements.txt`
2. Create a `.env` file with `GEMINI_API_KEY` if you want AI generation.
3. Start the app: `python app.py`
4. Open `http://localhost:8080`

## Important files
- [app.py](../app.py) — main Flask application and API routes
- [generator.py](../generator.py) — AI calendar and copy generation
- [audio.py](../audio.py) — text-to-speech audio generation
- [requirements.txt](../requirements.txt) — Python dependencies
