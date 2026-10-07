import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Mobile Native Layout
st.set_page_config(
    page_title="Gemini",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom Mobile CSS
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0b0b0e !important;
        color: #E3E3E8 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }
    header[data-testid="stHeader"] {
        background-color: #0b0b0e !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 6rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 100% !important;
    }
    div[data-testid="stChatInput"] {
        border-radius: 28px !important;
        background-color: #1e1e26 !important;
        border: 1px solid #333344 !important;
        padding: 4px 10px !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #121218 !important;
        border-right: 1px solid #22222d !important;
    }
</style>
""", unsafe_allow_html=True)

# Yahan apni Step 1 wali AIzaSy key paste karein
API_KEY = "AIzaSy_APNI_KEY_YAHAN_DALO"

# Agar code mein key na badli ho toh screen par mangega
if not API_KEY.startswith("AIzaSy"):
    user_key = st.sidebar.text_input("Gemini API Key (AIzaSy...):", type="password")
    if user_key:
        API_KEY = user_key.strip()

# Initialize Chat Memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- WORKING SIDEBAR DRAWER (Recent Chats + Features) ---
with st.sidebar:
    st.markdown("## ✨ Gemini Studio")
    if st.button("➕ New chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.markdown("### 🧭 Special Features")
    app_mode = st.radio(
        "Feature Mode:",
        [
            "💬 General AI Chat (Sab Kuch Pucho)",
            "🎓 Students Help (Maths, Science, Code)",
            "💰 Online Earning & Business Roadmap",
            "📖 Story Writer (Horror, Suspense, Love)",
            "📱 Viral Social Media (Reels & Shorts)"
        ]
    )

    st.markdown("---")
    with st.expander("⚙️ Chat Options (Pop-up Menu)", expanded=False):
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

# Top Title Bar
st.markdown(f"#### ✨ {app_mode.split('(')[0].strip()}")

# Show Empty State or Messages
if len(st.session_state.chat_history) == 0:
    st.markdown("""
    <div style="text-align: center; margin-top: 18vh; color: #8F8FA0;">
        <h2 style="color: #FFFFFF; font-size: 2.2rem; margin-bottom: 6px;">Gemini</h2>
        <p style="font-size: 1rem;">Ask anything, padhai, kamayi ya kahani likhwao...</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Bottom Floating Input
user_query = st.chat_input("Ask Gemini / Kuch bhi pucho...")

if user_query:
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        if not API_KEY.startswith("AIzaSy"):
            err_box = "Kripya sidebar mein apni valid 'AIzaSy' wali Gemini API Key dalein."
            st.error(err_box)
            st.session_state.chat_history.append({"role": "assistant", "content": err_box})
        else:
            with st.spinner("Gemini is answering..."):
                try:
                    genai.configure(api_key=API_KEY)
                    model = genai.GenerativeModel("models/gemini-2.5-flash")
                    
                    full_prompt = f"Mode: {app_mode}\nUser Request: {user_query}\nAnswer clearly in Hinglish/Hindi or English as requested."
                    response = model.generate_content(full_prompt)
                    ans = response.text
                    st.markdown(ans)
                    st.session_state.chat_history.append({"role": "assistant", "content": ans})
                except Exception as e:
                    st.error(f"Error: {e}")
                    
