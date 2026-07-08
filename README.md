# ⚡ PhandaSnap Operator (AI Marketing Assistant SaaS)

PhandaSnap Operator is an AI-powered marketing assistant SaaS tailored for South African township and small business merchants (spazas, salons, shisanyamas, etc.). Instead of just generating one-off assets, it behaves like an active junior marketing hire—diagnosing business needs, running a rolling content calendar, adapting to real-world weather and payday triggers, tracking promotion outcomes, and interacting directly with the merchant via a simulated WhatsApp chat interface.

## Core Features

1. **Strategic Diagnosis**: Automatically analyzes the business profile (best sellers, slow-moving items, busiest days) on onboarding to provide strategic marketing insights.
2. **Rolling Content Calendar**: Manages a rolling 14-day campaign calendar tied to real-world triggers.
3. **Environment & Trigger Simulation**: Allows changing simulated weather (Sunny & Hot, Rainy & Cold) or payday flags, which prompts the Operator to suggest swapping scheduled campaigns dynamically (e.g. promoting cold drinks on a hot day).
4. **WhatsApp Assistant Chat (Simulated)**: A mock smartphone chat view allows interacting with the Operator chatbot in real-time to tweak campaigns and approve posts using local township slang (tsotsitaal/slang support).
5. **Outcome Feedback Loop**: Log redemption and click metrics to let the AI learn and adapt future suggestions.
6. **Multi-format Assets**: Every calendar campaign generates vertical story posters (Pillow text rendering over AI-generated backgrounds), browser-playable TTS voiceovers, WhatsApp voice notes, and caption copy in multiple languages (isiZulu, English, Afrikaans, Sesotho).
7. **Zero-Setup Demo Mode**: Runs out-of-the-box with simulated client-side calendar generation and local chat rules if no Gemini API Key is configured.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
   Add your Google Gemini API Key to `.env` (optional; falls back to Demo Mode if omitted):
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Run the SaaS Application**:
   ```bash
   python app.py
   ```
   Then open [http://localhost:8080](http://localhost:8080) in your browser.

4. **Deploy to Firebase**:
   - Install the Firebase CLI if needed:
     ```bash
     npm install -g firebase-tools
     ```
   - Set your Firebase project ID in `.firebaserc`.
   - Deploy the app to Firebase Hosting + Cloud Run:
     ```bash
     firebase deploy --only hosting,run
     ```
   - The app uses the existing `Dockerfile` and serves through Cloud Run behind Firebase Hosting.

5. **Deploy to Vercel as a Container**:
   - Install the Vercel CLI if needed:
     ```bash
     npm install -g vercel
     ```
   - Ensure `vercel.json` exists in the repo root and the app listens on the `PORT` environment variable.
   - Deploy the containerized app:
     ```bash
     vercel --prod
     ```
   - This uses the existing `Dockerfile` and serves the Flask app through a Vercel container.

## Project Structure

```
PhandaSnap/
├── app.py          # Flask Web server & persistable DB simulation (db.json)
├── generator.py    # Operator Engine (Gemini calendar & chat reasoning)
├── audio.py        # TTS Voice note & Voiceover generation (Gemini TTS)
├── image.py        # Graphic poster rendering (Pillow overlay + background generator)
├── templates/
│   └── index.html  # Modern Glassmorphic SaaS Web UI (Flask-served)
├── public/
│   └── index.html  # Hybrid client-side Web UI (for Firebase Hosting)
├── docker-compose.yml
├── firebase.json   # Firebase Cloud Run config for container deployment
├── vercel.json     # Vercel static deployment config
└── outputs/        # Generated campaign packs and media caches
```
