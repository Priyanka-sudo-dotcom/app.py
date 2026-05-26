import streamlit as st
import json
import google.generativeai as genai

# ... (keep existing configuration and session state)

# --- 3. ENGINE (FIXED) ---
def call_evolution_ai(prompt):
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key: return "ERROR: No API Key found."
        genai.configure(api_key=api_key)
        
        # Use the most stable, universally available model identifier
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        # Fallback to the Pro version if Flash is restricted in your project
        try:
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(prompt)
            text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception as e2:
            return f"DEBUG_ERROR: {str(e2)}"

# ... (keep existing interface and display logic)