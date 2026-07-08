# Deployment Guide

## Local deployment
Run the app directly with Python:

```bash
python app.py
```

## Docker deployment
Use Docker Compose for a containerized local or server deployment:

```bash
docker compose up --build
```

## Firebase Hosting + Cloud Run
The project includes Firebase configuration in [firebase.json](../firebase.json).

### Requirements
- Firebase CLI installed
- A Firebase project created
- A `.firebaserc` file with your project ID

### Deploy
```bash
firebase login
firebase deploy --only hosting,run
```

## Vercel deployment
The project includes a Vercel config in [vercel.json](../vercel.json).

### Deploy
```bash
vercel --prod
```

## Production notes
- Set environment variables in the hosting platform, not only locally.
- Ensure the app listens on the `PORT` environment variable.
- Confirm the container build works before publishing.
