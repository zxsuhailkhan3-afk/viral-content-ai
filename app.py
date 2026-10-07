import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Viral Post AI", page_icon="🚀")
st.title("🚀 Viral Social Media Content Generator")

api_key = st.text_input("Apni Gemini API Key yahan dalein:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    platform = st.selectbox("Platform chunein:", ["Instagram Reels", "YouTube Shorts / Video", "Facebook Post"])
    topic = st.text_area("Aapka video ya post kis baare mein hai?")

    if st.button("Generate Karein 🔥"):
        if topic:
            prompt = f"""
            You are a top viral social media manager.
            Create high-engagement content for {platform} on topic: {topic}.

            Format:
            1. Killer Hook (Catchy opening)
            2. Script / Story outline
            3. Viral Caption
            4. 15 Trending Hashtags
            """
            with st.spinner("AI content likh raha hai..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
        else:
            st.warning("Pehle topic likhein!")
          
