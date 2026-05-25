import streamlit as st
import json
import requests
import time
import base64
import random

# --- 1. PREMIUM GLASSMORPHISM DARK LUXURY THEME ---
st.set_page_config(
    page_title="CookSwipe Elite - AI Gastronomy",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom injection of modern typography, matte black canvas, and custom glows
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #050505;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #F3F4F6;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(5, 5, 5, 0.5);
        backdrop-filter: blur(12px);
    }
    
    /* Glowing Titles */
    .brand-glow {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(135deg, #FF5E00 0%, #FF9E00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1.5px;
        margin-bottom: 0px;
    }
    
    /* Luxury Glass Cards */
    .glass-panel {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 30px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
    }
    
    .mascot-bubble {
        background: rgba(255, 94, 0, 0.08);
        border: 1px solid rgba(255, 94, 0, 0.2);
        border-radius: 20px;
        padding: 15px;
        color: #FFE6D5;
        font-style: italic;
        margin-bottom: 20px;
    }
    
    /* Ingredient Chips styling */
    .chip {
        display: inline-flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 6px 14px;
        border-radius: 100px;
        font-size: 13px;
        margin: 4px;
        color: #E5E7EB;
        transition: all 0.2s ease;
    }
    
    .chip-active {
        background: rgba(255, 94, 0, 0.15) !important;
        border: 1px solid #FF5E00 !important;
        color: #FF9E00 !important;
        font-weight: 600;
    }
    
    /* Buttons styles */
    .stButton>button {
        background: linear-gradient(135deg, #FF5E00 0%, #FF7A00 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 12px 24px !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(255, 94, 0, 0.3) !important;
    }
    
    /* Recipe step formatting */
    .step-card {
        background: rgba(255, 255, 255, 0.01);
        border-left: 4px solid #FF5E00;
        padding: 15px 20px;
        margin-bottom: 15px;
        border-radius: 0 15px 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SECURE EXPONENTIAL BACKOFF GEMINI CLIENT ---
def call_gemini_api(prompt, system_instruction="", is_image=False, image_bytes=None):
    """
    Direct REST invocation of the official gemini-2.5-flash-preview-09-2025 model.
    Implements 5-step exponential backoff retries for free tier stability.
    """
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        return {"error": "API Key is missing from your Streamlit Secrets!"}
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    # Configure Payload based on Text vs Image inputs
    if is_image and image_bytes:
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inlineData": {
                            "mimeType": "image/jpeg",
                            "data": base64_image
                        }
                    }
                ]
            }]
        }
    else:
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}
            
    # Exponential Backoff delays: 1s, 2s, 4s, 8s, 16s
    backoff_delays = [1, 2, 4, 8, 16]
    
    for attempt, delay in enumerate(backoff_delays):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                if is_image:
                    return text_response
                return json.loads(text_response)
            elif response.status_code == 429: # Rate limit
                time.sleep(delay)
            else:
                time.sleep(delay)
        except Exception:
            time.sleep(delay)
            
    return None

# --- 3. SESSION STATE ENGINE ---
if 'view' not in st.session_state: st.session_state.view = "fridge"
if 'fridge_items' not in st.session_state: st.session_state.fridge_items = {"Paneer", "Spinach", "Garlic", "Onion"}
if 'deck' not in st.session_state: st.session_state.deck = []
if 'deck_idx' not in st.session_state: st.session_state.deck_idx = 0
if 'active_recipe' not in st.session_state: st.session_state.active_recipe = None
if 'xp' not in st.session_state: st.session_state.xp = 150
if 'streak' not in st.session_state: st.session_state.streak = 3
if 'calories_consumed' not in st.session_state: st.session_state.calories_consumed = 320
if 'favorites' not in st.session_state: st.session_state.favorites = []

