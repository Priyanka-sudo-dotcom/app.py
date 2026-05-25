import streamlit as st

# 1. PAGE SETUP
st.set_page_config(page_title="CookSwipe AI", page_icon="🍳")

# 2. LUXURY DARK THEME CSS
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    .recipe-card {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 25px;
        border: 1px solid #333;
        text-align: center;
        margin-top: 10px;
    }
    .tag {
        background-color: rgba(255, 165, 0, 0.1);
        color: #FFA500;
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 13px;
        display: inline-block;
        border: 1px solid rgba(255, 165, 0, 0.3);
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# 3. THE RECIPE DATABASE (The Brain)
all_recipes = [
    {
        "ingredients": ["rice", "egg"],
        "name": "Golden Egg Fried Rice",
        "time": "10m", "cal": "350",
        "img": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=500",
        "instructions": "Scramble eggs, mix with cooked rice and soy sauce."
    },
    {
        "ingredients": ["bread", "egg"],
        "name": "Cheesy Egg Toast",
        "time": "8m", "cal": "280",
        "img": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=500",
        "instructions": "Toast bread, add fried egg and a slice of cheese."
    },
    {
        "ingredients": ["milk", "banana"],
        "name": "Velvet Banana Smoothie",
        "time": "3m", "cal": "200",
        "img": "https://images.unsplash.com/photo-1553334820-13d8932c45ee?w=500",
        "instructions": "Blend banana and milk until smooth."
    },
    {
        "ingredients": ["chicken", "rice"],
        "name": "Seared Chicken & Rice",
        "time": "20m", "cal": "450",
        "img": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=500",
        "instructions": "Pan-fry chicken and serve over fluffy steamed rice."
    }
]

# 4. APP INTERFACE
st.title("CookSwipe AI 🍳")
st.write("### 👨‍🍳 What's in your fridge?")

# Ingredient Selection
user_ingredients = st.multiselect(
    "Select ingredients you have:",
    ["rice", "egg", "bread", "milk", "banana", "chicken", "onion"],
    default=["rice", "egg"]
)

# 5. FILTERING LOGIC (Find matches)
found_recipes = []
for r in all_recipes:
    # Check if all required ingredients for the recipe are in the user's list
    if all(item in user_ingredients for item in r['ingredients']):
        found_recipes.append(r)

# 6. DISPLAY RESULTS AS SWIPE CARDS
if found_recipes:
    if 'swipe_idx' not in st.session_state:
        st.session_state.swipe_idx = 0
    
    # Handle the index in case user changes ingredients
    current_idx = st.session_state.swipe_idx % len(found_recipes)
    recipe = found_recipes[current_idx]

    # Show the card
    st.image(recipe['img'], use_container_width=True)
    st.markdown(f"""
    <div class="recipe-card">
        <div class="tag">⏱ {recipe['time']}</div>
        <div class="tag">🔥 {recipe['cal']} kcal</div>
        <h2 style="color:white; margin-bottom:10px;">{recipe['name']}</h2>
        <p style="color:#bbb; font-style:italic;">{recipe['instructions']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Swipe Buttons
    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("❌ Next", use_container_width=True):
            st.session_state.swipe_idx += 1
            st.rerun()
    with c2:
        if st.button("🍳 Cook", type="primary", use_container_width=True):
            st.balloons()
    with c3:
        if st.button("❤️ Save", use_container_width=True):
            st.toast(f"Saved {recipe['name']}!")
            st.session_state.swipe_idx += 1
            st.rerun()
else:
    st.warning("👨‍🍳 No recipes found for those ingredients. Try adding more items!")
