import streamlit as st
import json
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="CookSwipe Evolution", layout="wide")
st.markdown("""
<style>
    .glass-card { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px; padding: 40px; }
    .stat-pill { background: rgba(255, 107, 0, 0.2); color: #FF6B00; padding: 8px 16px; border-radius: 50px; font-weight: bold; margin-right: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE EVOLUTION ENGINE ---
def call_evolution_ai(prompt):
    # Ensure API Key is loaded
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
    except Exception:
        st.error("🔑 GEMINI_API_KEY is missing from Streamlit secrets.")
        return None
    
    for model_name in ["gemini-1.5-flash", "gemini-1.5-pro"]:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            text = response.text.strip()
            
            # Robust JSON extraction
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
                
            return json.loads(text.strip())
        except Exception as e:
            continue
    return None

# --- 3. THE INTERFACE ---
st.markdown("<h1 style='font-size: 50px; font-weight: 800;'>CookSwipe <span style='color:#FF6B00;'>Evolution</span></h1>", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.8], gap="large")

with col_in:
    st.write("#### 📥 Kitchen Inventory")
    ingredients = st.text_area("What do you have?", "Egg, Bread, Cheese", height=100)
    
    st.write("#### 🎭 Choose Your Evolution")
    style = st.select_slider("Select Style", options=["Desi", "Continental", "Asian Fusion", "Street Style"])
    mood = st.selectbox("Cooking Mood", ["Lazy (5 mins)", "Healthy", "Cheat Meal", "Fine Dining"])

    if st.button("✨ GENERATE MASTERPIECE"):
        if ingredients:
            with st.spinner("🍳 AI is evolving your ingredients..."):
                prompt = f"""
                Create a {style} style {mood} recipe using these ingredients: {ingredients}.
                Return ONLY valid JSON with this structure:
                {{ "name": "Recipe Name", "time": "20 mins", "calories": "300", "spices": ["spice1", "spice2"], "steps": ["step1", "step2"], "fact": "Chef's tip" }}
                """
                result = call_evolution_ai(prompt)
                if result:
                    st.session_state.recipe = result
                    st.rerun()
                else:
                    st.error("The kitchen is busy. Please verify your API key and try again.")

# --- 4. THE DISPLAY ---
if 'recipe' in st.session_state and st.session_state.recipe:
    res = st.session_state.recipe
    with col_out:
        st.markdown(f'<img src="https://loremflickr.com/1200/500/cooked,food" style="width:100%; border-radius:40px; margin-bottom:25px; box-shadow: 0 20px 40px rgba(0,0,0,0.5);">', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="glass-card">
            <div style="margin-bottom: 25px;">
                <span class="stat-pill">⏱ {res['time']}</span>
                <span class="stat-pill">🥗 {res['calories']} KCAL</span>
                <span class="stat-pill">🎭 {style}</span>
            </div>
            <h1 style="font-size: 45px; margin-bottom: 15px;">{res['name']}</h1>
            <hr style="border: 0.1px solid rgba(255,255,255,0.1); margin: 25px 0;">
            <h3 style="color:#FF6B00;">Spice Palette</h3>
            <p style="font-size: 18px; margin-bottom:30px;">{", ".join(res['spices'])}</p>
            <h3 style="color:#FF6B00;">Technique</h3>
            {"".join([f"<p style='font-size:18px; margin-bottom:14px;'><b style='color:#FF6B00;'>{i+1}.</b> {s}</p>" for i, s in enumerate(res['steps'])])}
            <div style="background: rgba(255,107,0,0.1); padding: 20px; border-radius: 20px; margin-top: 35px; border-left: 5px solid #FF6B00;">
                <p style="margin:0; color:#FF6B00; font-weight:bold;">Chef's Secret:</p>
                <p style="margin:0; color:#ccc;">{res['fact']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()