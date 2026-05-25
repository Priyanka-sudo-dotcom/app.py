import streamlit as st

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="CookSwipe AI", page_icon="🍳", layout="centered")

# 2. LUXURY CSS (Turning Streamlit into a Mobile App Look)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    
    /* The Recipe Card Container */
    .recipe-card {
        background-color: #111;
        border-radius: 30px;
        border: 1px solid #333;
        overflow: hidden;
        margin-top: 20px;
        position: relative;
    }
    
    /* Image Styling */
    .recipe-img {
        width: 100%;
        height: 350px;
        object-fit: cover;
    }
    
    /* Floating Tags */
    .tag {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        margin-right: 5px;
    }
    
    /* Action Buttons */
    .action-btn {
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    </style>
""", unsafe_allowed_html=True)

# 3. TOP NAVIGATION
col_title, col_status = st.columns([2, 1])
with col_title:
    st.markdown("<h1 style='margin-bottom:0;'>CookSwipe 🍳</h1>", unsafe_allowed_html=True)
    st.markdown("<p style='color:gray;'>Swipe recipes you want to cook</p>", unsafe_allowed_html=True)
with col_status:
    st.markdown("<br><div style='background:rgba(255,165,0,0.2); color:#FFA500; padding:5px 15px; border-radius:20px; border:1px solid orange; text-align:center;'>AI Recipes</div>", unsafe_allowed_html=True)

# 4. RECIPE DATA (Using your React Data)
recipes = [
    {
        "title": "Paneer Tikka Wrap",
        "time": "10 mins",
        "calories": "320 kcal",
        "image": "https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=1200&auto=format&fit=crop"
    },
    {
        "title": "Cheesy Egg Toast",
        "time": "8 mins",
        "calories": "280 kcal",
        "image": "https://images.unsplash.com/photo-1525351484163-7529414344d8?q=80&w=1200&auto=format&fit=crop"
    },
    {
        "title": "Veg Fried Rice",
        "time": "15 mins",
        "calories": "410 kcal",
        "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19?q=80&w=1200&auto=format&fit=crop"
    }
]

# 5. CARD SWIPE DISPLAY
# We use a 'session state' to keep track of which recipe is showing (index)
if 'recipe_index' not in st.session_state:
    st.session_state.recipe_index = 0

current_idx = st.session_state.recipe_index % len(recipes)
r = recipes[current_idx]

# Displaying the Card
st.markdown(f"""
    <div class="recipe-card">
        <img src="{r['image']}" class="recipe-img">
        <div style="padding: 20px;">
            <span class="tag">⏱ {r['time']}</span>
            <span class="tag">🔥 {r['calories']}</span>
            <h2 style="margin-top:15px; font-size:32px;">{r['title']}</h2>
            <p style="color:#aaa;">AI generated quick recipe based on your ingredients.</p>
        </div>
    </div>
""", unsafe_allowed_html=True)

# 6. INTERACTIVE BUTTONS
st.write("")
btn_col1, btn_col2, btn_col3 = st.columns([1,1,1])

with btn_col1:
    if st.button("❌", use_container_width=True):
        st.session_state.recipe_index += 1
        st.rerun()

with btn_col2:
    if st.button("🍳 Cook", type="primary", use_container_width=True):
        st.confetti()
        st.success(f"Starting {r['title']} recipe!")

with btn_col3:
    if st.button("❤️", use_container_width=True):
        st.toast(f"Saved {r['title']} to favorites!")
        st.session_state.recipe_index += 1
        st.rerun()

# 7. BOTTOM QUICK CATEGORIES
st.write("---")
cat_col1, cat_col2, cat_col3 = st.columns(3)
cat_col1.button("⚡ 10 mins", use_container_width=True)
cat_col2.button("🥗 Healthy", use_container_width=True)
cat_col3.button("🍗 Non-Veg", use_container_width=True)
