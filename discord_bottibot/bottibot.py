import discord
import traceback
from enum import Enum
import openai
import time
import datetime
from logger import Logger
from discord_cmnd_hello import CommandHello
from discord_cmnd_chat import CommandChat
from discord_cmnd_msche import CommandMsche
from discord_cmnd_executable import CommandExecutable
from bottibot_general import BottibotGeneral
from bottibot_general import EmbedType


TAG = "[Bott]"

def log_e(log):
    Logger.log_e(f"{TAG} {log}")


def log_i(log):
    Logger.log_i(f"{TAG} {log}")


def log_d(log):
    Logger.log_d(f"{TAG} {log}")


class BottiBot(discord.Client):
    def __init__(self, intents) -> None:
        super().__init__(intents=intents)
    
    def log_command(self, command, args, user, guild, channel):
        log_i(f"{user} execute command {command} args:{args} at guild:{guild} channel:{channel}")

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
        log_i(f"user:{author} comments:{content} embeds:{','.join([embed.title for embed in embeds if embed.title])}")
        if author.bot:
            return
        command_prefix = "!"
        if content.startswith(command_prefix):
            await Command.command_process(self, message, command_prefix)

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
            notify_channels = [channel for channel in voice_channel_cate.channels if channel.name == BOT_NOTIFY_CH_NAME]
            if len(notify_channels) == 0:
                log_i(f"Create notify text ch {BOT_NOTIFY_CH_NAME} in {notify_channel.guild}")
                notify_channel = await voice_channel_cate.create_text_channel(BOT_NOTIFY_CH_NAME)
            else :
                notify_channel = notify_channels[0]
            if len(after.channel.members) == 1:
                embeds = []
                embeds.append(BottibotGeneral.create_embed(self, self.user, f"{member.name}がボイスチャットで話したがってるよ"), EmbedType.INFO1)
                await notify_channel.send(embeds=embeds)
            else:
                embeds = []
                embeds.append(BottibotGeneral.create_embed(self, self.user, f"{member.name}がボイスチャットに参加したよ"), EmbedType.INFO2)
                await notify_channel.send(embeds=embeds)


class Command(object):
    # 各コマンド処理
    @classmethod
    async def command_process(cls, client, message, command_prefix):
        author = message.author
        content = message.content
        if not CommandExecutable.chk_command_executable(author):
            command_failed_message = "別コマンド実行中のため、処理できませんでした。\n"
            command_failed_message += f"失敗コマンド：{content}"
            await message.channel.send(command_failed_message)
            return
        CommandExecutable.command_task_start(author)
        try:
            command = content.split(' ')[0]
            # helloコマンド(試験用)
            if command == f"{command_prefix}hello":
                await CommandHello.command_hello(message)
                return
            # chatコマンド
            if command == f"{command_prefix}chat":
                await CommandChat.command_chat(message)
                return
            # mscheコマンド
            if command == f"{command_prefix}msche":
                await CommandMsche().command_msche(client, message)
                return
            # TODO: Helpコマンド
        finally:
            CommandExecutable.command_task_done(author)


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
