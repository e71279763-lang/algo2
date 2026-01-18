from flask import Flask, render_template_string
import requests
import datetime
import random

app = Flask(__name__)

# Время запуска сервера
start_time = datetime.datetime.now()

@app.route('/')
def home():
    # 1. Пытаемся получить случайный факт из интернета
    try:
        response = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
        fact = response.json().get('text', 'No facts available today.')
    except:
        fact = "Internet connection stable, but facts database is silent."

    # 2. Считаем, сколько времени работает сервер
    uptime = datetime.datetime.now() - start_time
    uptime_str = str(uptime).split('.')[0]  # Убираем миллисекунды

    # 3. HTML-код страницы (CSS внутри, чтобы был всего один файл)
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mission Control</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                background-color: #0d1117;
                color: #00ff41;
                font-family: 'Courier New', Courier, monospace;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                text-align: center;
            }
            .container {
                border: 2px solid #00ff41;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
                max-width: 90%;
            }
            h1 { text-transform: uppercase; letter-spacing: 5px; margin-bottom: 5px; }
            .status { color: #ff0055; font-weight: bold; }
            .fact-box {
                margin-top: 20px;
                padding: 15px;
                border-top: 1px dashed #00ff41;
                font-style: italic;
                color: #e6edf3;
            }
            .uptime { font-size: 0.8em; color: #8b949e; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>System Online</h1>
            <p>Deploy Status: <span class="status">SUCCESS [200 OK]</span></p>
            
            <div class="fact-box">
                "{{ fact }}"
            </div>

            <p class="uptime">Server Uptime: {{ uptime }}</p>
        </div>
    </body>
    </html>
    """
    # Рендерим шаблон, вставляя в него факт и время
    return render_template_string(html_code, fact=fact, uptime=uptime_str)

if __name__ == '__main__':
    # Важно: host='0.0.0.0' делает сервер доступным из интернета
    # port=10000 — стандартный порт для Render
    app.run(host='0.0.0.0', port=10000)