
import streamlit as st
import json
import google.generativeai as genai
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="CookSwipe Elite", layout="wide")
st.markdown("""
<style>
    .brand-glow { font-size: 52px; font-weight: 800; background: linear-gradient(135deg, #FF5E00 0%, #FF9E00 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .glass-panel { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 25px; padding: 30px; }
</style>
""", unsafe_allow_html=True)

# --- 2. AI ENGINE ---
def call_evolution_ai(prompt):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key: return None
    genai.configure(api_key=api_key)
    
    # Cascade through models
    for model_name in ["gemini-1.5-flash", "gemini-1.5-pro"]:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            res_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(res_text)
        except:
            continue
    return None

# --- 3. SESSION STATE ---
if 'recipe' not in st.session_state: st.session_state.recipe = None

# --- 4. INTERFACE ---
st.markdown("<h1 class='brand-glow'>CookSwipe Evolution</h1>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1.5])

with col1:
    ingredients = st.text_area("What's in your fridge?", "Paneer, Spinach, Garlic")
    style = st.selectbox("Style", ["Desi", "Continental", "Asian Fusion"])
    mood = st.selectbox("Mood", ["Healthy", "Cheat Meal", "Fine Dining"])
    
    if st.button("✨ GENERATE RECIPE"):
        prompt = f"""
        Create a {style} style {mood} recipe using: {ingredients}.
        Return ONLY valid JSON:
        {{ "name": "Recipe Name", "time": "20 mins", "calories": "300", "spices": ["list", "of", "spices"], "steps": ["step 1", "step 2"], "fact": "Chef's tip" }}
        """
        with st.spinner("Evolving ingredients..."):
            st.session_state.recipe = call_evolution_ai(prompt)

with col2:
    if st.session_state.recipe:
        res = st.session_state.recipe
        st.subheader(res['name'])
        st.write(f"⏱ {res['time']} | 🥗 {res['calories']} kcal")
        st.write(f"**Spices:** {', '.join(res['spices'])}")
        st.write("**Instructions:**")
        for i, step in enumerate(res['steps']):
            st.write(f"{i+1}. {step}")
        st.info(f"💡 Chef's Secret: {res['fact']}")
    else:
        st.info("Your recipe will appear here once generated.")