# --- 4. SIDEBAR: MASCOT & GAMIFICATION DASHBOARD ---
with st.sidebar:
    st.markdown("<h2 style='color:#FF5E00; margin-bottom:0;'>Chef Gusteau 👨‍🍳</h2>", unsafe_allow_html=True)
    
    # Mascot Dialog Bubble reacts dynamically based on app view state
    mascot_phrases = {
        "fridge": "Gusteau says: 'What beautiful treasures do we have hiding in our fridge today?'",
        "swipe": "Gusteau says: 'Swipe right on what makes your heart skip a beat! Let's build a masterpiece.'",
        "cook": "Gusteau says: 'Chop, sauté, plate! Your hands are the brush, the pan is the canvas!'",
        "gamify": "Gusteau says: 'Ah! Look at you earning your stars! A master in the making.'"
    }
    st.markdown(f'<div class="mascot-bubble">{mascot_phrases.get(st.session_state.view, mascot_phrases["fridge"])}</div>', unsafe_allow_html=True)
    
    st.markdown("<hr style='border:0.1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("### 🏆 Chef Level")
    
    # Simple interactive level algorithm
    current_level = int(st.session_state.xp / 100) + 1
    xp_progress = st.session_state.xp % 100
    
    st.write(f"**Level {current_level} Gastronomer**")
    st.progress(xp_progress / 100)
    st.write(f"✨ {st.session_state.xp} XP | 🔥 {st.session_state.streak} Day Hot Streak")
    
    # Daily Calorie Dashboard
    st.markdown("<hr style='border:0.1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("### 📊 Today's Progress")
    st.write(f"Calories Consumed: **{st.session_state.calories_consumed}** / 2000 kcal")
    st.progress(min(st.session_state.calories_consumed / 2000, 1.0))
    
    # Badges display
    st.markdown("<hr style='border:0.1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("### 🏅 Active Badges")
    st.write("🟢 **Master Sauté Chef**")
    if st.session_state.streak >= 3:
         st.write("🔥 **3-Day Flame Badge**")
    if st.session_state.calories_consumed < 1500:
         st.write("🥗 **Healthy Hero Star**")

# --- 5. APP VIEW 1: THE SMART FRIDGE & AI SCANNER ---
if st.session_state.view == "fridge":
    st.markdown("<h1 class='brand-glow'>CookSwipe Elite</h1>", unsafe_allow_html=True)
    st.markdown("##### Turn your raw inventory into Michelin-Star culinary artwork.")
    
    tab_fridge, tab_scanner = st.tabs(["🧊 Virtual Fridge Station", "📷 Holographic Food Scanner"])
    
    with tab_fridge:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("Add Custom Ingredients")
        
        col_add, col_space = st.columns([2, 1])
        with col_add:
            new_item = st.text_input("What else did you buy?", placeholder="e.g. Avocado, Paneer, Mushroom...", key="new_ing")
            if st.button("Add to Fridge") and new_item:
                st.session_state.fridge_items.add(new_item.strip().capitalize())
                st.rerun()
                
        st.write("#### Double-Tap / Click to remove items currently in your Fridge:")
        
        # Displaying floating chips
        all_possible = ["Paneer", "Spinach", "Garlic", "Onion", "Tomato", "Chicken", "Eggs", "Milk", "Cheese", "Bread", "Rice", "Avocado", "Lemon", "Mushrooms"]
        for item in all_possible:
            is_active = item in st.session_state.fridge_items
            class_style = "chip-active" if is_active else ""
            if st.button(f"{'🛒' if is_active else '➕'} {item}", key=f"chip_{item}"):
                if is_active:
                    st.session_state.fridge_items.remove(item)
                else:
                    st.session_state.fridge_items.add(item)
                st.rerun()
                
        st.write("---")
        
        col_mood, col_vibe = st.columns(2)
        with col_mood:
            cuisine_mood = st.selectbox("Current Culinary Vibe", ["Authentic Indian", "Modern Fusion", "Street Style", "Minimalist Clean Eat"])
        with col_vibe:
            cook_style = st.selectbox("Prep Complexity", ["Lazy (Under 10 Mins)", "Intermediate Sauté", "Full Gastronomy"])
            
        st.write("")
        if st.button("🚀 IGNITE THE SWIPE ENGINE", use_container_width=True):
            if len(st.session_state.fridge_items) < 2:
                st.warning("Chef Gusteau says: 'Please pick at least 2 ingredients so we can make something beautiful!'")
            else:
                with st.spinner("🍽️ Running flavor matchmaking..."):
                    # Strict prompt for structured cards
                    prompt = f"""
                    You are a world-class culinary AI. Analyze these ingredients: {list(st.session_state.fridge_items)}.
                    Design exactly 3 premium recipes fitting the '{cuisine_mood}' and '{cook_style}' styles.
                    Return ONLY a JSON array containing exactly 3 objects matching this structure:
                    [
                      {{
                        "name": "Creative Gastronomy Name",
                        "time": "e.g. 12 mins",
                        "calories": 350,
                        "type": "Veg or Non-Veg",
                        "spices": ["spice 1", "spice 2"],
                        "steps": ["Step 1 detailing michelin technique", "Step 2 detailed sauté rules", "Step 3 final plating"],
                        "match": 90,
                        "substitutes": "If missing items, swap Paneer with Tofu or Spinach with Kale",
                        "tip": "Chef's pro trick here"
                      }}
                    ]
                    """
                    response_json = call_gemini_api(prompt, system_instruction="Output raw JSON array strictly. Do not include formatting.")
                    if response_json and isinstance(response_json, list):
                        st.session_state.deck = response_json
                        st.session_state.deck_idx = 0
                        st.session_state.view = "swipe"
                        st.rerun()
                    else:
                        st.error("Connection congestion. Please hit Ignite again to kickstart.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab_scanner:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("📸 AI Food Vision Scanner")
        st.write("Present ingredients to your camera. Gusteau's AI vision will auto-fill your inventory!")
        
        img_capture = st.camera_input("Scanner Interface")
        if img_capture is not None:
            with st.spinner("🧠 Scanning photo for raw ingredients..."):
                vision_prompt = "Analyze this food/kitchen photo. List only the raw ingredients you clearly see as a comma-separated list of items."
                detected_text = call_gemini_api(vision_prompt, is_image=True, image_bytes=img_capture.getvalue())
                if detected_text:
                    detected_items = [x.strip().capitalize() for x in detected_text.split(",") if len(x.strip()) > 1]
                    for item in detected_items:
                        st.session_state.fridge_items.add(item)
                    st.success(f"Successfully identified and added: {', '.join(detected_items)}")
                    time.sleep(1)
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- 6. APP VIEW 2: THE COOKSWIPE DECK (TINDER SWIPE INTERFACE) ---
elif st.session_state.view == "swipe":
    st.markdown("<h1 class='brand-glow'>CookSwipe Deck 📱</h1>", unsafe_allow_html=True)
    
    if not st.session_state.deck:
        st.warning("Deck is currently empty. Redirecting to Fridge...")
        st.session_state.view = "fridge"
        st.rerun()
        
    recipe = st.session_state.deck[st.session_state.deck_idx % len(st.session_state.deck)]
    
    # Beautiful image query fallback using LoremFlickr (highly reliable CDN)
    search_tag = recipe["name"].replace(" ", ",")
    img_url = f"https://loremflickr.com/1200/600/dish,{search_tag}/all"
    
    # Showcase full size responsive luxury card
    st.markdown(f'<img src="{img_url}" style="width:100%; height:420px; object-fit:cover; border-radius:35px; box-shadow: 0 15px 35px rgba(0,0,0,0.6); margin-bottom:25px;">', unsafe_allow_html=True)
    
    col_card, col_details = st.columns([1.5, 1])
    
    with col_card:
        st.markdown(f"""
        <div class="glass-panel">
            <span class="chip chip-active">⏱ {recipe['time']}</span>
            <span class="chip chip-active">🔥 {recipe['calories']} kcal</span>
            <span class="chip chip-active">🎯 {recipe['match']}% Match</span>
            <h1 style="color:white; margin-top:20px; font-size:42px;">{recipe['name']}</h1>
            <p style="font-size:18px; color:#FF9E00; font-weight:600;">{recipe['type']}</p>
            <hr style="border:0.1px solid rgba(255,255,255,0.1); margin: 20px 0;">
            <p style="font-size:16px; color:#ccc;">{recipe['tip']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_details:
        st.markdown("<div class='glass-panel' style='height: 100%;'>", unsafe_allow_html=True)
        st.subheader("Swipe Control Deck")
        st.write("Decide the fate of this culinary masterpiece:")
        
        st.write("")
        col_no, col_cook, col_yes = st.columns(3)
        with col_no:
            if st.button("❌ Skip (Next)", use_container_width=True):
                st.session_state.deck_idx += 1
                st.rerun()
        with col_cook:
            if st.button("🍳 Cook Now", use_container_width=True):
                st.session_state.active_recipe = recipe
                st.session_state.view = "cook"
                st.rerun()
        with col_yes:
            if st.button("❤️ Save (Fav)", use_container_width=True):
                if recipe['name'] not in st.session_state.favorites:
                    st.session_state.favorites.append(recipe['name'])
                    st.toast(f"Saved {recipe['name']} to collection! +10 XP")
                    st.session_state.xp += 10
                st.session_state.deck_idx += 1
                st.rerun()
                
        st.write("---")
        st.markdown(f"**Aromatics required:** {', '.join(recipe['spices'])}")
        st.write(f"💡 **Substitutes:** {recipe['substitutes']}")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 7. APP VIEW 3: CHEF'S KITCHEN (STEP-BY-STEP COOKING MODE) ---
elif st.session_state.view == "cook":
    recipe = st.session_state.active_recipe
    if not recipe:
        st.session_state.view = "fridge"
        st.rerun()
        
    st.markdown(f"<h1 class='brand-glow'>Active Kitchen: {recipe['name']}</h1>", unsafe_allow_html=True)
    
    if st.button("⬅️ Discard & Return to Deck"):
        st.session_state.view = "swipe"
        st.rerun()
        
    col_steps, col_tools = st.columns([1.8, 1])
    
    with col_steps:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("Execution Blueprints")
        
        for idx, step in enumerate(recipe['steps']):
            st.markdown(f"""
            <div class="step-card">
                <span style="font-weight:800; color:#FF5E00; font-size:18px;">STEP {idx+1}</span>
                <p style="font-size:18px; margin-top:5px; color:#F3F4F6;">{step}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_tools:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("Kitchen Tool Station")
        
        # Interactive Active Cooking Timer
        st.write("⏱ **Sauté Prep Timer**")
        timer_col, timer_btn = st.columns([2, 1])
        with timer_col:
            timer_duration = st.number_input("Duration (seconds)", min_value=1, value=10)
        with timer_btn:
            start_timer = st.button("Start Timer")
            
        if start_timer:
            progress_bar = st.progress(1.0)
            status_text = st.empty()
            for remaining in range(timer_duration, -1, -1):
                progress_bar.progress(remaining / timer_duration)
                status_text.markdown(f"⏱ **{remaining} seconds remaining...**")
                time.sleep(1)
            status_text.success("🔥 Sauté step completed!")
            st.balloons()
            
        st.write("---")
        st.subheader("Smart Substitutions")
        st.write(recipe['substitutes'])
        
        st.write("---")
        st.write("🗣 **Gusteau's Voice guidance Tip:**") 
        st.info("Don't turn your back on hot garlic, it burns in the blink of an eye!")
        
        if st.button("🏆 DISH FINISHED & PLATED!", use_container_width=True):
            st.balloons()
            st.session_state.calories_consumed += recipe['calories']
            st.session_state.xp += 50
            st.session_state.streak += 1
            st.success("Successfully logged calories, XP gained! Excellent job Chef!")
            time.sleep(2)
            st.session_state.view = "fridge"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
