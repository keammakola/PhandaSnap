"""
generator.py
------------
Operator Engine powered by Gemini.
Handles business profile diagnosis, 14-day calendar generation,
copy asset generation, and the simulated WhatsApp operator chatbot.
"""

import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# ponytail: load env once here
load_dotenv()

def get_client():
    # ponytail: helper to return configured client
    return genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_calendar(profile: dict, simulated_date: str) -> dict:
    """
    Generate a 14-day content calendar and strategic diagnosis based on an extensive business profile.
    """
    client = get_client()
    campaign_type = profile.get("campaign_type", "promo")
    
    if campaign_type == "competition":
        campaign_details = f"""
        CAMPAIGN TYPE: Competition/Giveaway
        - Prize: {profile.get('comp_prize')}
        - Entry Rule: {profile.get('comp_rule')}
        - Draw Date: {profile.get('comp_date')}
        Goal: Build massive community hype and engagement in {profile.get('location')} by telling residents how to enter and counting down.
        """
    elif campaign_type == "branding":
        campaign_details = f"""
        CAMPAIGN TYPE: branding / "Be Out There" brand trust
        - Main Message/Vibe: {profile.get('brand_vibe')}
        - Store Slogan: {profile.get('brand_slogan')}
        Goal: Create local brand trust and community connection in {profile.get('location')} by highlighting staff, customer testimonials, greetings, and credentials.
        """
    else:
        campaign_details = f"""
        CAMPAIGN TYPE: Sales Promotion
        - Best Sellers: {profile.get('offering_popular')}
        - Slow Sellers: {profile.get('offering_slow')}
        - Average Deal Price Tier: {profile.get('price_tier')}
        - Slowest Day: {profile.get('slow_day')}
        - Daily Rush Hours: {profile.get('peak_hours')}
        Goal: Drive foot traffic on slow days using targeted discount deals and combo packages.
        """

    prompt = f"""
    You are the PhandaSnap Operator Engine. You are a senior marketing strategist for South African township and small businesses.
    Based on this extensive business profile:
    - Store Name: {profile.get('store_name')}
    - Category: {profile.get('category')}
    - Location / Township: {profile.get('location')}
    - Preferred Language: {profile.get('language')}
    {campaign_details}
    - Marketing Channels: {", ".join(profile.get('channels', []))}

    Task:
    1. Generate a strategic diagnosis/point-of-view (1-2 sentences) about how this business should execute this specific campaign type in {profile.get('location')}. Refer to the township name and details to make it personal.
    2. Generate a rolling 14-day calendar starting from simulated date: {simulated_date}.
       - Each day should have a campaign concept.
       - If it's a competition: Daily count-down posts, rule announcements, prize highlight, winner anticipation.
       - If it's a branding campaign: Staff spotlight, community greeting, customer quote, slogans.
       - If it's a promo campaign: Combo pricing, slow day discounts, rainy/hot day drink bundles.
       - Keep it extremely relevant to their township context.

    You MUST return a JSON object with exactly these keys:
    - "diagnosis": "Your 1-2 sentence strategic advice"
    - "calendar": A list of 14 objects, each containing:
      - "date": "YYYY-MM-DD"
      - "day_name": "Monday", "Tuesday", etc.
      - "trigger": "Reason for post (e.g., Prize Spotlight, Slow Day Combo, Slogan Greeting)"
      - "concept": "Catchy campaign concept title (e.g., Saturday Platter Boost)"
      - "channel": "Primary channel (e.g. WhatsApp Status, Facebook)"
      - "deals": ["Promo deal or call to action (e.g. buy a kota to enter, tag a friend)"]

    Return ONLY the raw JSON. Do not wrap in markdown or code blocks.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    # ponytail: parse and handle fallback in one place
    try:
        return json.loads(response.text.strip())
    except Exception as e:
        print(f"[ERROR] Failed parsing calendar: {e}. Raw: {response.text}")
        return {
            "diagnosis": "Keep driving sales with consistent daily promotions and localized WhatsApp statuses.",
            "calendar": [
                {
                    "date": simulated_date,
                    "day_name": "Today",
                    "trigger": "Welcome Boost",
                    "concept": f"Grand Launch at {profile.get('store_name')}",
                    "channel": "WhatsApp Status",
                    "deals": ["Special discount on popular items"]
                }
            ]
        }

def generate_assets_for_campaign(store_name: str, concept: str, deals: list, trigger: str, language: str) -> dict:
    """
    Generate all copy assets (captions, scripts, translations) for a specific calendar campaign.
    """
    client = get_client()
    deals_str = "\n".join(f"- {d}" for d in deals)
    prompt = f"""
    You are an expert South African social media marketer.
    Create a marketing copywriting suite for this campaign:
    - Store Name: {store_name}
    - Concept: {concept}
    - Trigger Reason: {trigger}
    - Selected Language: {language}
    - Promotional Deals:
    {deals_str}

    REQUIREMENTS:
    1. Primary content must be in {language} and use authentic South African slang/expressions suitable for township business promotion (e.g., sharp, choma, mzansi, spaza, shisanyama, yebo).
    2. Keep Rands formatted with 'R' (e.g. R49, R120) in all copy. Do not write out in words.
    3. For spoken voiceover/voicenote scripts: DO NOT include emojis, hashtags, or stage directions. Make them read smoothly.

    Return a JSON object with exactly these keys:
    - "caption": A high-energy TikTok/Reels caption in {language} with emojis and hashtags.
    - "whatsapp_text": A clean, emoji-rich WhatsApp broadcast message in {language}.
    - "voiceover": An energetic spoken video voiceover script in {language}.
    - "zulu_caption": The main caption translated/adapted into isiZulu.
    - "afrikaans_caption": The main caption translated/adapted into Afrikaans.
    - "sesotho_caption": The main caption translated/adapted into Sesotho.
    - "english_caption": The main caption translated/adapted into English.
    - "community_whatsapp_group": A warm, personal broadcast message for a community WhatsApp group (neighbours, regulars). Longer than the standard WhatsApp text, more conversational, uses the merchant's first name vibe. In {language}.
    - "tiktok_script": A punchy TikTok/Reels video script with a hook (0-3s), body (3-12s), and CTA (12-15s). No emojis. Written to be spoken on camera. In {language}.

    Return ONLY the raw JSON. Do not wrap in markdown or code blocks.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    try:
        return json.loads(response.text.strip())
    except Exception as e:
        print(f"[ERROR] Asset generation failed: {e}. Raw: {response.text}")
        return {
            "caption": f"Come try our {concept}! {deals_str}",
            "whatsapp_text": f"Hey customer! Check out our {concept}: {deals_str}",
            "voiceover": f"Get ready for the best deal in town at {store_name}!",
            "zulu_caption": "Ikhona into entsha!",
            "afrikaans_caption": "Kry jou spesiale aanbod vandag!",
            "sesotho_caption": "Fumana deal ya gago kajeno!",
            "english_caption": f"Check out our new special at {store_name}!",
            "community_whatsapp_group": f"Hey family! 👋 Just a quick one — {store_name} is running a {concept} today. {deals_str}. Come through and show love to your local. Sharp!",
            "tiktok_script": f"Hook: You won't believe what {store_name} is doing today. Body: We've got {concept} — {deals_str}. This is for the whole community, not just one person. CTA: Come through before it's gone. Location in bio."
        }

