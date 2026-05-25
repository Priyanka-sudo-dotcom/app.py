import streamlit as st
import google.generativeai as genai
import json
import requests
import random

# --- 1. LUXURY STYLING (THE VIBE) ---
st.set_page_config(page_title="CookSwipe Elite", page_icon="🥘", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #050505;
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-size: 50px;
        font-weight: 700;
        background: linear-gradient(90deg, #FF6B00, #FFB800);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    .recipe-card {
        background: #111111;
        border: 1px solid #222;
        border-radius: 35px;
        padding: 40px;
        margin-top: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.8);
    }
    
    .metric-tag {
        background: rgba(255, 107, 0, 0.1);
        border: 1px solid rgba(255, 107, 0, 0.3);
        color: #FF6B00;
        padding: 8px 20px;
        border-radius: 100px;
        font-size: 14px;
        font-weight: 600;
        margin-right: 10px;
    }
    
    .spice-pill {
        background: #1A1A1A;
        border: 1px solid #333;
        padding: 5px 15px;
        border-radius: 10px;
        margin: 5px;
        display: inline-block;
    }

    .stButton>button {
        background: linear-gradient(90deg, #FF6B00, #FF4500) !important;
        color: white !important;
        border: none !important;
        padding: 15px 30px !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        transition: 0.3s !important;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. THE BRAIN (AI & IMAGE TOOLS) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("⚠️ API Key missing in Secrets!")

def get_food_image(query):
    return f"https://source.unsplash.com/1200x800/?food,{query.replace(' ', ',')}"

# --- 3. THE UI LAYOUT ---
st.markdown("<h1 class='main-title'>CookSwipe Elite</h1>", unsafe_allow_html=True)
st.write("### AI-Powered Gastronomy for your Kitchen")

col_left, col_right = st.columns([1, 2])

with col_left:
    st.write("#### 🛒 Inventory")
    ingredients = st.text_area("Type your available ingredients:", 
                              placeholder="e.g. Salmon, Asparagus, Lemon, Garlic...",
                              height=150)
    
    mood = st.select_slider("Select Dining Mood:", 
                            options=["Lazy", "Healthy", "Comfort", "Chatpata", "Gourmet"])
    
    generate_btn = st.button("✨ DESIGN RECIPE")

# --- 4. THE MAGIC LOGIC ---
if generate_btn and ingredients:
    with st.spinner("🍽️ Orchestrating your culinary masterpiece..."):
        prompt = f"""
        Act as a Michelin-star chef. Create a world-class recipe using: {ingredients}.
        The mood is {mood}. 
        Return ONLY a JSON object with these keys:
        "name", "time", "calories", "difficulty", "description", "spices", "steps", "nutrition_fact"
        """
        
        try:
            response = model.generate_content(prompt)
            data = json.loads(response.text.replace('```json', '').replace('```', ''))
            
            # Show the Result in col_right
            with col_right:
                # Dynamic High Quality Image
                st.image(get_food_image(data['name']), use_column_width=True)
                
                st.markdown(f"""
                <div class="recipe-card">
                    <div style="display: flex; margin-bottom: 20px;">
                        <span class="metric-tag">⏱ {data['time']}</span>
                        <span class="metric-tag">🔥 {data['calories']} kcal</span>
                        <span class="metric-tag">👨‍🍳 {data['difficulty']}</span>
                    </div>
                    <h1 style="color:white; margin-bottom:10px;">{data['name']}</h1>
                    <p style="color:#888; font-size:18px; line-height:1.6;">{data['description']}</p>
                    <hr style="border: 0.1px solid #333; margin: 30px 0;">
                    
                    <h3 style="color:#FF6B00;">Essential Spices</h3>
                    <div style="margin-bottom:20px;">
                        {"".join([f'<div class="spice-pill">{s}</div>' for s in data['spices']])}
                    </div>
                    
                    <h3 style="color:#FF6B00;">Culinary Steps</h3>
                    {"".join([f"<div style='margin-bottom:15px;'><b style='color:#FF6B00;'>{i+1}.</b> {step}</div>" for i, step in enumerate(data['steps'])])}
                    
                    <div style="background:#1A1A1A; padding:20px; border-radius:20px; margin-top:30px; border:1px solid #333;">
                        <small style="color:#555;">HEALTH INSIGHT</small><br>
                        <span style="color:#00FF88;">{data['nutrition_fact']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action Buttons
                c1, c2 = st.columns(2)
                with c1: st.button("❤️ SAVE TO COLLECTION")
                with c2: st.button("🛒 ADD TO GROCERY LIST")

        except Exception as e:
            st.error("The AI Chef is currently overbooked. Try clicking generate again!")
else:
    with col_right:
        st.info("Input your ingredients and click 'Design Recipe' to begin your infinite culinary journey.")
