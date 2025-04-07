import json
import os
import openai
from config import TEXT_PATH

def is_active(current_path: str, nav_path: str) -> str:
    """返回當前頁面是否為選中狀態，並將其標註為 'is-active'。"""
    return "is-active" if current_path == nav_path else ""

def get_language_image(language: str) -> str:
    """從 'skills.json' 文件中返回指定編程語言的圖片。"""
    try:
        with open(f"{TEXT_PATH}/skills.json") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        print(f"錯誤！文件未找到：{error}.")
        return None
    else:
        for card in data.get("cards", []):
            if card.get("type") == "language" and card.get("title", "").lower() == language.lower():
                return card.get("image")
    return None

# 設置 OpenAI API 金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_text(prompt: str) -> str:
    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "你是一位親切又熱情的餐廳老闆，專門回答顧客的各種餐廳相關問題，"
                    "像是推薦菜單、介紹餐點、處理訂位、解決用餐疑問等，請用繁體中文回答。"
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        # 使用 OpenAI API 生成回應（使用 chat-completion API）
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 請根據需要選擇模型版本
            messages=messages,
            temperature=0.7,
        )

        # 返回生成的訊息內容
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        print(f"OpenAI 錯誤: {e}")
        return "系統錯誤，請稍後再試～"
