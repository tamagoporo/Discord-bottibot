from os import getenv
from dotenv import load_dotenv
import context
import bottibot


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


if __name__ == "__main__":
    ctx = context.Context()
    setup(ctx)
    bottibot.run(ctx)
