import streamlit as st

st.title("🥗 AI Recipe & Calorie Bot")

st.write("Enter ingredients you have (comma separated). Example: rice, egg, onion")

# Simple recipe + calorie database (inside one file)
recipes = {
    "rice,egg": {
        "recipe": "Make egg fried rice: cook rice, scramble egg, add onion, mix together.",
        "calories": 350
    },
    "bread,egg": {
        "recipe": "Make egg sandwich: toast bread, add fried egg in between.",
        "calories": 280
    },
    "oats,milk": {
        "recipe": "Cook oats in milk, add honey or fruits if available.",
        "calories": 220
    },
    "chicken,rice": {
        "recipe": "Cook chicken with spices and serve with boiled rice.",
        "calories": 450
    },
    "banana,milk": {
        "recipe": "Blend banana with milk to make a healthy smoothie.",
        "calories": 200
    }
}

ingredients = st.text_input("Enter your ingredients")

if ingredients:
    user_items = sorted([i.strip().lower() for i in ingredients.split(",")])

    found = False

    for key in recipes:
        key_items = sorted(key.split(","))

        # check if user has at least required ingredients
        if all(item in user_items for item in key_items):
            st.success("🍽️ Recipe Found!")

            st.write("### Recipe:")
            st.write(recipes[key]["recipe"])

            st.write("### Calories:")
            st.info(f"{recipes[key]['calories']} kcal (approx)")

            found = True
            break

    if not found:
        st.warning("No exact recipe found. Try adding more common ingredients like rice, egg, bread, milk.")
