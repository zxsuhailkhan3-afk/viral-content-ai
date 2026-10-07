import streamlit as st
import requests
import json
from datetime import datetime

# Mobile Native App Configuration
st.set_page_config(
    page_title="Gemini",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# EXACT GEMINI / CHATGPT MOBILE APP UI
st.markdown("""
<style>
    /* Full Phone Fit - No Desktop Zoom */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0e0e11 !important;
        color: #E3E3E8 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* Container padding removal for real mobile app experience */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 7rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 100% !important;
    }

    /* Top Bar */
    .gemini-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 6px 4px 14px 4px;
        border-bottom: 1px solid #1c1c24;
        margin-bottom: 12px;
    }
    .header-pill {
        background-color: #1a1a24;
        color: #70A1FF;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 600;
        border: 1px solid #2a2a3a;
    }

    /* Chat Messages */
    .stChatMessage {
        background-color: transparent !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        padding: 8px 0px !important;
    }

    /* Side Drawer */
    section[data-testid="stSidebar"] {
        background-color: #121218 !important;
        border-right: 1px solid #22222e !important;
    }

    /* Floating Rounded Gemini Bottom Input Bar */
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 15px !important;
        left: 4% !important;
        right: 4% !important;
        width: 92% !important;
        border-radius: 30px !important;
        background-color: #1e1e28 !important;
        border: 1px solid #36364a !important;
        padding: 4px 12px !important;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.8) !important;
        z-index: 99999 !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Aapki Verified AQ Key
API_KEY = "AQ.Ab8RN6KhaojI0Q2YVKIMkiNKOuYBDVa6c5N07YUUtmaq3iFXJg"

# Multi-Chat History Sessions
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"Main Chat": []}
if "active_chat" not in st.session_state:
    st.session_state.active_chat = "Main Chat"
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "💬 General AI (Sab Kuch Pucho)"

# --- SIDEBAR DRAWER (Photo 3 Gemini Style) ---
with st.sidebar:
    st.markdown("## ✨ Gemini AI")
    if st.button("➕ New chat", use_container_width=True):
        new_name = f"Chat {datetime.now().strftime('%H:%M')}"
        st.session_state.chat_sessions[new_name] = []
        st.session_state.active_chat = new_name
        st.rerun()

    st.markdown("---")
    st.markdown("### 🧭 Studios & Features")
    st.session_state.app_mode = st.radio(
        "Mode Chunein:",
        [
            "💬 General AI (Sab Kuch Pucho)",
            "🎓 Students Help (Padhai & Code)",
            "💰 Online Earning & Business Master",
            "📖 Story Writer (Kahaniyan)",
            "📱 Viral Social Media (Reels & Shorts)"
        ]
    )

    st.markdown("---")
    st.markdown("### 🕒 Recent Chats")
    for chat_title in list(reversed(list(st.session_state.chat_sessions.keys())))[:6]:
        if st.button(f"🗨️ {chat_title}", key=f"rec_{chat_title}", use_container_width=True):
            st.session_state.active_chat = chat_title
            st.rerun()

    st.markdown("---")
    if st.button("🗑️ Clear This Chat", use_container_width=True):
        st.session_state.chat_sessions[st.session_state.active_chat] = []
        st.rerun()

# --- TOP STATUS BAR ---
current_mode_title = st.session_state.app_mode.split("(")[0].strip()
st.markdown(f"""
<div class="gemini-header">
    <div style="font-size: 1.25rem;">☰</div>
    <div class="header-pill">✨ {current_mode_title}</div>
    <div style="font-size: 1.25rem;">⋮</div>
</div>
""", unsafe_allow_html=True)

# Active chat message render
active_msgs = st.session_state.chat_sessions[st.session_state.active_chat]

if len(active_msgs) == 0:
    st.markdown("""
    <div style="text-align: center; margin-top: 20vh; color: #8F8FA0;">
        <h2 style="color: #FFFFFF; font-size: 2rem; margin-bottom: 6px;">Gemini</h2>
        <p style="font-size: 1rem;">Ask anything, padhai, kamayi ya kahani...</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for m in active_msgs:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# Bottom Floating Input Box
user_prompt = st.chat_input("Ask Gemini / Kuch bhi pucho...")

if user_prompt:
    active_msgs.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Gemini is answering..."):
            prompt_payload = f"Mode: {st.session_state.app_mode}\nUser Query: {user_prompt}\nGive clear, direct, and well-explained response in Hinglish/Hindi or English."
            
            # Universal Multi-Model Fallback Engine for AQ. keys
            models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-pro","gemini-3.8-flash"]
            reply_found = False
            last_err = ""

            for mod in models_to_try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{mod}:generateContent?key={API_KEY}"
                headers = {
                    "Content-Type": "application/json",
                    "x-goog-api-key": API_KEY
                }
                body = {
                    "contents": [{
                        "parts": [{"text": prompt_payload}]
                    }]
                }

                try:
                    res = requests.post(url, headers=headers, json=body, timeout=25)
                    if res.status_code == 200:
                        data = res.json()
                        reply_text = data["candidates"][0]["content"]["parts"][0]["text"]
                        st.markdown(reply_text)
                        active_msgs.append({"role": "assistant", "content": reply_text})
                        reply_found = True
                        break
                    else:
                        last_err = res.text
                except Exception as ex:
                    last_err = str(ex)

            if not reply_found:
                err_msg = f"API Issue: {last_err}"
                st.error(err_msg)
                active_msgs.append({"role": "assistant", "content": err_msg})
