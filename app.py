"""
app.py
------
Flask backend for the PhandaSnap Marketing Assistant SaaS.
Manages onboarding, content calendar, trigger simulation, outcome analytics,
simulated WhatsApp chatbot, and media serving.
"""

import os
import io
import json
import zipfile
import datetime
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
import generator
import audio

# ponytail: load env on startup
load_dotenv()

app = Flask(__name__)

if os.environ.get("VERCEL"):
    DB_FILE = "/tmp/db.json"
    OUTPUT_DIR = "/tmp/outputs"
else:
    DB_FILE = "db.json"
    OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_db():
    """Load JSON database, initialize default state if missing."""
    # ponytail: default structure inlined to save space
    default_state = {
        "onboarded": False,
        "profile": {},
        "calendar": [],
        "analytics": {
            "total_campaigns": 0,
            "total_clicks": 0,
            "total_redemptions": 0,
            "estimated_revenue": 0,
            "insights": ["Complete onboarding to receive custom operator insights."]
        },
        "chat_history": [
            {"role": "assistant", "content": "Yo! PhandaSnap AI Marketing Operator here. ⚡ Ready to help you tell customers what's hot today. Let's get your business profile set up!"}
        ],
        "simulated_weather": "Mild",
        "simulated_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "is_payday": False
    }
    
    # ponytail: helper to inject api key availability dynamically
    has_api_key = bool(os.environ.get("GEMINI_API_KEY"))
    
    if not os.path.exists(DB_FILE):
        default_state["api_key_available"] = has_api_key
        return default_state
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
            db["api_key_available"] = has_api_key
            return db
    except Exception:
        default_state["api_key_available"] = has_api_key
        return default_state

