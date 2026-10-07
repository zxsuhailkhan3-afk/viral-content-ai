import streamlit as st
import google.generativeai as genai

# Page settings
st.set_page_config(
    page_title="ViralForge AI", 
    page_icon="⚡", 
    layout="centered"
)

# Custom CSS for Premium UI
st.markdown("""
<style>
    /* Gradient heading */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 50%, #FFA07A 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .hero-subtitle {
        text-align: center;
        color: #94A3B8;
        font-size: 0.95rem;
        margin-bottom: 24px;
    }
    /* Card container */
    .metric-badge {
        display: inline-block;
        background: #1E293B;
        color: #38BDF8;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 15px;
    }
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #6366F1, #8B5CF6);
        color: white;
        font-weight: 700;
        font-size: 1rem;
        border-radius: 12px;
        border: none;
        padding: 0.75rem 1rem;
        transition: transform 0.2s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# API Setup
API_KEY = "AQ.Ab8RN6K_3MpnxhiJ-O9PzYV4wdnn8D9jInE9ghK7g8uQLbHVYw"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")

# Header Section
st.markdown('<div class="hero-title">⚡ ViralForge AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Turn raw ideas into high-retention viral scripts & posts in seconds</div>', unsafe_allow_html=True)

# Main Form
col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox(
        "🎯 Target Platform", 
        ["Instagram Reels", "YouTube Shorts", "LinkedIn Pulse", "X (Twitter) Thread"]
    )
with col2:
    tone = st.selectbox(
        "🔥 Tone & Style", 
        ["High Energy & Punchy", "Storytelling & Curiosity", "Educational & Authoritative", "Bold & Controversial"]
    )

topic = st.text_area(
    "💡 Content Idea / Topic",
    placeholder="e.g. 3 passive income sources for college students in 2026...",
    height=110
)

# Generator trigger
if st.button("Generate Viral Blueprint 🚀"):
    if topic.strip():
        with st.spinner("Analyzing viral hooks and crafting your blueprint..."):
            prompt = f"""
            You are an elite ghostwriter and viral media strategist.
            Create a high-retention, conversion-optimized blueprint for {platform}.
            Tone: {tone}
            Topic: {topic}

            Use this structured markdown output:
            ### 🎣 3 Tested Hooks (Choose 1)
            - **Visual / Action:** ...
            - **Opening Line:** ...

            ---
            ### 📜 Full Script & Story Arc
            (Breakdown pacing: 0-3s Hook, 3-15s Retain, 15-45s Value drops, 45-60s Payoff)

            ---
            ### ✍️ Caption & CTA
            (Engagement-driving caption with comment trigger)

            ---
            ### 🏷️ 15 High-Reach Hashtags
            """
            try:
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown("### 📋 Generated Blueprint")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error generating content: {e}")
    else:
        st.warning("Pehle apna idea ya topic likhein!")
        
