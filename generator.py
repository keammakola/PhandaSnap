"""
generator.py
------------
Uses the Gemini API (google-genai SDK) to generate South African-style
marketing content for various use cases.
"""

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

SCENARIO_CONTEXTS = {
    "General Hustle": "A high-energy, viral social media style (TikTok/Instagram). Use extreme hype and FOMO.",
    "WhatsApp Status": "Short, punchy, and emoji-heavy. Perfect for quick viewing and high conversion on mobile.",
    "Spaza/Store Sale": "Traditional local 'radio ad' style. Focus heavily on prices and immediate store visits.",
    "Community Market": "Inviting, friendly, and warm. Focus on community spirit and high-quality local products.",
    "NGO Announcement": "Clear, informative, and community-focused. Use a helpful and respectful but engaging tone.",
    "Creative Agency": "Balanced, professional, and sophisticated. Focus on clear brand messaging and perfect tone."
}

def build_prompt(store_name: str, promo_end: str, promos: list[str], language: str, scenario: str) -> str:
    promo_list = "\n".join(f"  - {p}" for p in promos)
    context = SCENARIO_CONTEXTS.get(scenario, SCENARIO_CONTEXTS["General Hustle"])
    
    return f"""
You are an expert South African social media marketer and content creator.
Your goal is to create a marketing campaign for the following scenario: **{scenario}**

**SCENARIO CONTEXT:**
{context}

**REQUIREMENTS:**
1. The entire response must be in {language}.
2. Use authentic South African slang and expressions that match {language} and the **{scenario}** vibe.
3. Mention the store/organization name ({store_name}), all deals/info clearly, and the end date ({promo_end}).
4. Ensure the tone matches the scenario perfectly.

**OUTPUT FORMAT:**
You must provide exactly TWO sections separated by "===VOICEOVER===":

[Section 1: The Caption/Text Component]
Optimized for {scenario}.

===VOICEOVER===

[Section 2: The Spoken Component]
Write the script for a voiceover or voice note. NO emojis. NO hashtags. NO stage directions. Just the exact, punchy words meant to be spoken out loud.

Store name: {store_name}
Valid until: {promo_end}
Current deals/info:
{promo_list}
""".strip()


def generate_script(store_name: str, promo_end: str, promos: list[str], language: str = "English", scenario: str = "General Hustle") -> tuple[str, str]:
    """Call Gemini and return (caption, voiceover)."""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt = build_prompt(store_name, promo_end, promos, language, scenario)

    print(f"\n⚡  Generating {scenario} campaign in {language} with Gemini...")
    
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
