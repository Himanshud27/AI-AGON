import streamlit as st
import requests
import re
from PIL import Image
import numpy as np
from paddleocr import PaddleOCR
from keras.models import load_model
import tempfile
from datetime import datetime


fruit_model = load_model('fruit_classifier_model.h5')


fruit_class_mapping = {
    0: "Fresh Apples ",
    1: "Fresh Bananas ",
    2: "Fresh Oranges ",
    3: "Rotten Apples ",
    4: "Rotten Bananas ",
    5: "Rotten Oranges "
}


LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"



emoji_map = {
    "Plant": "🌱", "Blight": "🦠", "Fungicide": "🧪",
    "Soil": "🌿", "Temperature": "🌡", "Pest": "🐛",
    "Disease": "⚠️", "Leaves": "🍃", "Sunlight": "☀️", "Harvest": "🌾",
    "Prevention": "🛑", "Yield": "📈", "Spray": "🚿", "Weather": "⛅",
    "Resistant": "🛡", "Organic": "🌍", "Fertilizer": "🪴", "Air circulation": "🌬",
    "Chemical": "🧬", "Treatment": "💊", "Solution": "🔬", "Monitor": "📊",
    "Farm": "🚜", "Crops": "🌾", "Grow": "🌻"
}


def format_response(response_text):
    """Enhance AI response with emojis and markdown formatting."""
    for word, emoji in emoji_map.items():
        response_text = re.sub(rf'\b{word}\b', f"{word} {emoji}", response_text, flags=re.IGNORECASE)
        
    response_text = re.sub(r'(\d+\.)', r'\n \1', response_text)
    response_text = re.sub(r'(\d+\.)', r'🔹 \1', response_text)  
    response_text = re.sub(r'(\*\*.*?\*\*)', r'🌟 \1', response_text)  # Highlight bold text
    response_text = response_text.replace("•", "✅")  # Bullet points

    return response_text


def get_ai_response(user_query):
    payload = {
        "model": "llama-3.1-natural-farmer",
        "messages": [
            {"role": "system", "content": "You are an AI assistant that provides clear, engaging answers with emojis and give answere professionally dont show your emotions and dont give greetings answere language english."},
            {"role": "user", "content": user_query}
        ],
        "temperature": 0.7,
        "top_p": 1
    }
    
    response = requests.post(LM_STUDIO_URL, json=payload)
    
    if response.status_code == 200:
        assistant_reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
        return format_response(assistant_reply)
    
    return f"❌ **Error fetching AI response:** {response.status_code} - {response.text}"


def preprocess_image(image):
    image = image.convert('RGB')
    image = image.resize((100, 100))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

def predict_fruit(image):
    processed_image = preprocess_image(image)
    prediction = fruit_model.predict(processed_image)
    predicted_class_index = np.argmax(prediction, axis=1)[0]
    return fruit_class_mapping[predicted_class_index]



st.title("Krishi Mitra - Your AI Farming Assistant")
st.sidebar.title("🛠 Model Selection")
models = ["Krishi AI", "Fruit Vision"]
selected_model = st.sidebar.selectbox("🔍 Select a Model:", models)


def upload_image():
    uploaded_file = st.file_uploader("📷 Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='🖼 Uploaded Image', use_column_width=True)
        return image
    return None


def save_results_to_file(results_str):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results_with_date = f"📅 Results generated on: {current_time}\n\n{results_str}"
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmpfile:
        tmpfile.write(results_with_date.encode())
        tmpfile.close()
        return tmpfile.name


if selected_model == "Krishi AI":
    st.write("### Krishi AI")
    City_list = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata","Pune", "Hyderabad", "Ahmedabad", "Jaipur", "Lucknow"]
    selected_city = st.text_input("🏙️ Enter your city :")
    weather = st.number_input("🌡️ Enter the temperature in Celsius:")
    humidity = st.number_input(" Enter the humidity in percentage:")
    crop = st.text_input("🌾 Enter the crop name:")

    user_query = f"I live have a farm in {selected_city} and the temperature is {weather}°C and the humidty is {humidity}%. I have {crop} crop. how to make higher yeild in this and which diseases the crop can have how to cure them and which fertilizer to be used?"
    
    if st.button("🚀 Get AI Response"):
        if user_query.strip():
            ai_response = get_ai_response(user_query)
            st.markdown(ai_response, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter a query.")




elif selected_model == "Fruit Vision":
    st.write("###  Fruit Vision")
    image = upload_image()
    
    if image:
        prediction = predict_fruit(image)
        st.write(f"🔍 **Detected:** {prediction}")
