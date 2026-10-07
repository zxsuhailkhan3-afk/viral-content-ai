import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="Viral AI Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark ChatGPT Theme CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0b0b0f !important;
        color: #ECECF1 !important;
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 6rem !important;
    }
    /* Top Bar Title */
    .chat-pill {
        background: #1e1e24;
        color: #fff;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.95rem;
        display: inline-block;
        border: 1px solid #2d2d38;
        margin-bottom: 15px;
    }
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #121217 !important;
        border-right: 1px solid #23232d !important;
    }
    /* Bottom Chat Input Bar */
    div[data-testid="stChatInput"] {
        border-radius: 26px !important;
        background-color: #1e1e24 !important;
        border: 1px solid #32323f !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        font-size: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# API Setup
API_KEY = "AQ.Ab8RN6K_3MpnxhiJ-O9PzYV4wdnn8D9jInE9ghK7g8uQLbHVYw"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-3.8-flash")

# --- REAL WORKING SIDEBAR (☰ Menu) ---
with st.sidebar:
    st.markdown("### ⚙️ AI Studio Settings")
    
    app_mode = st.selectbox(
        "AI Feature Mode:",
        [
            "📱 Viral Social Media AI", 
            "📖 Master Story Writer", 
            "💬 Normal ChatGPT Bot", 
            "💼 Professional Copywriter"
        ]
    )

    st.markdown("---")
    
    # Dynamic settings based on selected mode
    if app_mode == "📖 Master Story Writer":
        st.markdown("#### 🎭 Story Controls")
        story_genre = st.selectbox("Story Type:", ["Horror & Suspense 👻", "Emotional & Romantic ❤️", "Motivational & Success 🚀", "Thriller / Crime 🕵️", "Desi Village Life 🌾", "Sci-Fi / Future 🤖"])
        story_length = st.select_slider("Kahani Ki Lambai:", options=["Short (1-2 Min)", "Medium (Reel / Video)", "Long Deep Story"])
        story_lang = st.selectbox("Language:", ["Hinglish (Roman)", "Pure Hindi", "English"])
    
    elif app_mode == "📱 Viral Social Media AI":
        st.markdown("#### 🎯 Platform Controls")
        target_platform = st.selectbox("Platform:", ["Instagram Reels", "YouTube Shorts", "Facebook Video", "X (Twitter) Thread", "LinkedIn"])
        viral_tone = st.selectbox("Tone:", ["Ultra Viral & Punchy 🔥", "Curiosity / Mystery 🤫", "Informative 🧠", "Aggressive Hook ⚡"])
    
    st.markdown("---")
    if st.button("🗑️ New Chat (Reset)"):
        st.session_state.messages = []
        st.rerun()

# Top Header Indicator
st.markdown(f'<div class="chat-pill">✨ {app_mode}</div>', unsafe_allow_html=True)

# Chat Session Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show Previous Chat Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Bottom Input Bar
user_prompt = st.chat_input("Kuch bhi pucho ya story/topic ka idea yahan likhein...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI likh raha hai..."):
            # Custom system prompt according to active mode
            if app_mode == "📖 Master Story Writer":
                system_instruction = f"""
                You are a world-class award-winning storyteller and scriptwriter.
                Write a gripping story based on: '{user_prompt}'.
                Genre: {story_genre}
                Length: {story_length}
                Language Format: {story_lang}

                Format properly:
                - **Catchy Title**
                - **Scene Setup / Character Introduction**
                - **The Climax / Turning Point**
                - **Emotional / Shocking Ending**
                - **Moral or Key Takeaway**
                """
            elif app_mode == "📱 Viral Social Media AI":
                system_instruction = f"""
                You are a top viral growth strategist.
                Create high-retention content for {target_platform} with tone '{viral_tone}'.
                Topic: '{user_prompt}'

                Format:
                ### 🎣 Viral Hooks (0-3s)
                ### 📜 Full Script with Camera/Visual Directions
                ### ✍️ High-Engagement Caption & Call to Action (CTA)
                ### 🏷️ 15 Trending Hashtags
                """
            elif app_mode == "💼 Professional Copywriter":
                system_instruction = f"""
                You are an expert copywriter. Write a persuasive, high-converting marketing copy on: '{user_prompt}'.
                Include strong headline, problem agitation, solution, social proof angle, and call to action.
                """
            else: # Normal ChatGPT Bot
                system_instruction = f"You are a helpful, smart AI assistant like ChatGPT. Answer user query comprehensively: '{user_prompt}'."

            try:
                response = model.generate_content(system_instruction)
                output_content = response.text
                st.markdown(output_content)
                st.session_state.messages.append({"role": "assistant", "content": output_content})
            except Exception as e:
                err = f"API Error: {e}"
                st.error(err)
                st.session_state.messages.append({"role": "assistant", "content": err})
    
