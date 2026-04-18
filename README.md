# ⚡ Hustle Engine

AI-powered social media toolkit for township and small business store promotions. Enter your store name, deals, and promo end date — get a viral caption, voiceover audio, and a promotional graphic in seconds.

## What it generates

- **Caption** — hype social media post with emojis and hashtags (TikTok/Reels style)
- **Voiceover** — spoken audio file ready to drop into your video edit
- **Poster** — eye-catching promotional graphic (requires Vertex AI setup)

## Prerequisites

- Python 3.10+
- A [Gemini API key](https://aistudio.google.com/app/apikey)
- *(Optional)* A Google Cloud project with Vertex AI enabled for poster generation

## Setup

1. **Clone the repo and install dependencies**

   ```bash
   git clone <repo-url>
   cd "hustle engine"
   pip install -r requirements.txt
   ```

2. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Open `.env` and fill in your values:

   ```env
   GEMINI_API_KEY=your_gemini_api_key_here

   # Optional — only needed for poster generation
   VERTEX_PROJECT_ID=your-gcp-project-id
   GOOGLE_APPLICATION_CREDENTIALS=path/to/service_account.json
   ```

## Running the web UI

```bash
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

## Running the CLI

```bash
python main.py
```

Follow the prompts to enter your store details and deals.

## Output files

All generated assets are saved to the `outputs/` folder:

| File | Description |
|---|---|
| `<store>_caption.txt` | Social media caption |
| `<store>_voiceover.wav` | Voiceover audio |
| `<store>_social_graphic.jpg` | Promotional poster |

## Project structure

```
hustle engine/
├── app.py          # Flask web server
├── main.py         # CLI entry point
├── generator.py    # Gemini caption + voiceover script generation
├── audio.py        # Gemini TTS audio generation
├── image.py        # Vertex AI Imagen poster generation
├── templates/
│   └── index.html  # Web UI
└── outputs/        # Generated assets (git-ignored)
```
