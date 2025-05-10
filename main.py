import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 🔐 Configure Gemini API
API_KEY = "AIzaSyBBTNFznyQOKaD56pYb-dXxwbp8bGYOXAI"  # 🔁 Replace with your actual Gemini API key
genai.configure(api_key=API_KEY)

# 🔁 Use a powerful, fast Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# 🌍 Supported Languages
languages = {
    "English": "English",
    "Urdu": "اردو",
    "Sindhi": "سنڌي",
    "Punjabi (Shahmukhi)": "پنجابی",
    "Pashto": "پښتو",
    "Balochi": "بلوچی",
    "Siraiki": "سرائیکی",
    "Kashmiri": "كشميري",
    "Brahui": "براہوئی",
    "Gujarati": "ગુજરાતી",
    "Gilgiti": "گلگتی",
    "Balti (Skardu)": "بلتی",
    "Khowar (Chitrali)": "کهووار",
    "Shina": "شِنا",
    "Hindko": "ہندکو",
    "Potohari": "پوٹوہاری",
    "Wakhi": "وخی",
    "Torwali": "توروالی",
    "Burushaski": "بروشسکی",
}

# 🧠 Generate and translate caption
def generate_caption(image_bytes, language, context=""):
    try:
        image = Image.open(io.BytesIO(image_bytes))

        # Step 1: Generate the caption in English
        english_prompt = "Generate a vivid, emotionally engaging caption for this image in English."
        if context:
            english_prompt += f" Use this tone or style: {context.strip()}."

        english_response = model.generate_content([image, english_prompt])
        english_caption = english_response.text.strip() if english_response and english_response.text else None

        if not english_caption:
            return "⚠️ Unable to generate an English caption."

        # Step 2: Translate if needed
        if language.lower() != "english":
            translation_prompt = (
                f"Translate the following text into {language}. "
                "Respond only with the translated version. Do not explain or include any English:\n\n"
                f"{english_caption}"
            )
            translated_response = model.generate_content(translation_prompt)
            translated_caption = translated_response.text.strip() if translated_response and translated_response.text else english_caption
            return translated_caption
        else:
            return english_caption

    except Exception as e:
        return f"❌ Error: {str(e)}"

# 🚀 Streamlit App
st.set_page_config(page_title="📸 AI Image Captioning", page_icon="📸")
st.title("📸 AI-Powered Image Captioning")

# Upload UI
uploaded_image = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

# Language and style
selected_language = st.selectbox("🌍 Choose your language:", options=languages.keys())
custom_context = st.text_input("🎨 Optional: Add style (e.g., poetic, emotional, humorous)")

# Generate caption
if uploaded_image:
    st.image(uploaded_image, caption="🖼️ Uploaded Image", use_container_width=True)

    if st.button("✨ Generate Caption"):
        with st.spinner("Generating caption..."):
            image_bytes = uploaded_image.read()
            caption = generate_caption(image_bytes, languages[selected_language], custom_context)
            st.success(f"📝 Caption in {selected_language}:\n\n{caption}")

# Footer
st.markdown("---")
st.markdown("👨‍💻 **Developed by Muhammad Mudasir**")
