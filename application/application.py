# Sets up the routes for all the pages

from flask import Flask, render_template, request, make_response, jsonify
from flask_caching import Cache
from config import TEMPLATES_PATH, TEXT_PATH
from application.helpers import *


app = Flask(__name__, template_folder=TEMPLATES_PATH)
app.jinja_env.filters["is_active"] = is_active
app.jinja_env.filters["get_language_image"] = get_language_image

app.config["CACHE_TYPE"] = "simple"
app.config["CACHE_DEFAULT_TIMEOUT"] = 3600
cache = Cache(app)


@app.route("/")
def loading():
    """Renders the 'Loading' page of the website."""

    return render_template("home.html")


@app.route("/home")
@cache.cached()
def home():
    """Renders the 'Home' page of the website."""

    return render_template("home.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "Empty message"}), 400

    reply = generate_text(user_input)
    
    return jsonify({"reply": reply})

@app.route("/about")
@cache.cached()
def about():
    """Renders the 'About' page of the website."""
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
@cache.cached()
def contact():
    """Renders the 'Contact' page of the website."""

    # User reached route via POST
    if request.method == "POST":
        return render_template("result.html")

    # User reached route via GET
    return render_template("contact.html")


@app.route("/result")
@cache.cached()
def result():
    """Renders the 'Result' page of the website."""

    return render_template("result.html")


@app.route('/generate', methods=['POST'])
def generate():
    """生成食譜回應並顯示在 About 頁面"""
    prompt = request.form['prompt']  # 從表單獲取用戶的查詢

    # 使用 OpenAI 生成回應
    response = openai.ChatCompletion.create(
        model="gpt-4",  # 使用 GPT-4 模型，可以根據需要更改為其他模型
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,  # 控制生成文本的隨機性
    )

    # 提取生成的回應文本
    generated_text = response['choices'][0]['message']['content'].strip()

    # 返回到 About 頁面並顯示生成的回應
    return render_template('about.html', response=generated_text)

