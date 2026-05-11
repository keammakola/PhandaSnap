# Google Cloud Run Deployment Guide (Docker)

This project is now ready to be Dockerized and deployed to **Google Cloud Run**.

## Prerequisites

1.  **Google Cloud SDK (gcloud)**: Installed and authenticated.
2.  **Billing Account**: Enabled on your Google Cloud project.
3.  **Project ID**: `apr-kitchen`

## 1. Build and Push to Artifact Registry

First, enable the required services:
```bash
gcloud services enable artifactregistry.googleapis.com run.googleapis.com
```

Create a repository (You already did this):
```bash
gcloud artifacts repositories create phandasnap-repo \
    --repository-format=docker \
    --location=us-central1
```

**Build and push the image (RUN THIS NEXT):**
```bash
gcloud builds submit --tag us-central1-docker.pkg.dev/apr-kitchen/phandasnap-repo/phandasnap-app .
```

## 2. Deploy to Cloud Run

Deploy the container and set the `GEMINI_API_KEY` environment variable:

```bash
gcloud run deploy phandasnap \
    --image us-central1-docker.pkg.dev/apr-kitchen/phandasnap-repo/phandasnap-app \
    --set-env-vars="GEMINI_API_KEY=YOUR_REAL_API_KEY_HERE" \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

## 3. Local Testing with Docker

If you have Docker installed locally, you can test the container before pushing:

```bash
docker build -t phandasnap-app .
docker run -p 8080:8080 -e GEMINI_API_KEY=YOUR_KEY_HERE phandasnap-app
```
Then visit `http://localhost:8080`.

## Why this is better
- **High Quality**: Uses the Python backend for the high-end Gemini TTS.
- **Scalable**: Handles thousands of users automatically.
- **Standard**: Uses Docker, making it easy to manage and move.
