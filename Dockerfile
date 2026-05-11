# Use the official Python slim image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (needed for some audio processing and fonts)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure the public directory exists (if using for static files)
# and the templates directory is present
RUN mkdir -p outputs templates public

# Expose the port Flask will run on
# Cloud Run sets the PORT environment variable
ENV PORT 8080

# Run the application using gunicorn for production
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
