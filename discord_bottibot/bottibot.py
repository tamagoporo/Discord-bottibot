import discord
import asyncio
import traceback
from enum import Enum
import openai


class BottiClient(discord.Client):
    # 起動時
    async def on_ready(self):
        print("じゅんびかんりょー")

    # メッセージ受信時
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith("!chat"): # ぼっととの会話用分岐
            prompt = message.content[5:]
            response_text = await self.generate_text(prompt)
            await message.channel.send(response_text)

    # リアクション追加時に実行されるイベントハンドラ
    async def on_reaction_add(self, reaction, user):
        pass

    # ボイスステートが更新されたときに実行されるイベントハンドラ
    async def on_voice_state_update(self, member, before, after):
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
            voice_channel_cate = after.channel.category
            notify_channels = list(filter(lambda ele: ele.name == BOT_NOTIFY_CH_NAME ,voice_channel_cate.channels))
            if len(notify_channels) == 0:
                print(f"{BOT_NOTIFY_CH_NAME}がなかったからつくるよ")
                notify_channel = await voice_channel_cate.create_text_channel(BOT_NOTIFY_CH_NAME)
            else :
                print(f"{BOT_NOTIFY_CH_NAME}がすでにあったよ")
                notify_channel = notify_channels[0]
            if len(after.channel.members) == 1:
                embed = discord.Embed(
                    color=0x0000ff, 
                    description=f"{member.name}がボイスチャットで話したがってるよ",
                    )
                await notify_channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    color=0x00ff00, 
                    description=f"{member.name}がボイスチャットに参加したよ",
                    )
                await notify_channel.send(embed=embed)
    
    # メッセージに対するOpenAIの返信を生成
    async def generate_text(self, prompt):
        print(prompt)
        model_engine = "text-davinci-002"
        completions = openai.Completion.create(
            engine=model_engine,
            prompt=f"Question: {prompt} Answer:",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        message = completions.choices[0].text.strip()
        return message


def setup(ctx):
    openai.api_key = ctx.openai_key


def run(ctx):
    setup(ctx)
    intents = discord.Intents.default()
    intents.message_content = True
    client = BottiClient(intents=intents)
    client.run(ctx.bot_token)
