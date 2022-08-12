import discord
import asyncio
import traceback
from enum import Enum

client = discord.Client()


# 起動時
@client.event
async def on_ready():
    print("ログインしたあ")


# メッセージ受信時
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if client.user in message.mentions: # botに対してメンションを付けられたかの判定
        msg = f"{message.author.mention} ぼっちでかわいそう？それ誉め言葉ね。"
        await message.channel.send(msg) # 返信メッセージを送信


# リアクション追加時に実行されるイベントハンドラ
@client.event
async def on_reaction_add(reaction, user):
    msg = f"{user.mention} 🤔"
    await reaction.message.channel.send(msg)


@client.event
async def on_voice_state_update(member, before, after):
    class State(Enum):
        JOIN = 0
        LEAVE = 1
        MOVE = 2
        OTHER = 3

    if not before.channel and after.channel:
        state = State.JOIN
    elif before.channel and not after.channel:
        state = State.LEAVE
    elif before.channel != after.channel:
        state = State.MOVE
    else:   
        state = State.OTHER
    print(before)
    print(after)
    print(member)
    print(state)


    BOT_NOTIFY_CH_NAME = "bot_notify"
    if state is State.JOIN or state is State.MOVE:
        if len(after.channel.members) == 1:
            voice_channel_cate = after.channel.category
            notify_channels = list(filter(lambda ele: ele.name == BOT_NOTIFY_CH_NAME ,voice_channel_cate.channels))
            if len(notify_channels) == 0:
                print(f"{BOT_NOTIFY_CH_NAME}がなかったからつくるよ")
                notify_channel = await voice_channel_cate.create_text_channel(BOT_NOTIFY_CH_NAME)
            else :
                print(f"{BOT_NOTIFY_CH_NAME}がすでにあったよ")
                notify_channel = notify_channels[0]
            msg = f"{notify_channel.mention} {member.name}が{voice_channel_cate.name}の{after.channel.name}で話したがってるよ"
            await notify_channel.send(msg)


def setup(ctx):
    client.run(ctx.bot_token)
