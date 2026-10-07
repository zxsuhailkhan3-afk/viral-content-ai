import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. Native Mobile Screen Configuration
st.set_page_config(
    page_title="Gemini AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Perfect Mobile Viewport & ChatGPT/Gemini Theme CSS
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    /* Pure Black Dark Theme */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #E3E3E3 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }
    
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* App container fitting */
    .block-container {
        max-width: 100% !important;
        padding-top: 0.8rem !important;
        padding-bottom: 5.5rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }

    /* Top Navigation Bar */
    .mobile-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 6px 4px 14px 4px;
        border-bottom: 1px solid #1a1a1a;
        margin-bottom: 10px;
    }
    .header-pill {
        background-color: #1a1a1a;
        color: #E3E3E3;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 600;
        border: 1px solid #2a2a2a;
    }

    /* Side Drawer Menu styling */
    section[data-testid="stSidebar"] {
        background-color: #0e0e0e !important;
        border-right: 1px solid #1f1f1f !important;
    }
    
    /* Recent History Capsule item */
    .history-card {
        background-color: #1a1a1a;
        color: #f1f1f1;
        padding: 10px 14px;
        border-radius: 12px;
        margin-bottom: 8px;
        font-size: 0.9rem;
        border: 1px solid #262626;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Message Typography */
    .stChatMessage {
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        padding: 10px 0px !important;
    }

    /* Bottom Floating Rounded Input Box */
    div[data-testid="stChatInput"] {
        border-radius: 28px !important;
        background-color: #1e1e1e !important;
        border: 1px solid #333333 !important;
        padding: 4px 10px !important;
        box-shadow: 0 4px 25px rgba(0,0,0,0.8) !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
    }
</style>
""", unsafe_allow_html=True)

# API Setup
API_KEY = "AQ.Ab8RN6K_3MpnxhiJ-O9PzYV4wdnn8D9jInE9ghK7g8uQLbHVYw"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-3.8-flash")

# Session state initialization
if "all_chats" not in st.session_state:
    # Multiple chat session history memory
    st.session_state.all_chats = {"Current Chat": []}
if "current_chat_name" not in st.session_state:
    st.session_state.current_chat_name = "Current Chat"

# --- SIDEBAR DRAWER (Photo 3: Gemini History & Features) ---
with st.sidebar:
    st.markdown("## ✨ Gemini AI")
    
    # New chat button
    if st.button("➕ New chat", use_container_width=True):
        new_name = f"Chat {datetime.now().strftime('%H:%M:%S')}"
        st.session_state.all_chats[new_name] = []
        st.session_state.current_chat_name = new_name
        st.rerun()

    st.markdown("---")
    
    # Specialized App Modes
    st.markdown("### 🧭 Studios & Features")
    app_mode = st.selectbox(
        "Feature Mode:",
        [
            "💬 Free General AI (Chat & Talk)",
            "🎓 Students Study (Maths, Science, Code)",
            "💰 Online Earning & Business Master",
            "📖 Story & Script Novelist",
            "📱 Viral Social Media Studio"
        ]
    )

    if app_mode == "📖 Story & Script Novelist":
        story_genre = st.selectbox("Genre:", ["Horror & Suspense 👻", "Emotional & Love ❤️", "Motivational 🚀", "Crime & Thriller 🕵️"])
        story_len = st.select_slider("Length:", options=["Short Story", "Detailed Video Script", "Long Deep Novel"])
    elif app_mode == "📱 Viral Social Media Studio":
        platform = st.selectbox("Platform:", ["Instagram Reels", "YouTube Shorts", "Facebook Post", "LinkedIn"])

    st.markdown("---")
    
    # Recent Chats History List (Photo 3 look)
    st.markdown("### 🕒 Recent Chats")
    chat_keys = list(st.session_state.all_chats.keys())
    for c_name in reversed(chat_keys[-8:]):
        if st.button(f"🗨️ {c_name}", key=f"btn_{c_name}", use_container_width=True):
            st.session_state.current_chat_name = c_name
            st.rerun()

    # Chat Options Pop-up / Controls (Photo 4 Action Menu)
    st.markdown("---")
    with st.expander("⚙️ Chat Options (Pop-up Menu)"):
        st.markdown("**Action Menu:**")
        if st.button("🗑️ Delete This Conversation", use_container_width=True):
            st.session_state.all_chats[st.session_state.current_chat_name] = []
            st.rerun()
        if st.button("📌 Pin Conversation", use_container_width=True):
            st.toast("Conversation pinned to top!")
        st.caption("ℹ️ Share & Rename active in this session.")

# Top Navigation Bar
current_messages = st.session_state.all_chats[st.session_state.current_chat_name]
top_title = app_mode.split("(")[0].strip()

st.markdown(f"""
<div class="mobile-header">
    <div style="font-size: 1.3rem;">☰</div>
    <div class="header-pill">{top_title}</div>
    <div style="font-size: 1.1rem;">⚙️</div>
</div>
""", unsafe_allow_html=True)

# Display Messages for the active conversation
for msg in current_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Bottom Floating ChatGPT Input
user_input = st.chat_input("Ask Gemini / Kuch bhi pucho ya likhein...")

if user_input:
    # Append user question
    current_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if "Students Study" in app_mode:
                system_prompt = f"You are a master personal tutor. Solve problems step-by-step, explain with crystal clear examples: '{user_input}'."
            elif "Online Earning" in app_mode:
                system_prompt = f"You are an online income and business strategist. Give practical, 100% genuine step-by-step roadmap to earn money: '{user_input}'."
            elif "Story & Script" in app_mode:
                system_prompt = f"Write a compelling story for genre '{story_genre}' and length '{story_len}' on: '{user_input}'. Include title, hooks, and dramatic ending."
            elif "Viral Social Media" in app_mode:
                system_prompt = f"Create high-retention viral content for {platform} on '{user_input}'. Provide 3 hooks, scene-by-scene script, caption, and hashtags."
            else:
                system_prompt = f"You are an advanced, helpful, and friendly AI companion like ChatGPT/Gemini. Answer naturally: '{user_input}'."

            try:
                # Add context of previous messages
                context_str = "\n".join([f"{m['role']}: {m['content']}" for m in current_messages[-4:]])
                full_query = f"Conversation History:\n{context_str}\n\nTask:\n{system_prompt}"
                
                res = model.generate_content(full_query)
                answer = res.text
                st.markdown(answer)
                current_messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                err_text = f"API Error: {e}"
                st.error(err_text)
                current_messages.append({"role": "assistant", "content": err_text})
    
