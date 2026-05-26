import streamlit as st
import json
import google.generativeai as genai
import requests
import time
from PIL import Image
import io
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie

# --- 1. CONFIGURATION & PREMIUM LUXURY STYLING ---
st.set_page_config(page_title="CookSwipe Elite - AI Gastronomy", page_icon="🥘", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] { background-color: #030303; font-family: 'Plus Jakarta Sans', sans-serif; color: #F3F4F6; }
    .brand-glow { font-size: 52px; font-weight: 800; background: linear-gradient(135deg, #FF5E00 0%, #FF9E00 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .glass-panel { background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 25px; padding: 30px; }
    .stat-pill { background: rgba(255, 94, 0, 0.15); border: 1px solid #FF5E00; color: #FF9E00; padding: 6px 14px; border-radius: 100px; margin: 5px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'view' not in st.session_state: st.session_state.view = "fridge"
if 'fridge_items' not in st.session_state: st.session_state.fridge_items = ["Paneer", "Spinach"]
if 'xp' not in st.session_state: st.session_state.xp = 120
if 'streak' not in st.session_state: st.session_state.streak = 2
if 'calories_consumed' not in st.session_state: st.session_state.calories_consumed = 410

# --- 3. SIDEBAR HUD ---
with st.sidebar:
    st.markdown("### 🏆 Kitchen Mastery")
    st.write(f"✨ {st.session_state.xp} XP | 🔥 {st.session_state.streak}-Day Streak")
    progress_val = min(st.session_state.calories_consumed / 2000, 1.0)
    st.progress(progress_val)
    st.write(f"📊 Calories: {st.session_state.calories_consumed} / 2000 kcal")

# --- 4. MAIN INTERFACE ---
if st.session_state.view == "fridge":
    st.markdown("<h1 class='brand-glow'>CookSwipe Elite</h1>", unsafe_allow_html=True)
    
    # Inventory Management
    st.write("#### 🛒 Current Inventory")
    new_item = st.text_input("Add ingredient:")
    if st.button("Add"): 
        if new_item:
            st.session_state.fridge_items.append(new_item)
            st.rerun()
    
    st.write(", ".join(st.session_state.fridge_items))
    
    # Theme Selectors
    col1, col2 = st.columns(2)
    style = col1.selectbox("Theme", ["Healthy", "Chatpata", "Veg Only"])
    mood = col2.selectbox("Complexity", ["Simple Sauté", "Gourmet Chef"])
    
    if st.button("🚀 IGNITE ENGINE"):
        st.session_state.view = "swipe"
        st.rerun()

elif st.session_state.view == "swipe":
    st.write("## Recipe Deck")
    if st.button("🍳 Start Cooking"):
        st.session_state.view = "cook"
        st.rerun()

elif st.session_state.view == "cook":
    st.write("## Active Cooking")
    duration = st.number_input("Timer (s)", value=15)
    if st.button("Start Timer"):
        status = st.empty()
        for rem in range(duration, -1, -1):
            status.markdown(f"⏳ **{rem} seconds remaining...**")
            time.sleep(1)
        status.success("🔥 Step finished!")
