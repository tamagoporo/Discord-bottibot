from os import getenv
from threading import Thread
import time
from flask import Flask
from dotenv import load_dotenv
import context
import bottibot
from logger import Logger


app = Flask(__name__)


@app.route('/')
def main():
    return 'Hello World!'


@app.route('/_ah/warmup')
def warmup():
    # Handle your warmup logic here, e.g. set up a database connection pool
    return '', 200, {}


def setup(ctx):
    BOT_TOKEN_KEY = "BOT_TOKEN"
    OPENAI_KEY = "OPENAI_KEY"

    load_dotenv()
    token = getenv(BOT_TOKEN_KEY) # 環境変数からトークンを取得
    if token is None:
        raise KeyError(f"{BOT_TOKEN_KEY} not defined.")
    ctx.bot_token = token
    openai_key = getenv(OPENAI_KEY)
    if openai_key is None:
        raise KeyError(f"{OPENAI_KEY} not defined.")
    ctx.openai_key = openai_key
    Logger.setup()


def start_thread():
    t = Thread(target=bottibot.run, args=(ctx, ), daemon=True)
    t.start()


if __name__ == "__main__":
    ctx = context.Context()
    setup(ctx)
    start_thread()
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080)
    while True:
        time.sleep(0.1)
    
