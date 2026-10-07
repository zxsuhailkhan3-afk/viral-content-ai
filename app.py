import streamlit as st
import google.generativeai as genai

# 1. LOGO AUR APP TITLE SETTINGS
# 'page_icon' mein aap apna emoji logo rakh sakte hain (jaise 🤖, 🔥, 🚀, 💬)
st.set_page_config(
    page_title="Viral AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ChatGPT Style UI Theme
st.markdown("""
<style>
    /* Pure Black Background like ChatGPT */
    .stApp {
        background-color: #0d0d0d;
        color: #ECECF1;
    }
    
    /* Top Header Bar */
    .chat-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 4px 18px 4px;
        border-bottom: 1px solid #212121;
        margin-bottom: 20px;
    }
    .chat-header-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #E3E3E3;
    }
    .chat-badge {
        background-color: #212121;
        color: #10A37F;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid #2f2f2f;
    }
    
    /* Selector Pills */
    .stSelectbox label {
        color: #9E9E9E !important;
        font-size: 0.82rem !important;
    }
    div[data-baseweb="select"] {
        border-radius: 12px !important;
    }
    
    /* Message styling */
    .stChatMessage {
        background-color: transparent !important;
        border-radius: 12px;
        padding: 10px 0px;
    }
    
    /* Sticky Bottom Input Bar like ChatGPT */
    div[data-testid="stChatInput"] {
        border-radius: 24px !important;
        background-color: #212121 !important;
        border: 1px solid #303030 !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #555555 !important;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_KEY = "AQ.Ab8RN6K_3MpnxhiJ-O9PzYV4wdnn8D9jInE9ghK7g8uQLbHVYw"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-3.8-flash")

# Top ChatGPT-style Bar
st.markdown("""
<div class="chat-header">
    <div class="chat-header-title">✨ Viral AI</div>
    <div class="chat-badge">Pro 2.5</div>
</div>
""", unsafe_allow_html=True)

# Compact Filters (Platform & Tone)
col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("Platform", ["Instagram Reels", "YouTube Shorts", "Facebook Post", "LinkedIn"], label_visibility="collapsed")
with col2:
    tone = st.selectbox("Tone", ["Viral & Punchy", "Storytelling", "Educational", "Controversial"], label_visibility="collapsed")

# Chat History Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Conversation History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Bottom Input Bar (ChatGPT style)
prompt_topic = st.chat_input("Apna video ya post topic yahan likhein...")

if prompt_topic:
    # User message display
    st.session_state.messages.append({"role": "user", "content": prompt_topic})
    with st.chat_message("user"):
        st.markdown(prompt_topic)

    # AI Response generation
    with st.chat_message("assistant"):
        with st.spinner("Writing blueprint..."):
            system_prompt = f"""
            You are an elite viral social media strategist.
            Create high-converting, viral content for {platform} with tone '{tone}'.
            Topic: {prompt_topic}

            Format cleanly:
            ### 🎣 3 Viral Hooks
            ### 📜 Full Script & Pacing
            ### ✍️ Caption & Call to Action (CTA)
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
                
