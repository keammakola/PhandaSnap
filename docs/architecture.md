# Architecture Overview

## High-level structure
PhandaSnap is a small full-stack Flask application with AI-assisted content generation.

### Core components
- [app.py](../app.py) — Flask server, routing, state persistence, dashboard logic, and media endpoints
- [generator.py](../generator.py) — prompt-based generation for campaign calendars, captions, and chat responses using Gemini
- [audio.py](../audio.py) — audio generation using Gemini TTS with a fallback WAV generator
- [templates/](../templates) — Flask-rendered HTML views
- [public/](../public) — frontend assets for hosting-based deployment
- [outputs/](../outputs) — generated campaign media and assets

## Runtime flow
1. A merchant completes onboarding.
2. The app stores profile information in `db.json`.
3. The app generates a 14-day campaign calendar.
4. The user can generate assets for each campaign item.
5. Weather and payday triggers can modify the calendar.
6. The user can interact with the simulated WhatsApp-style assistant.

## State model
The main persisted state includes:
- `onboarded`
- `profile`
- `calendar`
- `analytics`
- `chat_history`
- `simulated_weather`
- `simulated_date`
- `is_payday`

## Important implementation notes
- The app uses a JSON file as a lightweight database rather than a dedicated database engine.
- Demo mode is available when no Gemini API key is configured.
- Audio generation writes WAV files into the `outputs/` directory.
- The app is designed to work both locally and in containerized hosting platforms.
