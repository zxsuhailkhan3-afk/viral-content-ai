import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="Gemini",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0d0d12 !important;
        color: #F3F4F6 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 7.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 1.5rem;
        margin-bottom: 1.2rem;
    }
    .neon-orb-logo {
        width: 100px;
        height: 100px;
        border-radius: 32px;
        background: radial-gradient(circle at 30% 30%, #38bdf8, #2563eb, #1e1b4b);
        box-shadow: 0 15px 35px rgba(37, 99, 235, 0.45);
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 2.8rem;
    }
    .center-ai-orb {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        margin: 1.2rem auto;
        background: radial-gradient(circle at 35% 35%, #a855f7, #6366f1, #3b82f6);
        box-shadow: 0 0 45px rgba(168, 85, 247, 0.55);
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 2.2rem;
    }
    .stButton>button {
        background-color: #1a1a24 !important;
        color: #E2E8F0 !important;
        border: 1px solid #2d2d42 !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        padding: 0.6rem !important;
    }
    .stButton>button:hover {
        border-color: #6366f1 !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stChatInput"] {
        border-radius: 30px !important;
        background-color: #1a1a26 !important;
        border: 1px solid #323248 !important;
        padding: 4px 10px !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.8) !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #111118 !important;
        border-right: 1px solid #222232 !important;
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
if "is_pinned" not in st.session_state:
    st.session_state.is_pinned = False
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "Auto Free AI (Sabse Fast & Active)"

MODEL_MAP = {
    "Auto Free AI (Sabse Fast & Active)": "openrouter/free",
    "Smart Free Model": "openrouter/free"
}

def call_openrouter(prompt_text, chosen_model_name):
    if not OPENROUTER_API_KEY:
        return "Secret Key Missing: Streamlit Secrets me OPENROUTER_API_KEY check karein."
        
    model_id = MODEL_MAP.get(chosen_model_name, "openrouter/free")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.io",
        "X-Title": "ViralContentAI"
    }
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": "You are a professional AI assistant. Give structured, helpful responses."},
            {"role": "user", "content": prompt_text}
        ]
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=40)
        data = res.json()
        if res.status_code == 200:
            return data["choices"][0]["message"]["content"]
        return f"Error ({res.status_code}): {data.get('error', {}).get('message', res.text)}"
    except Exception as e:
        return f"Network Error: {e}"

# SCREEN 1: LOGIN
if st.session_state.auth_status == "login":
    st.markdown("""
    <div class="logo-container">
        <div class="neon-orb-logo">🌊</div>
    </div>
    <h2 style="text-align: center; margin-bottom: 2px;">Welcome Back</h2>
    <p style="text-align: center; color: #8F90A6; font-size: 0.95rem; margin-bottom: 1.5rem;">Sign in to continue</p>
    """, unsafe_allow_html=True)

    with st.container():
        user_input_name = st.text_input("👤 Username or Email", placeholder="yourname@gmail.com")
        user_pass = st.text_input("🔒 Password", type="password", placeholder="••••••••")
        st.checkbox("Remember Me", value=True)
        
        if st.button("Login ➔", use_container_width=True, type="primary"):
            if user_input_name.strip() and len(user_pass) >= 4:
                st.session_state.user_name = user_input_name.split("@")[0].capitalize()
                st.session_state.auth_status = "permission"
                st.rerun()
            else:
                st.warning("Valid Email aur Password dalein.")
                
        st.markdown("<p style='text-align:center; color:#5A5A72; margin: 15px 0;'>— OR CONTINUE WITH —</p>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🌐 Google", use_container_width=True):
                st.session_state.user_name = "Google User"
                st.session_state.auth_status = "permission"
                st.rerun()
        with c2:
            st.button("👾 Discord", use_container_width=True)
        with c3:
            st.button("📘 Facebook", use_container_width=True)

