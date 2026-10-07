import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Viral Post AI", page_icon="🚀")
st.title("🚀 Viral Social Media Content Generator")

api_key = st.text_input("Apni Gemini API Key yahan dalein:", type="password")

if api_key:
    genai.configure(api_key=api_key)

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
                    # Auto-detect supported model from your account
                    available_models = [
                        m.name for m in genai.list_models() 
                        if "generateContent" in m.supported_generation_methods
                    ]
                    
                    # Target flash first, otherwise take the first supported model
                    chosen_model = None
                    for m in available_models:
                        if "flash" in m:
                            chosen_model = m
                            break
                    if not chosen_model and available_models:
                        chosen_model = available_models[0]

                    if not chosen_model:
                        st.error("Aapke account par koi generateContent model nahi mila.")
                    else:
                        model = genai.GenerativeModel(chosen_model)
                        response = model.generate_content(prompt)
                        st.success(f"Content taiyaar hai! (Model: {chosen_model})")
                        st.markdown(response.text)
                except Exception as e:
                    st.error(f"API Error: {e}")
        else:
            st.warning("Pehle topic likhein!")
else:
    st.info("Kripya pehle Gemini API Key dalein.")
    
