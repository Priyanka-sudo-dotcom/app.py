import streamlit as st
import google.generativeai as genai
import json
import requests

# --- LUXURY STYLING ---
st.set_page_config(page_title="CookSwipe Elite", page_icon="🥘", layout="wide")

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505; color: #E0E0E0; }
    .recipe-card { background: #111; border: 1px solid #222; border-radius: 30px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .stButton>button { background: linear-gradient(90deg, #FF6B00, #FF4500) !important; color: white !important; border-radius: 15px !important; }
</style>
""", unsafe_allow_html=True)

# --- AI SETUP ---
try:
    # This checks if your Secret Key is actually there
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"⚠️ Connection Error: {e}")

# --- UI ---
st.title("CookSwipe Elite 🍳")
ingredients = st.text_input("What ingredients do you have?", "Chicken, Rice, Onion")

if st.button("✨ DESIGN RECIPE"):
    if ingredients:
        with st.spinner("👨‍🍳 Chef is thinking..."):
            # Stronger prompt to prevent AI from "talking" too much
            prompt = f"Create a recipe using {ingredients}. Return ONLY JSON: {{\"name\":\"\",\"time\":\"\",\"calories\":\"\",\"spices\":[],\"steps\":[]}}"
            
            try:
                response = model.generate_content(prompt)
                
                # CLEANING THE RESPONSE
                clean_text = response.text.replace('```json', '').replace('```', '').strip()
                data = json.loads(clean_text)
                
                # DISPLAY
                st.image(f"https://source.unsplash.com/800x400/?cooking,{data['name'].replace(' ', ',')}")
                st.markdown(f"""
                <div class="recipe-card">
                    <h1>{data['name']}</h1>
                    <p>⏱ {data['time']} | 🔥 {data['calories']} kcal</p>
                    <hr>
                    <h3>Spices:</h3> {", ".join(data['spices'])}
                    <h3>Steps:</h3>
                    {"".join([f"<p>{i+1}. {s}</p>" for i, s in enumerate(data['steps'])])}
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
                
            except Exception as e:
                # This will tell us the REAL error now
                st.error(f"Chef Error: {e}")
                st.write("Full AI Response for debugging:", response.text if 'response' in locals() else "No response")
