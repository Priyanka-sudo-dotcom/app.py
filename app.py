import streamlit as st
import time

# 1. PAGE CONFIG & LUXURY STYLING
st.set_page_config(page_title="CookSwipe Ultimate", page_icon="👨‍🍳", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    .recipe-card {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 30px;
        border: 1px solid #333;
        text-align: center;
    }
    .tag {
        background: rgba(255, 165, 0, 0.1);
        color: #FFA500;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 11px;
        border: 1px solid orange;
        margin: 2px;
        display: inline-block;
    }
    .step-box {
        background: #262626;
        padding: 15px;
        border-left: 5px solid #FF6600;
        border-radius: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 2. THE MASTER DATABASE
all_recipes = [
    {
        "name": "Paneer Tikka Wrap",
        "ingredients": ["paneer", "bread", "onion"],
        "spices": ["Garam Masala", "Chilli Powder", "Salt"],
        "time": 10, "cal": 320, "type": "Veg", "mood": "Chatpata", "diff": "Easy",
        "img": "https://images.unsplash.com/photo-1544025162-d76694265947?w=500",
        "steps": ["Slice paneer and sauté with spices.", "Toast the bread.", "Wrap and serve hot."]
    },
    {
        "name": "Spicy Chicken Rice",
        "ingredients": ["chicken", "rice", "onion"],
        "spices": ["Biryani Masala", "Turmeric", "Pepper"],
        "time": 20, "cal": 450, "type": "Non-Veg", "mood": "Healthy", "diff": "Medium",
        "img": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=500",
        "steps": ["Cook chicken with spices until tender.", "Boil rice separately.", "Mix together and steam for 2 mins."]
    },
    {
        "name": "Cheesy Egg Bread",
        "ingredients": ["egg", "bread"],
        "spices": ["Oregano", "Chilli Flakes"],
        "time": 5, "cal": 280, "type": "Non-Veg", "mood": "Lazy", "diff": "Easy",
        "img": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=500",
        "steps": ["Toast bread on one side.", "Crack egg on top and cover with lid.", "Add cheese and spices."]
    }
]

# 3. SESSION STATE (The App's Memory)
if 'view' not in st.session_state: st.session_state.view = "swipe"
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'calories_today' not in st.session_state: st.session_state.calories_today = 0

# 4. HEADER & FILTERS
st.title("CookSwipe Ultimate 🍳")

# Progress Bar for Health Goal
st.write(f"🔥 Daily Calories: {st.session_state.calories_today} / 2000 kcal")
st.progress(min(st.session_state.calories_today / 2000, 1.0))

col_a, col_b = st.columns(2)
with col_a:
    ing_search = st.multiselect("What's in the fridge?", ["rice", "egg", "paneer", "chicken", "bread", "onion", "milk"], default=["egg", "bread"])
with col_b:
    mood_filter = st.selectbox("Current Mood?", ["All", "Chatpata", "Healthy", "Lazy"])

# Filter Logic
found = [r for r in all_recipes if any(i in ing_search for i in r['ingredients'])]
if mood_filter != "All":
    found = [r for r in found if r['mood'] == mood_filter]

# 5. UI LOGIC
if not found:
    st.warning("No recipes match your ingredients/mood. Try selecting more!")
else:
    recipe = found[st.session_state.idx % len(found)]

    if st.session_state.view == "swipe":
        # --- SWIPE VIEW ---
        st.image(recipe['img'], use_container_width=True)
        
        # Calculate Match %
        match_pc = int((len(set(ing_search) & set(recipe['ingredients'])) / len(recipe['ingredients'])) * 100)
        
        st.markdown(f"""
        <div class="recipe-card">
            <span class="tag">{recipe['type']}</span>
            <span class="tag">{recipe['mood']}</span>
            <span class="tag">💪 {recipe['diff']}</span>
            <h2>{recipe['name']}</h2>
            <p>⏱ {recipe['time']} mins | 🔥 {recipe['cal']} kcal | 🎯 {match_pc}% Match</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("❌ Next"): 
                st.session_state.idx += 1
                st.rerun()
        with c2:
            if st.button("🍳 Cook Now", type="primary"): 
                st.session_state.view = "cook"
                st.rerun()
        with c3:
            if st.button("❤️ Save"): 
                st.toast("Saved to Favorites!")

    elif st.session_state.view == "cook":
        # --- COOKING MODE ---
        if st.button("⬅️ Back"):
            st.session_state.view = "swipe"
            st.rerun()
            
        st.header(f"Cooking {recipe['name']}")
        
        # Substitutes Feature
        if st.button("🔄 Missing something?"):
            st.info("💡 No Paneer? Use Tofu. No Bread? Use a Roti/Tortilla.")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🛒 Ingredients")
            for i in recipe['ingredients']: st.write(f"- {i}")
        with col2:
            st.subheader("🌶️ Spices")
            for s in recipe['spices']: st.write(f"- {s}")

        st.write("---")
        # Step-by-Step with Timer
        st.subheader("📖 Steps")
        for step in recipe['steps']:
            st.markdown(f"<div class='step-box'>{step}</div>", unsafe_allow_html=True)
            
        if st.button("⏱ Start 1-Min Prep Timer"):
            ph = st.empty()
            for secs in range(60, 0, -1):
                ph.metric("Timer", f"{secs}s")
                time.sleep(1)
            st.success("Timer Done!")

        if st.button("✅ Finished Cooking!"):
            st.balloons()
            st.session_state.calories_today += recipe['cal']
            st.session_state.view = "swipe"
            st.rerun()
