import streamlit as st
import requests
import json

# Mobile Viewport & Screen Setup
st.set_page_config(page_title="AI Master App", page_icon="🤖", layout="centered")

# Screen Scaling CSS taaki mobile par sab bada aur saaf dikhe
st.markdown("""
<style>
    .stApp {
        background-color: #0e0e12;
        color: #FFFFFF;
    }
    .stSelectbox, .stTextArea, .stButton {
        margin-bottom: 14px;
    }
    div[data-baseweb="select"] {
        border-radius: 12px !important;
        background-color: #1a1a24 !important;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563EB;
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        border-radius: 12px;
        padding: 0.8rem;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 All-In-One AI Master")

# Aapki bilkul nayi AQ key
API_KEY = "AQ.Ab8RN6KhaojI0Q2YVKIMkiNKOuYBDVa6c5N07YUUtmaq3iFXJg"

# Screen par saare features samne wapas aa gaye hain
feature = st.selectbox(
    "Aapko kya karwana hai?",
    [
        "💬 Normal Kuch Bhi Puchna / Chat Karna",
        "📖 Kahani / Story Likhwana (Horror, Romance, Suspense)",
        "💰 Online Earning / Paise Kamane Ke Tarike",
        "🎓 Student Padhai / Homework / Maths / Science",
        "📱 Viral Social Media Script (Reels / Shorts)"
    ]
)

user_input = st.text_area("Aapka sawal, topic ya kahani ka idea yahan likhein:", height=110)

if st.button("Generate Karein 🔥"):
    if not user_input.strip():
        st.warning("Pehle apna topic ya sawal likhein!")
    else:
        with st.spinner("AI likh raha hai..."):
            prompt = f"Role: {feature}\nRequest: {user_input}\nDetailed helpful response dein (Hinglish/Hindi ya English jaise pucha gaya ho)."
            
            # Direct Native Google API Call (Supports new AQ. keys without 401 bug)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={API_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            try:
                res = requests.post(url, headers=headers, json=payload)
                data = res.json()
                
                if res.status_code == 200:
                    ans = data["candidates"][0]["content"]["parts"][0]["text"]
                    st.success("Ye raha aapka content:")
                    st.markdown(ans)
                else:
                    st.error(f"Google API Response ({res.status_code}): {data.get('error', {}).get('message', res.text)}")
            except Exception as e:
                st.error(f"Request Error: {e}")
                
