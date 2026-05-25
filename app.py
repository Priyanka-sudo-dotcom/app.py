import streamlit as st

# 1. BASIC SETTINGS
st.set_page_config(page_title="CookSwipe AI", page_icon="🍳")

# 2. THE DESIGN (CSS) - Fixed the spelling error here!
st.markdown("""
<style>
    .stApp {
        background-color: #000000;
        color: white;
    }
    .recipe-card {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #333;
        text-align: center;
    }
    .tag {
        background-color: #333;
        color: #FFA500;
        padding: 5px 10px;
        border-radius: 10px;
        margin: 5px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# 3. THE CONTENT
st.title("CookSwipe 🍳")

recipes = [
    {"name": "Paneer Tikka Wrap", "time": "10m", "cal": "320", "img": "https://images.unsplash.com/photo-1544025162-d76694265947?w=400"},
    {"name": "Cheesy Egg Toast", "time": "8m", "cal": "280", "img": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=400"}
]

if 'count' not in st.session_state:
    st.session_state.count = 0

item = recipes[st.session_state.count % len(recipes)]

# 4. SHOW THE CARD - Fixed spelling here too!
st.image(item['img'], use_container_width=True)
st.markdown(f"""
<div class="recipe-card">
    <div class="tag">⏱ {item['time']}</div>
    <div class="tag">🔥 {item['cal']} kcal</div>
    <h2 style="color:white;">{item['name']}</h2>
</div>
""", unsafe_allow_html=True)

# 5. BUTTONS
st.write("")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("❌ Skip"):
        st.session_state.count += 1
        st.rerun()
with c2:
    if st.button("🍳 Cook", type="primary"):
        st.balloons()
with c3:
    if st.button("❤️ Save"):
        st.toast("Saved!")
        st.session_state.count += 1
        st.rerun()
