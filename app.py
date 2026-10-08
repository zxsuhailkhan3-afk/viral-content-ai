import streamlit as st
import requests
import json
from datetime import datetime

# Page & Viewport Settings
st.set_page_config(
    page_title="Gemini",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# FIXED TRUE DARK THEME CSS
st.markdown("""
<style>
    /* Pure Pitch Black Theme */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0d0d12 !important;
        color: #F3F4F6 !important;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #13131a !important;
        border-right: 1px solid #232332 !important;
    }

    /* Container padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 7rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
        max-width: 100% !important;
    }

    /* Glowing AI Avatar Orb */
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

    /* Buttons */
    .stButton>button {
        background-color: #1e1e2d !important;
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

    /* Floating Rounded Input Box */
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
</style>
""", unsafe_allow_html=True)

# API KEY
API_KEY = "AQ.Ab8RN6J99bgmwD-kodjf4JFv1bDK80J663YAn0qArf-4OWailQ"

if "auth_status" not in st.session_state:
    st.session_state.auth_status = "app"
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

# Direct Valid API Call (OAuth issue resolved)
def call_gemini(prompt_text):
    # Fixed endpoint with pure query parameter & x-goog-api-key header (No Bearer conflict)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=35)
        data = res.json()
        if res.status_code == 200:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"API Error ({res.status_code}): {data.get('error', {}).get('message', res.text)}"
    except Exception as e:
        return f"Network Error: {e}"

# --- SIDEBAR DRAWER ---
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
        st.session_state.all_chats = {"Current Chat": []}
        st.rerun()

# --- TOP HEADER BAR ---
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
        if st.button("🗑️ Delete conversation", use_container_width=True):
            st.session_state.all_chats[st.session_state.active_chat] = []
            st.rerun()

current_chat = st.session_state.all_chats[st.session_state.active_chat]

# Welcome Screen
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
                reply = call_gemini(f"Act as tutor: {q}")
                current_chat.append({"role": "assistant", "content": reply})
            st.rerun()
    with r1_2:
        if st.button("💰 Online Earning Ideas", use_container_width=True):
            q = "Zero investment se online earning ke practical tarike batao."
            current_chat.append({"role": "user", "content": q})
            with st.spinner("Processing..."):
                reply = call_gemini(f"Act as business expert: {q}")
                current_chat.append({"role": "assistant", "content": reply})
            st.rerun()

    r2_1, r2_2 = st.columns(2)
    with r2_1:
        if st.button("📖 Story & Novel Writer", use_container_width=True):
            q = "Ek interesting suspense story likho."
            current_chat.append({"role": "user", "content": q})
            with st.spinner("Processing..."):
                reply = call_gemini(f"Act as novelist: {q}")
                current_chat.append({"role": "assistant", "content": reply})
            st.rerun()
    with r2_2:
        if st.button("📱 Viral Content Creator", use_container_width=True):
            q = "Instagram reel script likho with 3 hooks."
            current_chat.append({"role": "user", "content": q})
            with st.spinner("Processing..."):
                reply = call_gemini(f"Act as viral strategist: {q}")
                current_chat.append({"role": "assistant", "content": reply})
            st.rerun()

# Message Stream
for msg in current_chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Model Selection
col_m, _ = st.columns([3, 1])
with col_m:
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

# Floating Input Bar
user_query = st.chat_input("Ask Gemini...")

if user_query:
    current_chat.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Gemini soch raha hai..."):
            context = "\n".join([f"{m['role']}: {m['content']}" for m in current_chat[-3:]])
            prompt = f"Mode: {st.session_state.selected_model}\nContext:\n{context}\n\nTask: {user_query}\nJawab Hinglish/Hindi ya English mein clear aur accurate dein."
            
            ans = call_gemini(prompt)
            st.markdown(ans)
            current_chat.append({"role": "assistant", "content": ans})
