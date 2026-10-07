import streamlit as st
import google.generativeai as genai

# Mobile App configuration
st.set_page_config(
    page_title="ChatGPT",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling for exact ChatGPT Mobile App feel
st.markdown("""
<style>
    /* Full Black Background & Padding reset */
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    /* Hide Streamlit default header decoration */
    header[data-testid="stHeader"] {
        background: transparent !important;
        display: none !important;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* ChatGPT Top Bar */
    .chatgpt-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 6px 0px 18px 0px;
    }
    .nav-circle-btn {
        width: 44px;
        height: 44px;
        background-color: #212121;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        color: #ECECF1;
        border: 1px solid #2A2A2A;
    }
    .nav-pill-btn {
        background-color: #171717;
        color: #ECECF1;
        padding: 8px 18px;
        border-radius: 25px;
        font-size: 0.95rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
        border: 1px solid #2B2B2B;
    }

    /* Select Boxes Styling - Bold & Large */
    div[data-baseweb="select"] {
        border-radius: 18px !important;
        background-color: #181818 !important;
        border: 1px solid #2E2E2E !important;
        min-height: 48px !important;
    }
    div[data-baseweb="select"] * {
        font-size: 1rem !important;
        color: #F1F1F1 !important;
    }

    /* ChatGPT Chat Bubble Text */
    .stChatMessage {
        background-color: transparent !important;
        font-size: 1.08rem !important;
        line-height: 1.6 !important;
        padding: 12px 0px !important;
    }
    
    /* Bottom Floating Rounded Input Bar like ChatGPT */
    div[data-testid="stChatInput"] {
        border-radius: 28px !important;
        background-color: #212121 !important;
        border: 1px solid #363636 !important;
        padding: 6px 14px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6) !important;
    }
    div[data-testid="stChatInput"] textarea {
        font-size: 1.05rem !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #8E8EA0 !important;
    }
</style>
""", unsafe_allow_html=True)

# API Setup
API_KEY = "AQ.Ab8RN6K_3MpnxhiJ-O9PzYV4wdnn8D9jInE9ghK7g8uQLbHVYw"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-3.8-flash")

# Top ChatGPT Header Bar (Side buttons + Center Pill)
st.markdown("""
<div class="chatgpt-nav">
    <div class="nav-circle-btn">☰</div>
    <div class="nav-pill-btn">✨ Viral AI</div>
    <div class="nav-circle-btn">💬</div>
</div>
""", unsafe_allow_html=True)

# Selectors as large tap-friendly dropdowns
col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("Platform", ["Instagram Reels", "YouTube Shorts", "Facebook Post", "LinkedIn"], label_visibility="collapsed")
with col2:
    tone = st.selectbox("Tone", ["Viral & Punchy", "Storytelling", "Educational", "Bold Hook"], label_visibility="collapsed")

# Session State for Messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Bottom Input Bar
prompt_topic = st.chat_input("Ask Viral AI (topic ya idea likhein)...")

if prompt_topic:
    st.session_state.messages.append({"role": "user", "content": prompt_topic})
    with st.chat_message("user"):
        st.markdown(prompt_topic)

    with st.chat_message("assistant"):
        with st.spinner("AI likh raha hai..."):
            system_prompt = f"""
            You are a top viral social media manager.
            Create high-engagement viral content for {platform} with tone '{tone}'.
            Topic: {prompt_topic}

            Format:
            ### 🎣 Viral Hook (0-3 Sec)
            ### 📜 Full Script & Scene Flow
            ### ✍️ Caption & CTA
            ### 🏷️ 15 Trending Hashtags
            """
            try:
                response = model.generate_content(system_prompt)
                output_text = response.text
                st.markdown(output_text)
                st.session_state.messages.append({"role": "assistant", "content": output_text})
            except Exception as e:
                err_msg = f"Error: {e}"
                st.error(err_msg)
                st.session_state.messages.append({"role": "assistant", "content": err_msg})
                
