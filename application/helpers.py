import json
import os
import openai
from openai.types.chat import ChatCompletionMessageParam
from config import TEXT_PATH

def is_active(current_path: str, nav_path: str) -> str:
    """Returns a string that shows which page is active in the navigation menu."""
    return "is-active" if current_path == nav_path else ""

def get_language_image(language: str) -> str:
    """Returns the image of a programming language from 'skills.json'."""
    try:
        with open(f"{TEXT_PATH}/skills.json") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        print(f"ERROR! {error}.")
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
        messages: list[ChatCompletionMessageParam] = [
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

        # 使用 OpenAI API 生成回應
        response = openai.ChatCompletion.create(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),  # 確保這個是有效的模型名稱
            messages=messages,
            temperature=0.7,
        )

        return response.choices[0].message["content"].strip()  # 訪問 content 的正確方式

    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "系統錯誤，請稍後再試～"
