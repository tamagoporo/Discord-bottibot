from os import getenv
import context
import bottibot
import botticommand


def setup(ctx):
    token = getenv("BOT_TOKEN")
    if token is None:
        raise KeyError("BOT_TOKEN not exist. BOT token is required")
    ctx.set_token(token)


if __name__ == "__main__":
    ctx = context.Context()
    setup(ctx)
    bottibot.setup(ctx)
    botticommand.setup(ctx)
