# Troubleshooting Guide

## App fails to start
Check that Python dependencies are installed:

```bash
pip install -r requirements.txt
```

## Gemini API errors
If AI generation fails or returns empty content:
- Confirm `GEMINI_API_KEY` is set correctly in `.env`
- Check the API quota or billing status
- The app should fall back to demo mode if no key is set

## Missing audio files
If audio does not render:
- Ensure the `outputs/` directory exists
- Check the server logs for errors from `audio.py`
- The app can regenerate audio on request if needed

## Deployment issues
If Firebase or Vercel deployment fails:
- Verify the correct CLI is installed
- Confirm the project configuration files are present
- Check environment variables in the hosting platform

## State reset
If the app behaves unexpectedly, reset the local state by calling the reset endpoint or deleting `db.json`.
