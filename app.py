import streamlit as st
import google.generativeai as genai
import json

# --- 1. LUXURY INTERFACE ---
st.set_page_config(page_title="CookSwipe Elite", page_icon="🥘", layout="wide")

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #050505; color: white; }
    .main-card {
        background: #111;
        border: 1px solid #333;
        border-radius: 35px;
        padding: 35px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }
    .tag { background: #FF6B00; color: white; padding: 5px 15px; border-radius: 50px; font-size: 12px; margin-right: 5px; }
    .stButton>button {
        background: white !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        height: 55px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. THE AI ENGINE (FREE TIER OPTIMIZED) ---
def generate_recipe_ai(ingredients):
    # These models are currently FREE in May 2026
    free_models = ['gemini-3.5-flash', 'gemini-3.1-flash-lite', 'gemini-2.5-flash-lite']
    
    prompt = f"""
    Create a unique recipe using: {ingredients}. 
    Return ONLY a raw JSON object: 
    {{"name": "...", "time": "...", "calories": "...", "spices": [], "steps": []}}
    """
    
    for m_name in free_models:
        try:
            model = genai.GenerativeModel(m_name)
            response = model.generate_content(prompt)
            # Clean AI chatter
            clean_json = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_json)
        except:
            continue # Try next free model if this one hits a limit
    return None

# --- 3. APP LOGIC ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("🔑 API Key not found in Streamlit Secrets!")

st.title("CookSwipe Elite 🍳")
user_input = st.text_input("What's in your fridge?", "Chicken, Avocado, Lime")

if st.button("DESIGN MASTERPIECE"):
    if user_input:
        with st.spinner("👨‍🍳 AI Chef is crafting your dish..."):
            data = generate_recipe_ai(user_input)
            
            if data:
                col1, col2 = st.columns([1, 1.5])
                with col1:
                    # High-quality photography link
                    st.image(f"https://source.unsplash.com/800x1000/?gourmet,{data['name'].replace(' ', ',')}", use_column_width=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="main-card">
                        <span class="tag">⏱ {data['time']}</span>
                        <span class="tag">🔥 {data['calories']} kcal</span>
                        <h1 style="color:white; margin-top:15px;">{data['name']}</h1>
                        <hr style="border:0.5px solid #222;">
                        <h4 style="color:#FF6B00;">Essential Spices</h4>
                        <p>{", ".join(data['spices'])}</p>
                        <h4 style="color:#FF6B00;">Steps</h4>
                        {"".join([f"<p><b>{i+1}.</b> {s}</p>" for i, s in enumerate(data['steps'])])}
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
            else:
                st.error("Free Tier Limit Reached. Please wait 60 seconds and try again!")
