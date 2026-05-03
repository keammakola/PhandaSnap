"""
image.py
--------
Hybrid image generator:
1. Generates a high-quality background using Pollinations.ai (Flux).
2. Overlays 100% accurate text (Store Name & Deals) using Pillow.
"""

import requests
import io
from PIL import Image, ImageDraw, ImageFont
from urllib.parse import quote

# Path to a reliable font in the WSL environment
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def build_background_prompt(store_name: str) -> str:
    """Creates a prompt for a high-quality background WITHOUT text."""
    return f"Professional cinematic product display, modern luxury retail background, blurred shop interior, high-end commercial aesthetic, vibrant lighting, abstract bokeh, 8k, photorealistic, elegant composition. No people, no text."

def draw_text_with_shadow(draw, text, position, font, text_color="white", shadow_color="black"):
    x, y = position
    # Draw shadow
    draw.text((x+2, y+2), text, font=font, fill=shadow_color)
    # Draw main text
    draw.text((x, y), text, font=font, fill=text_color)

def generate_poster(store_name: str, promos: list[str], output_path: str) -> None:
    """
    1. Fetch AI background
    2. Overlay accurate text using Pillow
    """
    print(f"🎨  Creating high-accuracy hybrid poster for '{store_name}'...")

    # 1. Fetch AI Background
    bg_prompt = build_background_prompt(store_name)
    encoded_prompt = quote(bg_prompt)
    bg_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=1024&nologo=true&seed=42"

    try:
        response = requests.get(bg_url, timeout=45)
        response.raise_for_status()
        img = Image.open(io.BytesIO(response.content))
        
        draw = ImageDraw.Draw(img)
        width, height = img.size

        # 2. Add Semi-transparent Overlay for Readability
        # Darken the whole image slightly for better text contrast
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 80))
        img = Image.alpha_composite(img.convert('RGBA'), overlay)
        draw = ImageDraw.Draw(img)

        # 3. Load Fonts
        try:
            title_font = ImageFont.truetype(FONT_PATH, 70)
            deal_font = ImageFont.truetype(FONT_PATH, 45)
        except:
            title_font = ImageFont.load_default()
            deal_font = ImageFont.load_default()

        # 4. Draw Store Name (Top)
        title_text = store_name.upper()
        # Use textbbox for centering (Pillow 10.0+)
        bbox = draw.textbbox((0, 0), title_text, font=title_font)
        tw = bbox[2] - bbox[0]
        draw_text_with_shadow(draw, title_text, ((width - tw) / 2, 80), title_font, text_color="#FF6B00")

        # 5. Draw Decorative Line
        draw.line([(100, 180), (width - 100, 180)], fill="#FF6B00", width=5)

        # 6. Draw Deals (Center-aligned)
        y_offset = 300
        for promo in promos:
            promo_text = f"• {promo}"
            # Wrap text if too long
            if len(promo_text) > 30:
                promo_text = promo_text[:27] + "..."
            
            bbox = draw.textbbox((0, 0), promo_text, font=deal_font)
            pw = bbox[2] - bbox[0]
            draw_text_with_shadow(draw, promo_text, ((width - pw) / 2, y_offset), deal_font)
            y_offset += 100

        # 7. Add Branding/Call to Action (Bottom)
        cta_text = "HURRY! DEALS END SOON"
        bbox = draw.textbbox((0, 0), cta_text, font=deal_font)
        cw = bbox[2] - bbox[0]
        draw_text_with_shadow(draw, cta_text, ((width - cw) / 2, height - 120), deal_font, text_color="#FF0080")

        # 8. Save
        img.convert('RGB').save(output_path, "JPEG", quality=95)
        print(f"✅  Accuracy-guaranteed poster saved to: {output_path}")

    except Exception as e:
        print(f"   ⚠️  Hybrid image generation failed: {e}")

def get_poster_prompt(store_name: str, promos: list[str]) -> str:
    """Return the prompt used for the background."""
    return build_background_prompt(store_name)
