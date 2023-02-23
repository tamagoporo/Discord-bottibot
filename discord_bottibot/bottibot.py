import discord
import asyncio
import traceback
from enum import Enum
import openai
import datetime
from logger import Logger


TAG = "[Bott]"

def log_e(log):
    Logger.log_e(f"{self.TAG} {log}")


def log_i(log):
    Logger.log_i(f"{TAG} {log}")


def log_d(log):
    Logger.log_d(f"{TAG} {log}")


class BottiBot(discord.Client):
    def log_command(self, command, args, user):
        log_i(f"{user} executing {command} {' '.join(args)}")

    # 起動時
    async def on_ready(self):
        log_i("--------------------")
        log_i(f"bottibot user: {self.user.name}")
        log_i(f"bottibot id  : {self.user.id}")
        log_i("--------------------")
        log_i("Ready bottibot!")

    # メッセージ受信時
    async def on_message(self, message):
        author = message.author
        content = message.content
        embeds = message.embeds
        embeds_desc = [embed.description for embed in message.embeds]
        log_i(f"user:{author} comments:{content} embeds:{','.join([embed.description for embed in embeds])}")
        if author.bot:
            return
        command = content.split(' ')[0]
        command_prefix = "!"
        if content.startswith(f"{command_prefix}chat"):
            await self.command_chat(message)
            return
        if content.startswith(f"{command_prefix}hello"):
            await self.command_hello(message)

    async def command_chat(self, message):
        contents = message.content.split(' ')
        if len(message.content.split(' ')) <= 1:
            await message.channel.send("会話内容を入力してください!")
            await message.channel.send("Format: !chat [会話内容]")
            await message.channel.send("HowUse: !chat \"なんか おもしろい話して\"")
            return
        args = contents[1:]
        self.log_command('chat', args, message.author)
        prompt = ' '.join(args)
        response_text = await self.generate_text(prompt)
        await message.channel.send(response_text)

    async def command_hello(self, message):
        args = message.content.split(' ')[1:]
        self.log_command('hello', args, message.author)
        await message.channel.send('Hello!')

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
        log_d(f"before: {before}")
        log_d(f"after: {after}")
        log_d(f"member: {member}")
        log_d(f"state: {state}")

        BOT_NOTIFY_CH_NAME = "bot_notify"
        if state == State.JOIN or state == State.MOVE:
            voice_channel_cate = after.channel.category
            notify_channels = list(filter(lambda ele: ele.name == BOT_NOTIFY_CH_NAME ,voice_channel_cate.channels))
            if len(notify_channels) == 0:
                log_i(f"Create text ch {BOT_NOTIFY_CH_NAME}")
                notify_channel = await voice_channel_cate.create_text_channel(BOT_NOTIFY_CH_NAME)
            else :
                notify_channel = notify_channels[0]
            if len(after.channel.members) == 1:
                embeds = []
                embeds.append(discord.Embed(
                    color=0x0000ff, 
                    description=f"{member.name}がボイスチャットで話したがってるよ",
                    ))
                await notify_channel.send(embeds=embeds)
            else:
                embeds = []
                embeds.append(discord.Embed(
                    color=0x00ff00, 
                    description=f"{member.name}がボイスチャットに参加したよ",
                    )) 
                await notify_channel.send(embeds=embeds)

    # メッセージに対するOpenAIの返信を生成
    async def generate_text(self, message):
        model_engine = "text-davinci-002"
        completions = openai.Completion.create(
            engine=model_engine,
            prompt=f"Question: {message} Answer:",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        response = completions.choices[0].text.strip()
        return response


def setup(ctx):
    openai.api_key = ctx.openai_key


def run(ctx):
    log_i("Starting Bottibot")
    setup(ctx)
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bottibot = BottiBot(intents=intents)
    bottibot.run(ctx.bot_token)
