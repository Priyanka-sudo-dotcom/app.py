import streamlit as st
import json
import google.generativeai as genai
import traceback

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="CookSwipe Evolution", layout="wide")
st.markdown("""
<style>
    .glass-card { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px; padding: 40px; }
    .stat-pill { background: rgba(255, 107, 0, 0.2); color: #FF6B00; padding: 8px 16px; border-radius: 50px; font-weight: bold; margin-right: 10px; }
    .hud { background: #111; border-radius: 20px; padding: 20px; border: 1px solid #333; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'xp' not in st.session_state: st.session_state.xp = 120
if 'streak' not in st.session_state: st.session_state.streak = 2
if 'cals' not in st.session_state: st.session_state.cals = 410
if 'recipe' not in st.session_state: st.session_state.recipe = None

# --- 3. ENGINE ---
def call_evolution_ai(prompt):
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key: return "ERROR: No API Key found."
        genai.configure(api_key=api_key)
        # Using the standard latest flash model identifier
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        return f"DEBUG_ERROR: {str(e)}"

# --- 4. INTERFACE ---
st.markdown("<h1 style='font-size: 50px; font-weight: 800;'>CookSwipe <span style='color:#FF6B00;'>Evolution</span></h1>", unsafe_allow_html=True)
col_in, col_out = st.columns([1, 1.8], gap="large")

with col_in:
    st.markdown(f"""
    <div class="hud">
        <h4>🏆 Kitchen Mastery</h4>
        <p>✨ {st.session_state.xp} XP | 🔥 {st.session_state.streak} Day Streak</p>
        <p>📊 Calories: {st.session_state.cals}/2000 kcal</p>
    </div>
    """, unsafe_allow_html=True)
    
    ingredients = st.text_area("📥 Kitchen Inventory", "Egg, Bread, Cheese", height=100)
    style = st.select_slider("🎭 Style", options=["Desi", "Continental", "Asian Fusion", "Street Style"])
    mood = st.selectbox("🍳 Mood", ["Lazy", "Healthy", "Cheat Meal", "Fine Dining"])

    if st.button("✨ GENERATE MASTERPIECE"):
        with st.spinner("🍳 AI is evolving..."):
            prompt = f"Create a {style} style {mood} recipe using: {ingredients}. Return ONLY valid JSON: {{'name': 'Name', 'time': '20m', 'calories': '300', 'spices': ['s1'], 'steps': ['step1'], 'fact': 'tip'}}"
            res = call_evolution_ai(prompt)
            
            if isinstance(res, dict):
                st.session_state.recipe = res
                st.session_state.xp += 15
                st.rerun()
            else:
                st.error(f"Generation Failed: {res}")

with col_out:
    if st.session_state.recipe:
        res = st.session_state.recipe
        st.subheader(res.get('name', 'Recipe'))
        st.markdown(f"""
        <div class="glass-card">
            <span class="stat-pill">⏱ {res.get('time', 'N/A')}</span> 
            <span class="stat-pill">🥗 {res.get('calories', 'N/A')} KCAL</span>
            <hr>
            <h4>Technique</h4>
            {''.join([f'<p><b>{i+1}.</b> {s}</p>' for i, s in enumerate(res.get('steps', []))])}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Your masterpiece will appear here once evolved.")