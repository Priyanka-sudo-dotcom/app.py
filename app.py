import streamlit as st
import json
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="CookSwipe Evolution", layout="wide")

# --- 2. THE STABLE ENGINE ---
def get_recipe_from_ai(ingredients, style, mood):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key: return None
    
    genai.configure(api_key=api_key)
    # Using gemini-1.0-pro as it is the most stable and widely supported model
    model = genai.GenerativeModel('gemini-1.0-pro')
    
    prompt = f"""
    Act as a professional chef. Create a {style} style {mood} recipe using these ingredients: {ingredients}.
    Return the response in JSON format only with these keys: 
    "name", "time", "calories", "spices", "steps", "fact".
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        st.error(f"AI Engine Error: {e}")
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
            st.warning("Failed to generate. Please check your API key.")

if 'recipe' in st.session_state and st.session_state.recipe:
    r = st.session_state.recipe
    st.subheader(r['name'])
    st.write(f"⏱ {r['time']} | 🥗 {r['calories']} kcal")
    st.write(f"**Spices:** {', '.join(r['spices'])}")
    st.write("**Instructions:**")
    for i, step in enumerate(r['steps']):
        st.write(f"{i+1}. {step}")
    st.info(f"💡 Tip: {r['fact']}")