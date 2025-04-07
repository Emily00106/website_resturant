這邊我改動了把skill跟portfolio給刪除了，還有更改contact、about的頁面讓他更像餐廳，還有home.html我把羅博寫的全改掉，變成顯示一個餐廳的背景在此之上進行描述，這邊的樣式可以參考 'application/static/css/home.css'。
主要整合openai的部分在 'application/helpers.py' 的 generate_text 可以改的地方有我註解的部分: content，可以改成你喜歡的提示詞。
網頁的部分則是在 'application/templates/layout.html' 的 <div id="chatbot-toggle">💬</div> 部分，我有寫JavaScript來控制網頁的動畫，還有 'application/static/css/chatbot.css' 來自訂他的樣式。
我有標上中文註解的就是可以改動的