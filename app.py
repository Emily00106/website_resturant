from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    response = None
    if request.method == 'POST':
        prompt = request.form['prompt']
        # 呼叫 OpenAI API 生成回應
        response = openai.ChatCompletion.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4o-mini-2024-07-18",
            temperature=0.5,
        )
        generated_text = response['choices'][0]['message']['content'].strip()
        return render_template('about.html', response=generated_text)
    return render_template('about.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
