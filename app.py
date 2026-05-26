import streamlit as st
import json
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="CookSwipe Elite", layout="wide")

# Custom CSS to ensure elements are visible and themed correctly
st.markdown("""
<style>
    .glass-card { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px; padding: 40px; color: white; }
    .stat-pill { background: rgba(255, 107, 0, 0.2); color: #FF6B00; padding: 8px 16px; border-radius: 50px; font-weight: bold; margin-right: 10px; }
    .main-title { font-size: 50px; font-weight: 800; color: white; }
</style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'recipe' not in st.session_state: st.session_state.recipe = None

# --- 3. ENGINE ---
def call_evolution_ai(prompt):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key: return {"error": "API Key missing."}
    
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        return {"error": str(e)}

# --- 4. INTERFACE ---
st.markdown("<h1 class='main-title'>CookSwipe <span style='color:#FF6B00;'>Elite</span></h1>", unsafe_allow_html=True)
col_in, col_out = st.columns([1, 1.8], gap="large")

with col_in:
    ingredients = st.text_area("📥 Kitchen Inventory", "Egg, Bread, Cheese", height=100)
    if st.button("✨ GENERATE MASTERPIECE"):
        with st.spinner("AI is evolving..."):
            prompt = f"Create a recipe using: {ingredients}. Return ONLY JSON: {{'name': 'Name', 'time': '20m', 'calories': '300', 'spices': ['s1'], 'steps': ['step1'], 'fact': 'tip'}}"
            res = call_evolution_ai(prompt)
            if 'error' not in res:
                st.session_state.recipe = res
                st.rerun()
            else:
                st.error(f"Error: {res['error']}")

with col_out:
    if st.session_state.recipe:
        res = st.session_state.recipe
        st.markdown(f"""
        <div class="glass-card">
            <h1>{res['name']}</h1>
            <p>⏱ {res['time']} | 🥗 {res['calories']} kcal</p>
            <h3>Technique</h3>
            {''.join([f'<p><b>{i+1}.</b> {s}</p>' for i, s in enumerate(res['steps'])])}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Add ingredients and click generate to start.")