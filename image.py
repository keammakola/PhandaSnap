"""
image.py
--------
Generates a promotional poster image for the store deals using Vertex AI
(Imagen 3). Authenticates via Application Default Credentials / Service Accounts.
"""

import os
from google import genai
from google.genai import types

def build_image_prompt(store_name: str, promos: list[str]) -> str:
    promo_list = " \\n ".join(promos)
    return f"""
A visually stunning, eye-catching promotional poster for a social media marketing campaign.

Text to render on the image:
1. Top heading: "{store_name}"
2. Main body: "{promo_list}"

CRITICAL INSTRUCTIONS FOR TEXT:
- You must perfectly spell the text exactly as provided.
- Do NOT add any extra words, random letters, or filler text.
- ONLY include the exact text provided above. No other words should appear in the image.

Visual Style: Vibrant colors, energetic, highly professional, modern dynamic lighting, meant to stop the scroll.
""".strip()

def generate_poster(store_name: str, promos: list[str], output_path: str) -> None:
    """
    Generate a poster image using Vertex AI Imagen 3 and save it to output_path.
    """
    project_id = os.environ.get("VERTEX_PROJECT_ID")
    
    if not project_id or project_id == "your-gcp-project-id":
        print("   ⚠️  Poster skipped: Missing VERTEX_PROJECT_ID in your .env file.")
        return
        
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print("   ⚠️  Poster skipped: No GOOGLE_APPLICATION_CREDENTIALS path found in your .env file.")
        return

    print("🎨  Generating brilliant promotional poster with Google Cloud Vertex AI (Imagen 3)...")

    # Initializing genai to route exactly sequentially via Vertex backend.
    try:
        client = genai.Client(
            vertexai=True, 
            project=project_id, 
            location="us-central1"
        )
        prompt = build_image_prompt(store_name, promos)

        response = client.models.generate_images(
            model='imagen-3.0-generate-002',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                output_mime_type="image/jpeg",
                aspect_ratio="3:4" 
            )
        )

        if not response.generated_images:
            print("   ⚠️  Failed to generate image via Vertex AI.")
            return

        # Extract image bytes and save
        image_bytes = response.generated_images[0].image.image_bytes
        
        with open(output_path, "wb") as f:
            f.write(image_bytes)

        print(f"✅  Poster saved to: {output_path}")

    except Exception as e:
        print(f"   ⚠️  Vertex AI Imagen generation failed: {e}")
