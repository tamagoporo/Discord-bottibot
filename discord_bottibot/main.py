from os import getenv
import context
import bottibot


def setup(ctx):
    BOT_TOKEN_KEY = "BOT_TOKEN"

    token = getenv(BOT_TOKEN_KEY)
    if token is None:
        raise KeyError(f"{BOT_TOKEN} not defined.")
    ctx.set_token(token)


if __name__ == "__main__":
    ctx = context.Context()
    setup(ctx)
    bottibot.setup(ctx)
