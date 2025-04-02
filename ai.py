import requests
import re

# 🌐 Define LM Studio API endpoint
url = "http://localhost:1234/v1/chat/completions"

# 📨 Request headers
headers = {
    "Content-Type": "application/json"
}

# 🧠 Define the payload for the AI request
payload = {
    "model": "llama-3.2-3b-instruct",  # Ensure this matches your loaded model
    "messages": [
        {"role": "system", "content": "You are an AI assistant that provides clear and engaging answers with emojis for better readability."},
        {"role": "user", "content": "My plant has Potato Early Blight. What should I do?"}
    ],
    "temperature": 0.7,
    "top_p": 1
}

# 🚀 Send the request
response = requests.post(url, headers=headers, json=payload)

# 🎯 Extract and format the assistant's response
if response.status_code == 200:
    assistant_reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response received.")

    # 🌟 Dictionary of common words to emojis
    emoji_map = {
         "Plant": "🌱", "Blight": "🦠", "Fungicide": "🧪",
        "Water": "💧", "Soil": "🌿", "Temperature": "🌡", "Pest": "🐛",
        "Disease": "⚠️", "Leaves": "🍃", "Sunlight": "☀️", "Harvest": "🌾",
        "Prevention": "🛑", "Yield": "📈", "Spray": "🚿", "Weather": "⛅",
        "Resistant": "🛡", "Organic": "🌍", "Fertilizer": "🪴", "Air circulation": "🌬",
        "Chemical": "🧬", "Treatment": "💊", "Solution": "🔬", "Monitor": "📊",
        "Farm": "🚜", "Crops": "🌾", "Grow": "🌻"
    }

    # 🔄 Replace words dynamically with emojis
    for word, emoji in emoji_map.items():
        assistant_reply = re.sub(rf'\b{word}\b', f"{word} {emoji}", assistant_reply, flags=re.IGNORECASE)

    # 🎨 Add markdown-style formatting for readability
    assistant_reply = re.sub(r'(\*\*.*?\*\*)', r'🌟 \1', assistant_reply)  # Highlight bold text
    assistant_reply = re.sub(r'(\d+\.)', r'🔹 \1', assistant_reply)  # Numbered lists
    assistant_reply = assistant_reply.replace("•", "✅")  # Bullet points

    print(assistant_reply)

else:
    print(f"❌ **Error:** {response.status_code} - {response.text}")
