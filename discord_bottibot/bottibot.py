import discord
import asyncio
import traceback



client = discord.Client()


# 起動時
@client.event
async def on_ready():
    print("ログインしたあ")


async def reply(message):
    reply = f"{message.author.mention} ぼっちでかわいそう？それ誉め言葉ね。"
    await message.channel.send(reply) # 返信メッセージを送信


# メッセージ受信時
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if client.user in message.mentions: # botに対してメンションを付けられたかの判定
        print("はなしかけられたー")
        await reply(message) # 返信する非同期関数を実行


# リアクション追加時に実行されるイベントハンドラ
@client.event
async def on_reaction_add(reaction, user):
    print("リアクションつけられたー")
    channel = client.get_channel(TEST_CHANNEL_ID)
    await channel.send('👍')


# @client.event
# async def on_message(message):
#     if message.content.startswith('$thumb'):
#         channel = message.channel
#         await channel.send('Send me that 👍 reaction, mate')

#         def check(reaction, user):
#             return user == message.author and str(reaction.emoji) == '👍'

#         try:
#             reaction, user = await client.wait_for('reaction_add', timeout=2.0, check=check)
#         except asyncio.TimeoutError:
#             await channel.send('👎')
#         else:
#             await channel.send('👍')


def setup(ctx):
    client.run(ctx.bot_token)
