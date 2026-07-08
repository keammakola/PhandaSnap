# API Reference

## Core endpoints

### GET `/`
Renders the main landing page.

### GET `/api/dashboard`
Returns the current persisted app state as JSON.

### POST `/api/set_api_key`
Stores a Gemini API key at runtime and updates the current DB state.

### POST `/api/reset`
Resets the app state to the default onboarding state.

### POST `/api/onboard`
Accepts a merchant profile and initializes the calendar.

Example payload:
```json
{
  "profile": {
    "store_name": "Mandla's Spaza",
    "location": "Soweto"
  },
  "simulated_date": "2026-07-08"
}
```

### POST `/api/calendar/generate-assets`
Generates copy assets and audio for a specific campaign item.

### POST `/api/calendar/update-item`
Updates a calendar item status and optionally records outcomes.

### POST `/api/simulate-trigger`
Applies simulated weather or payday triggers to the current calendar.

### POST `/api/calendar/apply-swap`
Applies a trigger-based swap to a campaign item.

### POST `/api/whatsapp/chat`
Sends a message to the simulated WhatsApp operator assistant.

### GET `/api/media/audio/<item_id>/<type>`
Serves generated audio for a campaign item.

### GET `/api/download_zip/<item_id>`
Downloads a ZIP bundle of campaign assets.
