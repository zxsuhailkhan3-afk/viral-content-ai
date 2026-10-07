import streamlit as st
import google.generativeai as genai
import requests

# 1. Native Mobile Screen Fit
st.set_page_config(
    page_title="Gemini AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Complete Mobile Scaling CSS (ChatGPT / Gemini look)
st.markdown("""
<style>
    /* Full Phone Black Background */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0b0b0e !important;
        color: #E3E3E8 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }
    
    /* Mobile Screen padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 6.5rem !important;
        padding-left: 0.9rem !important;
        padding-right: 0.9rem !important;
        max-width: 100% !important;
    }

    /* Top Mode Header */
    .top-pill {
        background-color: #1a1a24;
        color: #60A5FA;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 600;
        display: inline-block;
        border: 1px solid #2a2a3a;
        margin-bottom: 12px;
    }

    /* Floating Rounded Bottom Input */
    div[data-testid="stChatInput"] {
        border-radius: 28px !important;
        background-color: #1e1e28 !important;
        border: 1px solid #36364a !important;
        padding: 4px 12px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.8) !important;
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

# Chat History Memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("## ✨ Gemini Studio")
    
    # API Key Input Box
    user_api_key = st.text_input(
        "🔑 Gemini API Key dalein:",
        value="AQ.Ab8RN6KhaojI0Q2YVKIMkiNKOuYBDVa6c5N07YUUtmaq3iFXJg",
        type="password"
    )
    
    st.markdown("---")
    st.markdown("### 🧭 Mode Chunein")
    app_mode = st.radio(
        "Kiske baare mein baat karni hai:",
        [
            "💬 General Chat (Sab Kuch Pucho / Baat Karo)",
            "🎓 Students Help (Padhai, Maths, Coding)",
            "💰 Online Earning (Kamayi Ke Tarike & Roadmap)",
            "📖 Story Writer (Horror, Romance, Suspense)",
            "📱 Viral Social Media (Reels & Shorts Scripts)"
        ]
    )
    
    st.markdown("---")
    if st.button("➕ New Chat (Screen Clear Karein)", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# Top Indicator
st.markdown(f'<div class="top-pill">✨ {app_mode.split("(")[0].strip()}</div>', unsafe_allow_html=True)

# Display Messages
if len(st.session_state.chat_history) == 0:
    st.markdown("""
    <div style="text-align: center; margin-top: 16vh; color: #8F8FA0;">
        <h2 style="color: #FFFFFF; font-size: 2.2rem; margin-bottom: 6px;">Gemini</h2>
        <p style="font-size: 1rem;">Ask anything, padhai, kamayi ya kahani likhwao...</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Bottom Input
user_query = st.chat_input("Ask Gemini / Kuch bhi pucho...")

if user_query:
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        api_key = user_api_key.strip()
        if not api_key:
            err = "Kripya sidebar mein apni API key dalein."
            st.error(err)
            st.session_state.chat_history.append({"role": "assistant", "content": err})
        else:
            with st.spinner("Gemini soch raha hai..."):
                prompt = f"Mode: {app_mode}\nUser Query: {user_query}\nJawab Hinglish ya Hindi mein detailed aur helpful dein."
                
                # Check key type (Standard AIza vs REST AQ)
                if api_key.startswith("AIzaSy"):
                    try:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel("models/gemini-2.5-flash")
                        res = model.generate_content(prompt)
                        reply = res.text
                        st.markdown(reply)
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    # REST call for AQ. keys
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
                    headers = {"Content-Type": "application/json"}
                    payload = {"contents": [{"parts": [{"text": prompt}]}]}
                    try:
                        resp = requests.post(url, headers=headers, json=payload, timeout=25)
                        data = resp.json()
                        if resp.status_code == 200:
                            reply = data["candidates"][0]["content"]["parts"][0]["text"]
                            st.markdown(reply)
                            st.session_state.chat_history.append({"role": "assistant", "content": reply})
                        else:
                            err_msg = data.get("error", {}).get("message", resp.text)
                            st.error(f"API Error: {err_msg}")
                            st.session_state.chat_history.append({"role": "assistant", "content": err_msg})
                    except Exception as ex:
                        st.error(f"Network error: {ex}")
                        
