# Firebase Deployment Guide (Completely Free Edition)

This project is now configured for **100% Free Hosting** using Firebase Hosting. It does not require a credit card or a billing account.

## How it works
- **Logic**: All AI generation happens in your browser using the Gemini Javascript SDK.
- **Voiceover**: Uses your device's built-in Text-to-Speech (free).
- **Hosting**: Served via Firebase's free Spark plan.

## Setup Instructions

1.  **Get a Gemini API Key**:
    - Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
    - Create a free API Key.
2.  **Deployment**:
    - Since you hit permission errors with global installation, use `npx` to run Firebase commands without installing them globally:
    ```bash
    # 1. Login to Firebase
    npx firebase-tools login

    # 2. Initialize (if not already done)
    # Just press enter for defaults, select your project
    npx firebase-tools init hosting

    # 3. Deploy
    npx firebase-tools deploy
    ```

## Security Note
Because this is a "Client-Side" app, your API key is stored in your browser's `localStorage`. It is not sent to any server except Google's Gemini API. If you share your website URL, others will need to enter **their own** API key to use it, or you can hardcode yours (not recommended for public sites).

## Local Testing
To test locally without deploying:
```bash
npx firebase-tools serve
```
Then open `http://localhost:5000`.
