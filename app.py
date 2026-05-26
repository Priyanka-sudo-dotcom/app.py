import google.generativeai as genai
import streamlit as st

# Test the connection
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    models = genai.list_models()
    for m in models:
        st.write(f"Available model: {m.name}")
except Exception as e:
    st.error(f"Connection Test Failed: {e}")
import streamlit as st
import json
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="CookSwipe Evolution", layout="wide")

# --- 2. THE STABLE ENGINE ---
def get_recipe_from_ai(ingredients, style, mood):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("API Key not found in Streamlit Secrets.")
        return None
    
    try:
        genai.configure(api_key=api_key)
        # Using the standard gemini-1.5-flash model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a professional chef. Create a {style} style {mood} recipe using these ingredients: {ingredients}.
        Return the response in JSON format ONLY. Do not include any other text.
        Structure: {{"name": "...", "time": "...", "calories": "...", "spices": ["..."], "steps": ["..."], "fact": "..."}}
        """
        
        response = model.generate_content(prompt)
        # Clean potential markdown wrappers
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        st.error(f"AI Engine Error: {str(e)}")
        return None

# --- 3. UI ---
st.title("🥘 CookSwipe Evolution")

ingredients = st.text_input("Ingredients", "Egg, Bread, Cheese")
style = st.selectbox("Style", ["Desi", "Continental", "Asian Fusion"])
mood = st.selectbox("Mood", ["Healthy", "Lazy", "Fine Dining"])

if st.button("✨ GENERATE RECIPE"):
    with st.spinner("Chef is cooking..."):
        recipe = get_recipe_from_ai(ingredients, style, mood)
        if recipe:
            st.session_state.recipe = recipe
        else:
            st.warning("Failed to generate. Please check your API key and permissions.")

if 'recipe' in st.session_state and st.session_state.recipe:
    r = st.session_state.recipe
    st.subheader(r.get('name', 'Recipe'))
    st.write(f"⏱ {r.get('time', 'N/A')} | 🥗 {r.get('calories', 'N/A')} kcal")
    st.write(f"**Spices:** {', '.join(r.get('spices', []))}")
    st.write("**Instructions:**")
    for i, step in enumerate(r.get('steps', [])):
        st.write(f"{i+1}. {step}")
    st.info(f"💡 Tip: {r.get('fact', 'Enjoy your meal!')}")