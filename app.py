import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Gemini",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# BUG FIXED: Hata diya faaltu position:fixed wala code jo input box gayab kar raha tha
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0d0d12 !important;
        color: #F3F4F6 !important;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    div[data-testid="stChatInput"] {
        border-radius: 20px !important;
        background-color: #1a1a26 !important;
        border: 1px solid #4338ca !important;
    }
    .stButton>button {
        background-color: #1a1a24 !important;
        color: #E2E8F0 !important;
        border: 1px solid #2d2d42 !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", "")

if "auth_status" not in st.session_state:
    st.session_state.auth_status = "login"
if "user_name" not in st.session_state:
    st.session_state.user_name = "User"
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {"Current Chat": []}
if "active_chat" not in st.session_state:
    st.session_state.active_chat = "Current Chat"

def call_openrouter(prompt_text):
    if not OPENROUTER_API_KEY:
        return "Secret Key Missing! Manage App > Settings > Secrets mein OPENROUTER_API_KEY save karein."
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.io"
    }
    payload = {
        "model": "openrouter/free",
        "messages": [{"role": "user", "content": prompt_text}]
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=40)
        data = res.json()
        if res.status_code == 200:
            return data["choices"][0]["message"]["content"]
        return f"Error ({res.status_code}): {data.get('error', {}).get('message', res.text)}"
    except Exception as e:
        return f"Network Error: {e}"

# --- APP FLOW ---

if st.session_state.auth_status == "login":
    st.markdown('<h2 style="text-align: center; margin-top: 10vh;">✨ Gemini Login</h2>', unsafe_allow_html=True)
    if st.button("🌐 Continue as Google User", use_container_width=True):
        st.session_state.user_name = "Google User"
        st.session_state.auth_status = "app"
        st.rerun()

elif st.session_state.auth_status == "app":
    # Sidebar
    with st.sidebar:
        st.markdown("## ✨ Gemini AI")
        if st.button("➕ New Chat", use_container_width=True):
            new_title = f"Chat {datetime.now().strftime('%H:%M')}"
            st.session_state.all_chats[new_title] = []
            st.session_state.active_chat = new_title
            st.rerun()
        if st.button("🔄 Logout", use_container_width=True):
            st.session_state.auth_status = "login"
            st.rerun()

    current_chat = st.session_state.all_chats[st.session_state.active_chat]

    if len(current_chat) == 0:
        st.markdown(f'<h3 style="text-align:center;">Hello, {st.session_state.user_name}!</h3>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎓 Study Tutor"):
                current_chat.append({"role": "user", "content": "Mujhe ek student study tutor ki tarah guide karo."})
                st.rerun()
        with col2:
            if st.button("📱 Viral Hooks"):
                current_chat.append({"role": "user", "content": "Instagram reels ke liye 3 viral hooks batao."})
                st.rerun()

    # Pehle saare purane message dikhao
    for msg in current_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Phir API call karo agar aakhri message user ka hai aur assistant ka jawab baaki hai
    if len(current_chat) > 0 and current_chat[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Generating answer..."):
                reply = call_openrouter(current_chat[-1]["content"])
                st.markdown(reply)
                current_chat.append({"role": "assistant", "content": reply})

    # ALWAYS VISIBLE INPUT BOX
    user_query = st.chat_input("Ask Gemini...")
    if user_query:
        current_chat.append({"role": "user", "content": user_query})
        st.rerun()
