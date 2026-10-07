import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Viral Post AI", page_icon="🚀")
st.title("🚀 Viral Social Media Content Generator")

api_key = st.text_input("Apni Gemini API Key yahan dalein:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Google ke naye update ke anusaar 2.0-flash
    model = genai.GenerativeModel("gemini-3.8-flash")

    platform = st.selectbox(
        "Platform chunein:", 
        ["Instagram Reels", "YouTube Shorts", "Facebook Post", "LinkedIn"]
    )
    topic = st.text_area("Aapka video ya post kis baare mein hai?")

    if st.button("Generate Karein 🔥"):
        if topic:
            with st.spinner("AI content likh raha hai..."):
                prompt = f"""
                You are a top viral social media manager.
                Create high-engagement content for {platform} on topic: {topic}.

                Format:
                1. Killer Hook (Catchy opening)
                2. Script / Story outline
                3. Viral Caption
                4. 15 Trending Hashtags
                """
                try:
                    response = model.generate_content(prompt)
                    st.success("Aapka content ready hai!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"API Error: {e}")
        else:
            st.warning("Pehle topic likhein!")
else:
    st.info("Kripya pehle Gemini API Key dalein.")
    