def save_db(db):
    """Save database to JSON file."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

def get_demo_calendar(profile, start_date):
    """Generate default mock calendar for Demo Mode, utilizing the extensive profile fields."""
    slow_day = profile.get("slow_day", "Tuesday")
    busy_day = profile.get("busiest_day", "Saturday")
    signature = profile.get("offering_popular", "Signature Platter")
    slow_seller = profile.get("offering_slow", "Wors roll")
    price_tier = profile.get("price_tier", "R50 - R100")
    township = profile.get("location", "Soweto")
    
    # ponytail: build dynamic templates reflecting the merchant's real slow/busy days & signature offerings
    calendar = []
    base_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    for i in range(14):
        curr_date = base_date + datetime.timedelta(days=i)
        day_name = curr_date.strftime("%A")
        
        # Determine trigger & concept based on day category
        if day_name == slow_day:
            trigger = f"💤 Slow {slow_day} Foot Traffic"
            concept = f"{slow_day} {slow_seller} Push"
            deals = [f"Get our slow-moving {slow_seller} at a special promo price", f"Boost sales in {township} today!"]
        elif day_name == busy_day:
            trigger = f"🔥 Saturday Peak Traffic"
            concept = f"Weekend {signature} Feast"
            deals = [f"Platter deal featuring our popular {signature}", "Order early before we sell out!"]
        elif day_name == "Sunday":
            trigger = f"🙏 Sunday Soul Food"
            concept = f"Sunday Seven Colours Special"
            deals = [f"Seven Colours plate with {signature}", "Pensioners get 10% off today"]
        else:
            # Alternate mid-week slump vs weather trigger
            if i % 3 == 0:
                trigger = f"☀️ Hot Weather Trigger (32°C)"
                concept = f"Ice-Cold Drink + {signature} Combo"
                deals = [f"Buy our signature {signature}, get a cold drink for R10", "Valid today only!"]
            elif i % 3 == 1:
                trigger = f"💰 Mid-week Payday Hype"
                concept = f"{township} Mid-month Slump Buster"
                deals = [f"Get our {slow_seller} combo at a discount price", f"Perfect budget lunch under {price_tier.split(' ')[0]}"]
            else:
                trigger = f"📢 Community Favorite"
                concept = f"{profile.get('store_name')} Daily Special"
                deals = [f"Special bundle on {signature} & {slow_seller}"]
                
        calendar.append({
            "id": i,
            "date": curr_date.strftime("%Y-%m-%d"),
            "day_name": day_name,
            "trigger": trigger,
            "concept": concept,
            "channel": "WhatsApp Status" if i % 2 == 0 else "Facebook Page",
            "deals": deals,
            "status": "Pending Approval",
            "outcomes": None,
            "assets": None
        })
    return calendar

@app.route("/")
def index():
    # ponytail: reset DB state on root load to make it dead simple to rerun the wizard on refresh
    db = {
        "onboarded": False,
        "profile": {},
        "calendar": [],
        "analytics": {
            "total_campaigns": 0,
            "total_clicks": 0,
            "total_redemptions": 0,
            "estimated_revenue": 0,
            "insights": ["Complete onboarding to receive custom operator insights."]
        },
        "chat_history": [
            {"role": "assistant", "content": "Yo! PhandaSnap AI Marketing Operator here. ⚡ Ready to help you tell customers what's hot today. Let's get your business profile set up!"}
        ],
        "simulated_weather": "Mild",
        "is_payday": False
    }
    save_db(db)
    return render_template("index.html")

@app.route("/api/dashboard", methods=["GET"])
def get_dashboard():
    db = load_db()
    return jsonify(db)


@app.route("/api/set_api_key", methods=["POST"])
def set_api_key():
    """Set the GEMINI_API_KEY in the local .env and process env so generator can use Gemini.
    This persists the key to .env and updates runtime os.environ so subsequent requests use Gemini.
    """
    data = request.json or {}
    key = (data.get("key") or "").strip()
    if not key:
        return jsonify({"error": "No API key provided"}), 400

    env_path = ".env"
    lines = []
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            lines = []

    replaced = False
    for i, line in enumerate(lines):
        if line.strip().startswith("GEMINI_API_KEY="):
            lines[i] = f'GEMINI_API_KEY="{key}"\n'
            replaced = True
            break

    if not replaced:
        lines.append(f'GEMINI_API_KEY="{key}"\n')

    try:
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
    except Exception as e:
        return jsonify({"error": f"Failed to write .env: {e}"}), 500

    # Update runtime env for immediate use
    os.environ["GEMINI_API_KEY"] = key

    db = load_db()
    db["api_key_available"] = True
    save_db(db)
    return jsonify(db)


@app.route('/dashboard')
def dashboard_page():
    # standalone dashboard page
    return render_template('dashboard.html')

@app.route("/api/reset", methods=["POST"])
def reset_db():
    db = {
        "onboarded": False,
        "profile": {},
        "calendar": [],
        "analytics": {
            "total_campaigns": 0,
            "total_clicks": 0,
            "total_redemptions": 0,
            "estimated_revenue": 0,
            "insights": ["Complete onboarding to receive custom operator insights."]
        },
        "chat_history": [
            {"role": "assistant", "content": "Yo! PhandaSnap AI Marketing Operator here. ⚡ Ready to help you tell customers what's hot today. Let's get your business profile set up!"}
        ],
        "simulated_weather": "Mild",
        "is_payday": False
    }
    save_db(db)
    return jsonify(db)

@app.route("/api/onboard", methods=["POST"])
def onboard():
    data = request.json
    profile = data.get("profile", {})
    simulated_date = data.get("simulated_date", datetime.datetime.now().strftime("%Y-%m-%d"))
    
    db = load_db()
    db["profile"] = profile
    db["onboarded"] = True
    db["simulated_date"] = simulated_date
    
    # Check if Gemini key is available
    if os.environ.get("GEMINI_API_KEY"):
        print("[INFO] Generating AI calendar with Gemini...")
        try:
            ai_data = generator.generate_calendar(profile, simulated_date)
            db["analytics"]["insights"] = [ai_data.get("diagnosis", "Keep driving promotion on slow days.")]
            
            # Map calendar items
            db["calendar"] = []
            for i, item in enumerate(ai_data.get("calendar", [])):
                db["calendar"].append({
                    "id": i,
                    "date": item.get("date"),
                    "day_name": item.get("day_name"),
                    "trigger": item.get("trigger"),
                    "concept": item.get("concept"),
                    "channel": item.get("channel", "WhatsApp Status"),
                    "deals": item.get("deals", []),
                    "status": "Pending Approval",
                    "outcomes": None,
                    "assets": None
                })
        except Exception as e:
            print(f"[WARNING] Gemini calendar failed: {e}. Falling back to demo calendar.")
            db["calendar"] = get_demo_calendar(profile, simulated_date)
            db["analytics"]["insights"] = [f"💡 Focus on Wednesday specials and cold-drink weather triggers to optimize sales."]
    else:
        # Fallback to Demo mode
        db["calendar"] = get_demo_calendar(profile, simulated_date)
        db["analytics"]["insights"] = [
            "💡 PhandaSnap Demo Mode active: Foot traffic drops on Tuesdays. We recommend running a Tuesday Braai Platter promo.",
            "💡 Warm weather trigger active: Hot days double cooldrink sales. Auto-suggestions will update when weather shifts to Hot."
        ]
        
    db["chat_history"].append({
        "role": "assistant",
        "content": f"Awe {profile.get('store_name')}! 🚀 I've built your rolling 14-day marketing calendar based on your slow days ({profile.get('slow_day')}) and busiest days ({profile.get('busiest_day')}). Ready to generate your first campaign assets?"
    })
    
    save_db(db)
    return jsonify(db)

@app.route("/api/calendar/generate-assets", methods=["POST"])
def generate_assets():
    data = request.json
    item_id = int(data.get("id"))
    language = data.get("language", "English")
    
    db = load_db()
    calendar = db.get("calendar", [])
    
    # Find matching calendar item
    item = next((x for x in calendar if x["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Campaign item not found"}), 404
        
    store_name = db["profile"].get("store_name", "Our Store")
    deals = item["deals"]
    concept = item["concept"]
    trigger = item["trigger"]
    
    print(f"[INFO] Generating assets for campaign {item_id}: {concept}")
    
    # Generate copy suite
    if os.environ.get("GEMINI_API_KEY"):
        copy_suite = generator.generate_assets_for_campaign(store_name, concept, deals, trigger, language)
    else:
        # ponytail: local template generator for offline demo mode
        deals_str = ", ".join(deals)
        copy_suite = {
            "caption": f"🔥 Mzansi! You don't want to miss our {concept}! ⚡\n\n📢 SPECIAL DEALS:\n{deals_str}\n\n👉 Visit {store_name} today before it sells out! #PhandaSnap #LocalHustle",
            "whatsapp_text": f"Hey there! *{store_name}* here. 🌟 We have a special *{concept}* today:\n\n{deals_str}\n\nReply to this chat to secure yours now! 📲",
            "voiceover": f"Listen up! {store_name} is bringing the heat today with our {concept}! Get {deals_str} valid today only! Don't sleep on this, come visit us now!",
            "zulu_caption": f"Ningaphuthwa yi-{concept} yethu e-{store_name}! {deals_str}",
            "afrikaans_caption": f"Moenie ons {concept} by {store_name} misloop nie! {deals_str}",
            "sesotho_caption": f"O seke wa fetwa ke {concept} kwa {store_name}! {deals_str}",
            "english_caption": f"Don't miss out on our {concept} at {store_name}! {deals_str}"
        }
        
    # Generate audio tracks
    vo_bytes = audio.generate_audio_bytes(copy_suite["voiceover"])
    
    # Save audio files
    vo_path = os.path.join(OUTPUT_DIR, f"campaign_{item_id}_voiceover.wav")
    with open(vo_path, "wb") as f:
        f.write(vo_bytes)
        
    # Update item in database
    item["assets"] = {
        "copy_suite": copy_suite,
        "voiceover_url": f"/api/media/audio/{item_id}/voiceover",
    }
    
    save_db(db)
    return jsonify(item)

@app.route("/api/calendar/update-item", methods=["POST"])
def update_item():
    data = request.json
    item_id = int(data.get("id"))
    status = data.get("status")
    outcomes = data.get("outcomes")
    
    db = load_db()
    calendar = db.get("calendar", [])
    item = next((x for x in calendar if x["id"] == item_id), None)
    
    if not item:
        return jsonify({"error": "Campaign not found"}), 404
        
    if status:
        item["status"] = status
        if status == "Approved":
            db["analytics"]["total_campaigns"] += 1
            
    if outcomes:
        item["outcomes"] = outcomes
        item["status"] = "Completed"
        
        # Update analytics outcomes
        redemptions = int(outcomes.get("redemptions", 0))
        clicks = int(outcomes.get("clicks", 0))
        db["analytics"]["total_redemptions"] += redemptions
        db["analytics"]["total_clicks"] += clicks
        
        # Assume R50 average deal value for estimated revenue
        db["analytics"]["estimated_revenue"] += (redemptions * 50)
        
        # Add operator feedback log response
        feedback = outcomes.get("feedback", "Good response")
        insight = f"📝 Feedback Logged: '{item['concept']}' campaign on {item['day_name']} generated {redemptions} redemptions. Adjusting recommendation weights..."
        db["analytics"]["insights"].insert(0, insight)
        if len(db["analytics"]["insights"]) > 5:
            db["analytics"]["insights"] = db["analytics"]["insights"][:5]
            
        # Add automated Operator learning chat message
        db["chat_history"].append({
            "role": "assistant",
            "content": f"Awe! I've logged the feedback for the '{item['concept']}' campaign ({redemptions} customers redeemed it). I'm learning that {item['day_name']} promos drive solid results. I will suggest more {item['channel']} promos for this day!"
        })
        
    save_db(db)
    return jsonify(db)

@app.route("/api/simulate-trigger", methods=["POST"])
def simulate_trigger():
    data = request.json
    weather = data.get("weather")
    is_payday = data.get("is_payday")
    
    db = load_db()
    if weather:
        db["simulated_weather"] = weather
    if is_payday is not None:
        db["is_payday"] = is_payday
        
    # Check if there is an active swap trigger for today (index 0)
    if db["onboarded"] and len(db["calendar"]) > 0:
        today_item = db["calendar"][0]
        
        if db["simulated_weather"] == "Sunny & Hot":
            # Add alert to today's post
            today_item["swap_alert"] = {
                "reason": "☀️ High Temp Trigger (33°C, Sunny): Ideal weather for cold drink promos.",
                "concept": "Sunny Day Cool Down Splash",
                "deals": ["Buy any platter, get an ice-cold cooldrink for R10!", "Free cup of ice"]
            }
        elif db["simulated_weather"] == "Rainy & Cold":
            today_item["swap_alert"] = {
                "reason": "🌧️ Rainy & Cold Trigger: Customers will stay indoors. Boost comfort food delivery.",
                "concept": "Rainy Day Warm Platter",
                "deals": ["Hot soup or gravy cup free with any large plate", "Free Delivery in 1km"]
            }
        else:
            # Clear alert if mild
            today_item.pop("swap_alert", None)
            
        if db["is_payday"]:
            today_item["swap_alert"] = {
                "reason": "💰 Payday Weekend: High consumer spending power. Run a premium bundle.",
                "concept": "Month-End Payday Mega Feast",
                "deals": ["Super Braai Platter: Chuck, 2 Wors, Wings, Pap + 2L Drink for R199", "Free dessert muffin"]
            }

    save_db(db)
    return jsonify(db)

@app.route("/api/calendar/apply-swap", methods=["POST"])
def apply_swap():
    data = request.json
    item_id = int(data.get("id"))
    
    db = load_db()
    item = next((x for x in db["calendar"] if x["id"] == item_id), None)
    if not item or "swap_alert" not in item:
        return jsonify({"error": "No swap trigger available"}), 400
        
    alert = item["swap_alert"]
    item["concept"] = alert["concept"]
    item["deals"] = alert["deals"]
    item["trigger"] = alert["reason"]
    item["assets"] = None # Reset assets to force regeneration
    item.pop("swap_alert", None)
    
    db["chat_history"].append({
        "role": "assistant",
        "content": f"Trigger alert applied! ⚡ I've swapped the campaign concept to '{item['concept']}' to match the simulated triggers. Let's generate the assets for this new promo!"
    })
    
    save_db(db)
    return jsonify(db)

@app.route("/api/whatsapp/chat", methods=["POST"])
def whatsapp_chat():
    data = request.json
    message = data.get("message", "").strip()
    
    db = load_db()
    db["chat_history"].append({"role": "user", "content": message})
    
    # Generate bot response
    if os.environ.get("GEMINI_API_KEY"):
        try:
            reply = generator.chat_with_operator(db["profile"], db["calendar"], db["chat_history"], message)
        except Exception as e:
            reply = f"Awe my friend! 🚀 Got your message: '{message}'. Let's run a quick promo from the calendar. Ask me to generate the Tuesday flyer, sharp!"
    else:
        # ponytail: rule-based chatbot for offline demo
        msg_lower = message.lower()
        if "hello" in msg_lower or "hi" in msg_lower or "awe" in msg_lower:
            reply = f"Awe! PhandaSnap Operator here. ⚡ Ready to handle your marketing. Should we check what's pending on your content calendar?"
        elif "yes" in msg_lower or "approve" in msg_lower or "cool" in msg_lower:
            reply = "Sharp! 👍 I've approved that campaign. I'm generating the voice note and captions now. Check your dashboard in a second!"
        elif "weather" in msg_lower or "sunny" in msg_lower or "rain" in msg_lower:
            reply = f"Weather forecast is currently {db.get('simulated_weather', 'Mild')}. I've suggested a trigger-based campaign on your calendar to capitalize on this! ☀️"
        elif "slow" in msg_lower or "tuesday" in msg_lower:
            reply = f"Tuesdays are your slowest day, but we got this! I suggest running a R49 promo combo. Should I add it to the calendar?"
        else:
            reply = f"Bhuti/Sisi! Let's get that deal rolling. Reply 'yes' to approve the next calendar campaign, or tell me what specials you want to run today. 🚀"
            
    db["chat_history"].append({"role": "assistant", "content": reply})
    save_db(db)
    return jsonify(db)

@app.route("/api/media/audio/<int:item_id>/<type>")
def serve_audio(item_id, type):
    filename = f"campaign_{item_id}_{type}.wav"
    audio_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(audio_path):
        # Generate on the fly
        db = load_db()
        calendar = db.get("calendar", [])
        item = next((x for x in calendar if x["id"] == item_id), None)
        script = item["concept"] if item else "Special deal"
        audio.generate_audio(script, audio_path)
        
    return send_file(audio_path, mimetype="audio/wav")

@app.route("/api/download_zip/<int:item_id>")
def download_campaign_zip(item_id):
    db = load_db()
    calendar = db.get("calendar", [])
    item = next((x for x in calendar if x["id"] == item_id), None)
    if not item or not item.get("assets"):
        return jsonify({"error": "Assets not generated for this campaign"}), 400
        
    store_name = db["profile"].get("store_name", "Store")
    assets = item["assets"]
    copy_suite = assets["copy_suite"]
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("captions/social_caption.txt", copy_suite.get("caption", ""))
        zip_file.writestr("captions/whatsapp_broadcast.txt", copy_suite.get("whatsapp_text", ""))
        zip_file.writestr("captions/voiceover_script.txt", copy_suite.get("voiceover", ""))
        zip_file.writestr("captions/zulu_caption.txt", copy_suite.get("zulu_caption", ""))
        zip_file.writestr("captions/afrikaans_caption.txt", copy_suite.get("afrikaans_caption", ""))
        zip_file.writestr("captions/sesotho_caption.txt", copy_suite.get("sesotho_caption", ""))
        zip_file.writestr("captions/community_whatsapp_group.txt", copy_suite.get("community_whatsapp_group", ""))
        zip_file.writestr("captions/tiktok_script.txt", copy_suite.get("tiktok_script", ""))
            
    zip_buffer.seek(0)
    safe_name = store_name.lower().replace(" ", "_")
    return send_file(
        zip_buffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name=f"{safe_name}_campaign_{item_id}.zip"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
