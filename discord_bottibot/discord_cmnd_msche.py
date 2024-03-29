import discord
import asyncio
import datetime
import uuid
from bottibot_general import BottibotGeneral
from bottibot_general import EmbedType
from executable_manager import ExecutableManager
from logger import Logger
from enum import Enum


TAG = "[msch]"

def log_e(log):
    Logger.log_e(f"{TAG} {log}")


def log_i(log):
    Logger.log_i(f"{TAG} {log}")


def log_d(log):
    Logger.log_d(f"{TAG} {log}")


class ScheduleMessage(object):
    def __init__(self, author, datetime, guild, message, attachments) -> None:
        self.author = author
        self.send_datetime = datetime
        self.send_guild = guild
        self.send_message = message
        self.send_attachments = attachments


class Action(Enum):
    OTHER = 0   # その他(変換失敗など)
    SEND = 1    # メッセージ送信予約
    LIST = 2    # 予約メッセージ一覧
    REMOVE = 3  # 予約メッセージ削除
    CLEAR = 4   # 予約メッセージ全削除


class CommandMsche(object):
    
    CMND = "msche"
    _message_schedule = {}
    
    # mscheコマンド
    @classmethod
    async def command_msche(cls, client, message):
        args = message.content.split(' ')[1:] # !mscheを除いた後の引数部分
        BottibotGeneral.log_command(cls.CMND, args, message.author, message.guild, message.channel)
        if type(message.channel) == discord.DMChannel:
            await cls._dm_command_msche(client, message, args)
        else:
            await cls._other_command_msche(message)
            author = message.author
            ExecutableManager.task_done(author)

    @classmethod
    async def _dm_command_msche(cls, client, message, args):
        dm_channel = message.channel
        author = message.author
        result = await cls._parse_msche_format(dm_channel, message, args)
        if not result:
            ExecutableManager.task_done(author)
            return
        action = result[0]
        if action == Action.SEND:
            await cls._msche_send(result[1], result[2], result[3], client, message, dm_channel)
        if action == Action.LIST:
            await cls._msche_list(result[1], author, dm_channel)
        if action == Action.REMOVE:
            await cls._msche_remove(result[1], author, dm_channel,)
        if action == Action.CLEAR:
            await cls._msche_clear(author, dm_channel)
    
    @classmethod
    async def _parse_msche_format(cls, dm_channel, message, args):
        if len(args) <= 0:
            await cls._help_command_msche(message.author, dm_channel)
            return None
        action = args[0]
        if action == "send":
            return await cls._parse_msche_send_format(dm_channel, message, args)
        if action == "list":
            return await cls._parse_msche_list_format(args)
        if action == "remove":
            return await cls._parse_msche_remove_format(dm_channel, args)
        if action == "clear":
            return (Action.CLEAR,)
        await cls._help_command_msche(message.author, dm_channel)
        return None

    @classmethod
    async def _parse_msche_send_format(cls, dm_channel, message, args):
        if len(args) <= 3:
            await cls._help_command_msche_send(message.author, dm_channel)
            return None
        try:
            send_datetime = datetime.datetime.strptime(f"{args[1]} {args[2]}", '%Y-%m-%d %H:%M:%S')
        except ValueError:
            await dm_channel.send(f"送信日時のフォーマットが不正です。")
            return None
        diff = (send_datetime - datetime.datetime.now()).total_seconds()
        if diff < 0:
            await dm_channel.send(f"現在時刻よりも未来の時刻を指定してください。")
            return None
        try:
            guilds_index = int(args[3])
        except ValueError:
            await dm_channel.send(f"送信可能サーバ には一覧の数値を入力してください。")
            return None
        if guilds_index < 0 or (len(message.author.mutual_guilds) - 1) < guilds_index:
            await dm_channel.send(f"送信可能サーバ 一覧の範囲外です。")
            return None
        send_guild = message.author.mutual_guilds[guilds_index]
        if len(args) <= 4:
            if len(message.attachments) == 0:
                await dm_channel.send(f"メッセージもしくは添付ファイルを指定してください。")
                return None
            return (Action.SEND, send_datetime, send_guild, None)
        return (Action.SEND, send_datetime, send_guild, ' '.join(args[4:]))

    @classmethod
    async def _parse_msche_list_format(cls, args):
        with_files = False
        if len(args) <= 1:
            return (Action.LIST, with_files)
        for arg in args[1:]:
            if arg == "--with-files" or arg == "--withfiles":
                with_files = True
        return (Action.LIST, with_files)

    @classmethod
    async def _parse_msche_remove_format(cls, dm_channel, args):
        if len(args) <= 1:
            await cls._help_command_msche_remove(dm_channel)
            return None
        return (Action.REMOVE, args[1:])

    @classmethod
    async def _msche_send(cls, send_datetime, send_guild, send_message, client, message, dm_channel):
        author = message.author
        if len([schedule_message for schedule_message in cls._message_schedule.values() if schedule_message.author == author]) >= 10:
            await dm_channel.send("メッセージ送信予約数が既に10件存在しているため、送信予約できませんでした。")
            ExecutableManager.task_done(author)
            return
        id = str(uuid.uuid4())
        schedule_message = ScheduleMessage(message.author, send_datetime, send_guild, send_message, message.attachments)
        cls._message_schedule[id] = schedule_message
        success_response = "メッセージの送信予約に成功しました。\n"
        success_response += f"送信予約メッセージID: {id}"
        await dm_channel.send(success_response)
        ExecutableManager.task_done(author)
        await cls._chk_message_schedule(client, id)

    @classmethod
    async def _chk_message_schedule(cls, client, id):
        while id in cls._message_schedule:
            await asyncio.sleep(1)
            schedule_message = cls._message_schedule.get(id)
            if not schedule_message:
                return
            send_datetime = schedule_message.send_datetime
            if datetime.datetime.now() < send_datetime:
                continue
            author = schedule_message.author
            send_message = schedule_message.send_message
            send_guild = schedule_message.send_guild
            send_channel = await BottibotGeneral.get_bottibot_notify_channel(send_guild)
            send_attachments = schedule_message.send_attachments
            send_files = [await attachment.to_file() for attachment in send_attachments]
            if send_message:
                await send_channel.send(content=send_message, embed=BottibotGeneral.create_embed(client, author, f"↑{author.name}さんからの予約メッセージ↑", EmbedType.INFO1))
            if len(send_files) != 0:
                await send_channel.send(files=send_files, embed=BottibotGeneral.create_embed(client, author, f"↑{author.name}さんからの予約添付ファイル↑", EmbedType.INFO1))
            cls._message_schedule.pop(id)

    @classmethod
    async def _msche_list(cls, with_files, author, dm_channel):
        await dm_channel.send("送信予約メッセージ一覧：")
        for key, value in cls._message_schedule.items():
            if value.author != author:
                continue
            send_datetime = value.send_datetime
            send_guild = value.send_guild
            send_message = value.send_message
            response = f"送信予約メッセージID: {key}\n"
            response += f"送信予約日程: {send_datetime}\n"
            response += f"送信先サーバ: {send_guild}\n"
            response += f"送信メッセージ: {send_message}\n"
            send_files = []
            if with_files:
                send_attachments = value.send_attachments
                for attachment in send_attachments:
                    send_files.append(await attachment.to_file())
                response += f"送信ファイル:\n"
            await dm_channel.send(response, files=send_files)
        ExecutableManager.task_done(author)

    @classmethod
    async def _msche_remove(cls, remove_ids, author, dm_channel):
        ids = [key for key, value in cls._message_schedule.items() if value.author == author]
        for remove_id in remove_ids:
            if not remove_id in ids:
                await dm_channel.send(f"送信予約メッセージID が存在しないため削除できませんでした。 ID:{remove_id}")
                continue
            cls._message_schedule.pop(remove_id)
            await dm_channel.send(f"削除に成功しました。 ID:{remove_id}")
        ExecutableManager.task_done(author)

    @classmethod
    async def _msche_clear(cls, author, dm_channel):
        ids = [key for key, value in cls._message_schedule.items() if value.author == author]
        if len(ids) == 0:
            await dm_channel.send(f"送信予約メッセージは存在しません。")
            ExecutableManager.task_done(author)
            return
        for id in ids:
            cls._message_schedule.pop(id)
            await dm_channel.send(f"削除に成功しました。 ID:{id}")
        ExecutableManager.task_done(author)

    @classmethod
    async def _other_command_msche(cls, message):
        if message.author.dm_channel == None:
            dm_channel = await message.author.create_dm()
        else:
            dm_channel = message.author.dm_channel
        await cls._help_command_msche(message.author, dm_channel)

    @classmethod
    async def _help_command_msche(cls, author, dm_channel):
        guilds = author.mutual_guilds
        response = "メッセージ送信予約をぼっちぼっとで管理します。\n"
        response += "!msche send [送信日時(yyyy-mm-dd hh:mm:ss)] [送信サーバ(0～)] [送信メッセージ]\n"
        response += " - メッセージを送信予約します。\n"
        response += "!msche list (--with-files)\n"
        response += " - 送信予約メッセージの一覧を表示します。\n"
        response += "   --with-filesオプションを付けた場合は添付ファイルも一緒に表示します。\n"
        response += "!msche remove [送信予約メッセージID]\n"
        response += " - 指定された送信予約を取り消します。\n"
        response += "!msche clear\n"
        response += " - 送信予約をすべて取り消します。\n"
        response += "送信可能サーバ 一覧：\n"
        for index, guild in enumerate(guilds):
            response += f"[{index}] {guild}\n"
        response += "※ mscheコマンドはDMチャンネルで実行してください。\n"
        response += "※ また、送信可能サーバ 一覧はサーバの入退室によって変動する可能性があります。\n"
        await dm_channel.send(response)

    @classmethod
    async def _help_command_msche_send(cls, author, dm_channel):
        guilds = author.mutual_guilds
        response = "メッセージを送信予約します。\n"
        response += "送信可能サーバ 一覧：\n"
        for index, guild in enumerate(guilds):
            response += f"[{index}] {guild}\n"
        response += "Format: !msche send [送信日時(yyyy-mm-dd hh:mm:ss)] [送信サーバ(0～)] [送信メッセージ]\n"
        response += "Example: !msche send 2023-04-01 07:00:00 0 おはようございます\n"
        response += "また、画像などのファイル(8MBまで)も一緒に添付することで送信可能です。\n"
        response += "※ mscheコマンドはDMチャンネルで実行してください。\n"
        response += "※ また、送信可能サーバ 一覧はサーバの入退室によって変動する可能性があります。\n"
        await dm_channel.send(response)

    @classmethod
    async def _help_command_msche_remove(cls, dm_channel):
        response = "指定された送信予約を取り消します。\n"
        response += "Format: !msche remove [送信予約メッセージID 1] [送信予約メッセージID 2]...\n"
        response += "Example: !msche remove de285e94-b598-11ed-ac6a-eb9c6281a21d\n"
        response += "送信予約メッセージID は!msche send コマンド成功でそのメッセージID, !msche list コマンドで一覧を確認できます。\n"
        response += "※ mscheコマンドはDMチャンネルで実行してください。\n"
        await dm_channel.send(response)
