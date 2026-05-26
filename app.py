import streamlit as st
import json
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="CookSwipe Evolution", layout="wide")
st.markdown("""
<style>
    .glass-card { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px; padding: 40px; }
    .stat-pill { background: rgba(255, 107, 0, 0.2); color: #FF6B00; padding: 8px 16px; border-radius: 50px; font-weight: bold; margin-right: 10px; }
    .hud { background: #111; border-radius: 20px; padding: 20px; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'xp' not in st.session_state: st.session_state.xp = 120
if 'streak' not in st.session_state: st.session_state.streak = 2
if 'cals' not in st.session_state: st.session_state.cals = 410
if 'recipe' not in st.session_state: st.session_state.recipe = None

# --- 3. ENGINE & TOOLS ---
def call_evolution_ai(prompt):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except: return None

def speak_text(text):
    js = f"""<script>var u = new SpeechSynthesisUtterance("{text.replace('"', '')}"); window.speechSynthesis.speak(u);</script>"""
    components.html(js, height=0)

# --- 4. INTERFACE ---
st.markdown("<h1 style='font-size: 50px; font-weight: 800;'>CookSwipe <span style='color:#FF6B00;'>Evolution</span></h1>", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.8], gap="large")

with col_in:
    # Sidebar-style HUD integration
    st.markdown(f"""
    <div class="hud">
        <h4>🏆 Kitchen Mastery</h4>
        <p>✨ {st.session_state.xp} XP | 🔥 {st.session_state.streak} Day Streak</p>
        <p>📊 Calories: {st.session_state.cals}/2000 kcal</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    ingredients = st.text_area("📥 Kitchen Inventory", "Egg, Bread, Cheese", height=100)
    style = st.select_slider("🎭 Style", options=["Desi", "Continental", "Asian Fusion", "Street Style"])
    mood = st.selectbox("🍳 Mood", ["Lazy", "Healthy", "Cheat Meal", "Fine Dining"])

    if st.button("✨ GENERATE MASTERPIECE"):
        prompt = f"Create a {style} style {mood} recipe using: {ingredients}. JSON only: {{'name': '...', 'time': '...', 'calories': '...', 'spices': [], 'steps': [], 'fact': '...'}}"
        with st.spinner("Evolving..."):
            res = call_evolution_ai(prompt)
            if res:
                st.session_state.recipe = res
                st.session_state.xp += 15 # Award XP
                st.rerun()

with col_out:
    if st.session_state.recipe:
        res = st.session_state.recipe
        st.markdown(f"### {res['name']}")
        if st.button("🔊 Narrate Recipe"): speak_text(f"To make {res['name']}, follow these steps: " + ". ".join(res['steps']))
        
        st.markdown(f"""
        <div class="glass-card">
            <span class="stat-pill">⏱ {res['time']}</span> <span class="stat-pill">🥗 {res['calories']} KCAL</span>
            <hr>
            <h4>Technique</h4>
            {''.join([f'<p><b>{i+1}.</b> {s}</p>' for i, s in enumerate(res['steps'])])}
        </div>
        """, unsafe_allow_html=True)