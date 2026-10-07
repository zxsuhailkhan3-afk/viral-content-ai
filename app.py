import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="Omni AI Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark Sleek UI Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0b0b0e !important;
        color: #F1F1F5 !important;
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 6rem !important;
    }
    /* Top Pill Header */
    .top-mode-pill {
        background-color: #1a1a24;
        color: #60A5FA;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        border: 1px solid #2a2a38;
        margin-bottom: 12px;
    }
    /* Sidebar Theme */
    section[data-testid="stSidebar"] {
        background-color: #121218 !important;
        border-right: 1px solid #22222d !important;
    }
    /* Chat Input Bar */
    div[data-testid="stChatInput"] {
        border-radius: 26px !important;
        background-color: #1b1b22 !important;
        border: 1px solid #2f2f3d !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
    }
    .stChatMessage {
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }
</style>
""", unsafe_allow_html=True)

# API Setup
API_KEY = "AQ.Ab8RN6K_3MpnxhiJ-O9PzYV4wdnn8D9jInE9ghK7g8uQLbHVYw"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-3.8-flash")

# --- SMART SIDEBAR DRAWER (☰ Menu) ---
with st.sidebar:
    st.markdown("### ⚡ AI Master Studio")
    
    mode = st.selectbox(
        "AI Mode Chunein:",
        [
            "💬 Full Free Chat & Talk (Har cheez pucho)",
            "🎓 Student Study Tutor (Maths, Science, History, Code)",
            "💰 Online Earning & Business Master (Ghar baithe kamayi)",
            "📖 Story & Novel Writer (Kahaniyan likhein)",
            "📱 Viral Social Media Script (Reels, YT, Posts)"
        ]
    )
    
    st.markdown("---")
    
    # Sub-features based on selected mode
    if mode == "🎓 Student Study Tutor (Maths, Science, History, Code)":
        study_level = st.selectbox("Student Class / Level:", ["School (Class 1-10)", "College / 11th-12th", "Competitive Exam / UPSC / JEE", "Coding & Technical"])
        explain_style = st.selectbox("Samjhane Ka Tarika:", ["Step-by-step with simple examples", "Short & Quick Summary", "Exam Notes & Question Answers"])
        
    elif mode == "💰 Online Earning & Business Master (Ghar baithe kamayi)":
        earning_category = st.selectbox("Category:", ["Freelancing & Skills", "Content Creation & YouTube", "Affiliate Marketing & Blogging", "Zero Investment Hustles", "AI Tools & Automation"])
        
    elif mode == "📖 Story & Novel Writer (Kahaniyan likhein)":
        story_genre = st.selectbox("Story Type:", ["Horror & Suspense 👻", "Emotional & Love Story ❤️", "Motivational & Real Life 🚀", "Crime & Thriller 🕵️", "Desi Village Tales 🌾"])
        story_length = st.select_slider("Length:", options=["Short (1-2 Min)", "Full Story Script", "Deep Long Story"])
        
    elif mode == "📱 Viral Social Media Script (Reels, YT, Posts)":
        platform = st.selectbox("Platform:", ["Instagram Reels", "YouTube Shorts", "Facebook Video", "LinkedIn Post", "Twitter Thread"])

    st.markdown("---")
    if st.button("🗑️ New Chat (Screen Clear Karein)"):
        st.session_state.messages = []
        st.rerun()

# Top Active Mode Display
st.markdown(f'<div class="top-mode-pill">Active: {mode.split("(")[0]}</div>', unsafe_allow_html=True)

# Conversation History Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages on Screen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Bottom Unified Chat Input
user_query = st.chat_input("Pucho kuch bhi, baat karo, padhai ya kamayi ka idea...")

if user_query:
    # Append & Show user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("AI soch kar likh raha hai..."):
            
            # Dynamic prompt engineering for each specialized feature
            if "Student Study Tutor" in mode:
                system_prompt = f"""
                You are an expert personalized tutor for {study_level}.
                User query: '{user_query}'
                Explain style: {explain_style}.
                Explain concepts clearly, solve problems step-by-step, give practical real-world examples, and keep it extremely easy to understand in clean Hinglish/Hindi or English as asked.
                """
            elif "Online Earning" in mode:
                system_prompt = f"""
                You are a practical digital entrepreneur and online income consultant.
                Topic: '{user_query}'
                Focus Category: {earning_category}.
                Provide realistic, actionable, and 100% legitimate steps to earn money online.
                Breakdown: What skills are needed, step-by-step starting roadmap, which platforms to use, and how to get first client or revenue. Avoid generic fake scams.
                """
            elif "Story & Novel Writer" in mode:
                system_prompt = f"""
                You are a master fiction novelist and scriptwriter.
                Write a complete, gripping story on: '{user_query}'.
                Genre: {story_genre}
                Length: {story_length}
                Include strong character development, suspenseful hooks, vivid sensory descriptions, and a powerful ending.
                """
            elif "Viral Social Media" in mode:
                system_prompt = f"""
                You are a world-class viral content strategist.
                Create high-retention content for {platform} on topic: '{user_query}'.
                Include 3 viral hooks (0-3s), scene-by-scene script with visual cues, high-converting caption with call to action, and 15 targeted hashtags.
                """
            else:
                # Full free conversational AI (Gemini / ChatGPT style)
                system_prompt = f"""
                You are an exceptionally smart, helpful, empathetic, and witty AI companion like ChatGPT.
                You can converse naturally, advise on life, explain coding, write poetry, solve queries, and hold long contextual conversations.
                Answer clearly to: '{user_query}'.
                """

            try:
                # Include context history in query
                context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])
                full_request = f"Recent Conversation Context:\n{context}\n\nTask Instructions:\n{system_prompt}"
                
                response = model.generate_content(full_request)
                reply = response.text
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                err_text = f"Error: {e}"
                st.error(err_text)
                st.session_state.messages.append({"role": "assistant", "content": err_text})
                
