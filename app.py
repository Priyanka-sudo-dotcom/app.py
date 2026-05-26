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
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key: return None
    genai.configure(api_key=api_key)
    
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
                
            return json.loads(text)
        except:
            continue
    return None

# --- 3. THE INTERFACE ---
if 'recipe' not in st.session_state: st.session_state.recipe = None

st.markdown("<h1 style='font-size: 50px; font-weight: 800;'>CookSwipe <span style='color:#FF6B00;'>Evolution</span></h1>", unsafe_allow_html=True)
col_in, col_out = st.columns([1, 1.8], gap="large")

with col_in:
    ingredients = st.text_area("📥 Kitchen Inventory", "Egg, Bread, Cheese", height=100)
    style = st.select_slider("🎭 Choose Your Style", options=["Desi", "Continental", "Asian Fusion", "Street Style"])
    mood = st.selectbox("🍳 Cooking Mood", ["Lazy (5 mins)", "Healthy", "Cheat Meal", "Fine Dining"])

    if st.button("✨ GENERATE MASTERPIECE"):
        if ingredients:
            with st.spinner("🍳 AI is evolving your ingredients..."):
                prompt = f"""
                Create a {style} style {mood} recipe using these ingredients: {ingredients}.
                Return ONLY a JSON object with this exact structure:
                {{ "name": "Recipe Name", "time": "20 mins", "calories": "300", "spices": ["spice1", "spice2"], "steps": ["step1", "step2"], "fact": "Chef's tip" }}
                """
                result = call_evolution_ai(prompt)
                if result:
                    st.session_state.recipe = result
                    st.rerun()
                else:
                    st.error("The kitchen is busy. Please check your API key or try again!")

with col_out:
    if st.session_state.recipe:
        res = st.session_state.recipe
        st.markdown(f"""
        <div class="glass-card">
            <div style="margin-bottom: 25px;">
                <span class="stat-pill">⏱ {res['time']}</span>
                <span class="stat-pill">🥗 {res['calories']} KCAL</span>
                <span class="stat-pill">🎭 {style}</span>
            </div>
            <h1 style="font-size: 45px; margin-bottom: 15px;">{res['name']}</h1>
            <h3 style="color:#FF6B00;">Spice Palette</h3>
            <p>{", ".join(res['spices'])}</p>
            <h3 style="color:#FF6B00;">Technique</h3>
            {"".join([f"<p><b>{i+1}.</b> {s}</p>" for i, s in enumerate(res['steps'])])}
            <div style="background: rgba(255,107,0,0.1); padding: 20px; border-radius: 20px; margin-top: 20px;">
                <p><b>Chef's Secret:</b> {res['fact']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Your recipe will appear here once generated.")