def chat_with_operator(profile: dict, calendar: list, history: list, message: str) -> str:
    """
    Chat bot agent acting as the PhandaSnap Operator on WhatsApp.
    """
    client = get_client()
    
    # ponytail: compact chat log serialization
    history_str = ""
    for msg in history[-10:]: # Limit context to last 10 messages
        role = "Merchant" if msg['role'] == 'user' else "PhandaSnap AI Operator"
        history_str += f"{role}: {msg['content']}\n"
        
    calendar_summary = "\n".join(
        f"- {item['date']} ({item['day_name']}): {item['concept']} [{item.get('status', 'Pending')}]"
        for item in calendar[:5]
    )

    prompt = f"""
    You are the PhandaSnap AI Marketing Operator on WhatsApp. You chat with township spaza, salon, or shisanyama owners to help them run their marketing campaigns.
    
    BUSINESS DETAILS:
    - Store: {profile.get('store_name')}
    - Category: {profile.get('category')}
    - Target: {profile.get('target_audience')}
    - Busiest Day: {profile.get('busiest_day')}, Slowest: {profile.get('slow_day')}
    - Best Sellers: {profile.get('offering_popular')}
    
    UPCOMING CALENDAR:
    {calendar_summary}

    GUIDELINES:
    1. Be friendly, encouraging, and local. Use South African township expressions (e.g. sharp bhuti, choma, mzansi, sho, yebo, spaza, shisanyama) in moderation.
    2. Keep responses brief (1-3 sentences maximum). Make it look like a WhatsApp message.
    3. Help the merchant approve pending content, run promotions on slow days, or check the weather triggers.
    4. If they say "yes" to a promo or ask to generate, tell them you've updated their calendar and created the assets!
    
    CHAT HISTORY:
    {history_str}
    
    Merchant: {message}
    PhandaSnap AI Operator:
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()
