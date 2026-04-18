"""
generator.py
------------
Uses the Gemini API (google-genai SDK) to generate a South African-style
hype radio ad script from store discount data.
"""

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


def build_prompt(store_name: str, promo_end: str, promos: list[str], language: str) -> str:
    promo_list = "\n".join(f"  - {p}" for p in promos)
    return f"""
You are an expert social media marketer and content creator.
Create a viral social media post (TikTok/Instagram Reels style) for the following store promotion.

**REQUIREMENTS:**
1. The entire response must be in {language}.
2. Use authentic South African slang and expressions that match {language}.
3. The content must be extremely engaging, hype, and drive FOMO (Fear Of Missing Out).
4. Mention the store name, all deals clearly, and the promo end date.

**OUTPUT FORMAT:**
You must provide exactly TWO sections separated by "===VOICEOVER===":

[Section 1: The Social Media Caption]
Include engaging text, extreme hype, lots of emojis, and relevant hashtags.

===VOICEOVER===

[Section 2: The Voiceover Script]
Write the spoken script for a TikTok/Reel voiceover. NO emojis. NO hashtags. NO stage directions. Just the exact, punchy words meant to be spoken out loud (around 20-30 seconds read time).

Store name: {store_name}
Promotions valid until: {promo_end}
Current deals:
{promo_list}
""".strip()


def generate_script(store_name: str, promo_end: str, promos: list[str], language: str = "English") -> tuple[str, str]:
    """Call Gemini and return (caption, voiceover)."""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt = build_prompt(store_name, promo_end, promos, language)

    print("\n⚡  Generating viral social media caption & voiceover script with Gemini...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    
    output = response.text.strip()
    
    # Parse the split
    parts = output.split("===VOICEOVER===")
    if len(parts) == 2:
        caption = parts[0].strip()
        voiceover = parts[1].strip()
    else:
        # Fallback if AI fails to format properly
        caption = output
        voiceover = output

    return caption, voiceover
