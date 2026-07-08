# Setup Guide

## Prerequisites
- Python 3.10+
- pip
- Optional: Docker Desktop
- Optional: Firebase CLI and Vercel CLI for deployment

## Install dependencies
```bash
cd /home/kea/Desktop/PhandaSnap
pip install -r requirements.txt
```

## Environment variables
Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_key_here
PORT=8080
```

Notes:
- `GEMINI_API_KEY` is optional. If it is missing, the app falls back to demo mode.
- `PORT` is used by the Flask app when running in containers or hosting environments.

## Run locally
```bash
python app.py
```

Then open:
```text
http://localhost:8080
```

## Run with Docker
```bash
docker compose up --build
```

The app will be available at `http://localhost:8080`.

## Expected generated files
When the app runs, it will create:
- `db.json` — local JSON-based state
- `outputs/` — generated audio and campaign assets