# SCREEN 2: PERMISSION
elif st.session_state.auth_status == "permission":
    st.markdown("""
    <div style="text-align: center; margin-top: 20vh;">
        <div style="font-size: 3.5rem; margin-bottom: 10px;">🔐</div>
        <h2>Allow Access & Permissions</h2>
        <p style="color: #9AA0A6; max-width: 320px; margin: 0 auto 1.5rem auto;">
            App ko smooth run karne ke liye AI processing, storage aur session memory access allow karein.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Don't Allow", use_container_width=True):
            st.session_state.auth_status = "login"
            st.rerun()
    with col_b:
        if st.button("Allow & Continue", use_container_width=True, type="primary"):
            st.session_state.auth_status = "app"
            st.rerun()

# SCREEN 3: MAIN GEMINI APP
elif st.session_state.auth_status == "app":
    with st.sidebar:
        st.markdown("## ✨ Gemini AI")
        if st.button("➕ New Chat", use_container_width=True):
            new_title = f"Chat {datetime.now().strftime('%H:%M')}"
            st.session_state.all_chats[new_title] = []
            st.session_state.active_chat = new_title
            st.rerun()
            
        st.markdown("---")
        st.markdown("### 🕒 Recent Chats")
        for c_title in list(reversed(list(st.session_state.all_chats.keys())))[:8]:
            if st.button(f"🗨️ {c_title}", key=f"rec_{c_title}", use_container_width=True):
                st.session_state.active_chat = c_title
                st.rerun()
                
        st.markdown("---")
        st.markdown(f"**Logged in as:** `{st.session_state.user_name}`")
        if st.button("🔄 Switch Account / Logout", use_container_width=True):
            st.session_state.auth_status = "login"
            st.session_state.all_chats = {"Current Chat": []}
            st.rerun()

    col_head, col_pop = st.columns([8, 2])
    with col_head:
        pin = "📌 " if st.session_state.is_pinned else ""
        st.markdown(f"### {pin}Gemini")
    with col_pop:
        with st.popover("⋮"):
            st.markdown("### Actions")
            if st.button("🔗 Share conversation", use_container_width=True):
                st.toast("Link copied!")
            if st.button("📌 " + ("Remove pin" if st.session_state.is_pinned else "Pin chat"), use_container_width=True):
                st.session_state.is_pinned = not st.session_state.is_pinned
                st.rerun()
            rename_val = st.text_input("Rename", value=st.session_state.active_chat)
            if st.button("✏️ Rename", use_container_width=True):
                if rename_val.strip() and rename_val != st.session_state.active_chat:
                    st.session_state.all_chats[rename_val] = st.session_state.all_chats.pop(st.session_state.active_chat)
                    st.session_state.active_chat = rename_val
                    st.rerun()
            if st.button("❓ Help", use_container_width=True):
                st.info("Study, Earning, Stories aur Reels scripts banwayein!")
            if st.button("💬 Feedback", use_container_width=True):
                st.toast("Feedback registered!")
            if st.button("🗑️ Delete conversation", use_container_width=True):
                st.session_state.all_chats[st.session_state.active_chat] = []
                st.rerun()

    current_chat = st.session_state.all_chats[st.session_state.active_chat]

    if len(current_chat) == 0:
        st.markdown(f"""
        <div style="text-align: center; margin-top: 1rem;">
            <h1 style="font-size: 1.8rem; margin-bottom: 4px;">Where should we start?</h1>
            <p style="color: #94A3B8; font-size: 1rem;">Hello, {st.session_state.user_name}!</p>
            <div class="center-ai-orb">✨</div>
        </div>
        """, unsafe_allow_html=True)
        
        r1_1, r1_2 = st.columns(2)
        with r1_1:
            if st.button("🎓 Student Study Tutor", use_container_width=True):
                q = "Mujhe ek student study tutor ki tarah guide karo."
                current_chat.append({"role": "user", "content": q})
                with st.spinner("Processing..."):
                    reply = call_openrouter(f"Act as tutor: {q}", st.session_state.selected_model)
                    current_chat.append({"role": "assistant", "content": reply})
                st.rerun()
        with r1_2:
            if st.button("💰 Online Earning Ideas", use_container_width=True):
                q = "Zero investment se online earning ke practical tarike batao."
                current_chat.append({"role": "user", "content": q})
                with st.spinner("Processing..."):
                    reply = call_openrouter(f"Act as business expert: {q}", st.session_state.selected_model)
                    current_chat.append({"role": "assistant", "content": reply})
                st.rerun()

        r2_1, r2_2 = st.columns(2)
        with r2_1:
            if st.button("📖 Story & Novel Writer", use_container_width=True):
                q = "Ek interesting suspense story likho."
                current_chat.append({"role": "user", "content": q})
                with st.spinner("Processing..."):
                    reply = call_openrouter(f"Act as novelist: {q}", st.session_state.selected_model)
                    current_chat.append({"role": "assistant", "content": reply})
                st.rerun()
        with r2_2:
            if st.button("📱 Viral Content Creator", use_container_width=True):
                q = "Instagram reel script likho with 3 hooks."
                current_chat.append({"role": "user", "content": q})
                with st.spinner("Processing..."):
                    reply = call_openrouter(f"Act as viral strategist: {q}", st.session_state.selected_model)
                    current_chat.append({"role": "assistant", "content": reply})
                st
