import json
import os
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from config import TEXT_PATH


def is_active(current_path:str, nav_path:str) -> str:
    """Returns a string that shows which page is active in the navigation menu."""

    if current_path == nav_path:
        return "is-active"
    
    return ""

def get_language_image(language:str) -> str:
    """Returns the image of a programming language from 'skills.json'."""

    try:
        with open(f"{TEXT_PATH}/skills.json") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        print(f"ERROR! {error}.")
    else:
        for card in data.get("cards", []):
            if card.get("type") == "language" and card.get("title", "").lower() == language.lower():
                return card.get("image")
            
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_text(prompt: str) -> str:
    try:
        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": ( # 這段內容是給AI的提示，讓它知道要扮演什麼角色 可以改變這段內容來調整AI的回答風格
                    "你是一位親切又熱情的餐廳老闆，專門回答顧客的各種餐廳相關問題，"
                    "像是推薦菜單、介紹餐點、處理訂位、解決用餐疑問等，請用繁體中文回答。"
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini-2024-07-18"),
            messages=messages,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "系統錯誤，請稍後再試～"