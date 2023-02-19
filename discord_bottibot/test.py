import discord

# Discordボットのトークン
TOKEN = 'YOUR_DISCORD_BOT_TOKEN_HERE'

# Discordに接続する
client = discord.Client()

# サーバーに接続したときの処理
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

# メッセージを受け取ったときの処理
@client.event
async def on_message(message):
    # メッセージを送信したユーザーがボットの場合は、何もしない
    if message.author.bot:
        return

    # 「!hello」と入力された場合に「Hello!」を返す
    if message.content == '!hello':
        await message.channel.send('Hello!')

    # 「!ping」と入力された場合に「Pong!」を返す
    if message.content == '!ping':
        await message.channel.send('Pong!')

# ボットのトークンでDiscordに接続する
client.run(TOKEN)