import streamlit as st
import google.generativeai as genai

# Proper Mobile App Viewport Settings
st.set_page_config(
    page_title="Omni AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Native Mobile App Styling (ChatGPT Look)
st.markdown("""
<style>
    /* Mobile App Pure Black Background */
    .stApp {
        background-color: #0b0b0e !important;
        color: #F1F1F5 !important;
    }
    
    /* Top Header clean-up */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Mobile padding & font enlargement */
    .block-container {
        max-width: 100% !important;
        padding-top: 1rem !important;
        padding-bottom: 5.5rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    
    /* Active Mode Pill */
    .top-pill {
        background-color: #1a1a24;
        color: #60A5FA;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.95rem;
        display: inline-block;
        border: 1px solid #2a2a38;
        margin-bottom: 12px;
    }
    
    /* Mobile Drawer Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #121218 !important;
        border-right: 1px solid #22222d !important;
    }
    
    /* ChatGPT Mobile Style Bottom Floating Input */
    div[data-testid="stChatInput"] {
        border-radius: 28px !important;
        background-color: #1f1f27 !important;
        border: 1px solid #323242 !important;
        padding: 4px 10px !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
    }
    
    /* Chat message text size */
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

# --- MOBILE SIDEBAR DRAWER (☰ menu dabane par hi khulega) ---
with st.sidebar:
    st.markdown("### ⚡ AI Master Studio")
    
    mode = st.selectbox(
        "AI Feature Mode:",
        [
            "💬 Full Free Chat & Talk (Har cheez pucho)",
            "🎓 Student Study Tutor (Maths, Science, Code)",
            "💰 Online Earning & Business Master",
            "📖 Story & Novel Writer (Kahaniyan)",
            "📱 Viral Social Media Script"
        ]
    )
    
    st.markdown("---")
    
    if mode == "🎓 Student Study Tutor (Maths, Science, Code)":
        study_level = st.selectbox("Class / Level:", ["School (1-10)", "College / 11th-12th", "Competitive Exam", "Coding & Tech"])
        explain_style = st.selectbox("Style:", ["Step-by-step with examples", "Short Summary", "Exam Notes"])
        
    elif mode == "💰 Online Earning & Business Master":
        earning_cat = st.selectbox("Category:", ["Freelancing & Skills", "Content Creation / YouTube", "Affiliate Marketing", "Zero Investment"])
        
    elif mode == "📖 Story & Novel Writer (Kahaniyan)":
        story_genre = st.selectbox("Genre:", ["Horror & Suspense 👻", "Emotional & Love ❤️", "Motivational 🚀", "Crime & Thriller 🕵️", "Desi Tales 🌾"])
        story_len = st.select_slider("Length:", options=["Short (1-2 Min)", "Full Story Script", "Deep Long Story"])
        
    elif mode == "📱 Viral Social Media Script":
        platform = st.selectbox("Platform:", ["Instagram Reels", "YouTube Shorts", "Facebook Video", "LinkedIn Post", "Twitter Thread"])

    st.markdown("---")
    if st.button("🗑️ New Chat (Clear Screen)"):
        st.session_state.messages = []
        st.rerun()

# Top Active Status
mode_label = mode.split("(")[0]
st.markdown(f'<div class="top-pill">Active: {mode_label}</div>', unsafe_allow_html=True)

# Chat History Session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Message History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Bottom Input Bar
user_query = st.chat_input("Pucho kuch bhi, padhai, kamayi ya kahani...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("AI likh raha hai..."):
            
            if "Student Study Tutor" in mode:
                system_prompt = f"You are an expert tutor for {study_level}. Solve/explain step-by-step with clear examples: {user_query}. Style: {explain_style}."
            elif "Online Earning" in mode:
                system_prompt = f"You are a digital income expert. Category: {earning_cat}. Give actionable roadmap, platforms, and real steps to earn for: {user_query}."
            elif "Story & Novel Writer" in mode:
                system_prompt = f"Write an engaging story on '{user_query}'. Genre: {story_genre}, Length: {story_len}. Include title, gripping hooks, climax and emotional finish."
            elif "Viral Social Media" in mode:
                system_prompt = f"Create high-retention content for {platform} on '{user_query}'. Include 3 viral hooks (0-3s), scene script, caption, CTA, and 15 hashtags."
            else:
                system_prompt = f"You are a versatile, helpful AI like ChatGPT. Answer user query comprehensively: '{user_query}'."

            try:
                context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])
                full_request = f"Chat Context:\n{context}\n\nTask:\n{system_prompt}"
                
                response = model.generate_content(full_request)
                reply = response.text
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                err_text = f"Error: {e}"
                st.error(err_text)
                st.session_state.messages.append({"role": "assistant", "content": err_text})
                
