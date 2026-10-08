import streamlit as st
import requests
import json
from datetime import datetime

# Mobile Viewport Settings
st.set_page_config(
    page_title="Gemini",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Dark Sleek UI Styling
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0b0c10 !important;
        color: #F1F1F5 !important;
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
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }
    .neon-orb-logo {
        width: 110px;
        height: 110px;
        border-radius: 35px;
        background: radial-gradient(circle at 30% 30%, #38bdf8, #2563eb, #1e1b4b);
        box-shadow: 0 15px 35px rgba(37, 99, 235, 0.45);
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 3rem;
    }

    .center-ai-orb {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin: 1.5rem auto;
        background: radial-gradient(circle at 35% 35%, #c084fc, #6366f1, #3b82f6);
        box-shadow: 0 0 50px rgba(168, 85, 247, 0.55);
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 2.2rem;
    }

    /* Fixed Bottom Container for Model Picker & Input */
    .bottom-dock {
        position: fixed;
        bottom: 8px;
        left: 2%;
        right: 2%;
        width: 96%;
        z-index: 99999;
    }

    div[data-testid="stChatInput"] {
        border-radius: 28px !important;
        background-color: #1a1a24 !important;
        border: 1px solid #33334d !important;
        padding: 4px 10px !important;
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.9) !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #101016 !important;
        border-right: 1px solid #1f1f2e !important;
    }
    
    .stButton>button {
        border-radius: 14px !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

API_KEY = "AQ.Ab8RN6J99bgmwD-kodjf4JFv1bDK80J663YAn0qArf-4OWailQ"

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
    st.session_state.selected_model = "3.8 Flash (All-around help)"

# Model Mapping
MODEL_ENGINE_MAP = {
    "3.5 Flash-Lite (Fastest answers)": "gemini-2.5-flash",
    "3.8 Flash (All-around help)": "gemini-2.5-flash",
    "3.1 Pro (Advanced reasoning)": "gemini-2.5-pro",
    "Extended thinking (Complex problem solving)": "gemini-2.5-pro"
}

def call_gemini(prompt_text, selected_model_name):
    target_engine = MODEL_ENGINE_MAP.get(selected_model_name, "gemini-2.5-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_engine}:generateContent?key={API_KEY}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    if "Extended thinking" in selected_model_name:
        prompt_text = "Perform deep step-by-step extended logical thinking before giving final answer: " + prompt_text

    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=40)
        data = res.json()
        if res.status_code == 200:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"API Error: {data.get('error', {}).get('message', res.text)}"
    except Exception as e:
        return f"Network Error: {e}"

# --- SCREEN 1: LOGIN ---
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

# --- SCREEN 2: PERMISSION ---
elif st.session_state.auth_status == "permission":
    st.markdown("""
    <div style="text-align: center; margin-top: 20vh;">
        <div style="font-size: 3.5rem; margin-bottom: 10px;">🔐</div>
        <h2>Allow Access & Permissions</h2>
        <p style="color: #9AA0A6; max-width: 320px; margin: 0 auto 1.5rem auto;">
            App ko smooth run karne ke liye AI processing, storage aur session memory allow karein.
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

# --- SCREEN 3: MAIN APP WITH MODEL SELECTOR ---
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

    header_col1, header_col2 = st.columns([8, 2])
    with header_col1:
        pin_icon = "📌 " if st.session_state.is_pinned else ""
        st.markdown(f"### {pin_icon}Gemini")
    with header_col2:
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
                st.toast("Feedback sent!")
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
        
        row1_c1, row1_c2 = st.columns(2)
        with row1_c1:
            if st.button("🎓 Student Study Tutor", use_container_width=True):
                q = "Mujhe ek student study tutor ki tarah guide karo."
                current_chat.append({"role": "user", "content": q})
                with st.spinner("Processing..."):
                    reply = call_gemini(f"Act as tutor: {q}", st.session_state.selected_model)
                    current_chat.append({"role": "assistant", "content": reply})
                st.rerun()
        with row1_c2:
            if st.button("💰 Online Earning Ideas", use_container_width=True):
                q = "Zero investment se online earning ke practical tarike batao."
                current_chat.append({"role": "user", "content": q})
                with st.spinner("Processing..."):
                    reply = call_gemini(f"Act as business expert: {q}", st.session_state.selected_model)
                    current_chat.append({"role": "assistant", "content": reply})
                st.rerun()

        row2_c1, row2_c2 = st.columns(2)
        with row2_c1:
            if st.button("📖 Story & Novel Writer", use_container_width=True):
                q = "Ek interesting suspense story likho."
                current_chat.append({"role": "user", "content": q})
                with st.spinner("Processing..."):
                    reply = call_gemini(f"Act as novelist: {q}", st.session_state.selected_model)
                    current_chat.append({"role": "assistant", "content": reply})
                st.rerun()
        with row2_c2:
            if st.button("📱 Viral Content Creator", use_container_width=True):
                q = "Instagram reel script likho with 3 hooks."
                current_chat.append({"role": "user", "content": q})
                with st.spinner("Processing..."):
                    reply = call_gemini(f"Act as viral strategist: {q}", st.session_state.selected_model)
                    current_chat.append({"role": "assistant", "content": reply})
                st.rerun()

    for msg in current_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Bottom Area: Gemini Model Switcher + Floating Input
    col_mod, _ = st.columns([2, 1])
    with col_mod:
        st.session_state.selected_model = st.selectbox(
            "⚡ Gemini Model:",
            [
                "3.8 Flash (All-around help)",
                "3.5 Flash-Lite (Fastest answers)",
                "3.1 Pro (Advanced reasoning)",
                "Extended thinking (Complex problem solving)"
            ],
            index=0
        )

    user_query = st.chat_input("Ask Gemini...")

    if user_query:
        current_chat.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner(f"Gemini ({st.session_state.selected_model}) soch raha hai..."):
                context = "\n".join([f"{m['role']}: {m['content']}" for m in current_chat[-4:]])
                prompt = f"Context:\n{context}\n\nTask:\n{user_query}\nJawab Hinglish/Hindi ya English mein clear dein."
                
                ans = call_gemini(prompt, st.session_state.selected_model)
                st.markdown(ans)
                current_chat.append({"role": "assistant", "content": ans})
