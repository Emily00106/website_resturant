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

@app.route("/about", methods=["GET", "POST"])
@cache.cached()
def about():
    """Renders the 'About' page with recipe search functionality."""

    # 處理 POST 請求
    if request.method == "POST":
        prompt = request.form["prompt"]
        response = generate_text(prompt)  # 呼叫生成文字的函數
        return render_template("about.html", response=response)  # 將生成的回應顯示在頁面上

    # 預設的 GET 請求，顯示普通的 about 頁面
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
