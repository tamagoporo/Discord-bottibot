from logger import Logger
from executable_manager import ExecutableManager
from bottibot_general import BottibotGeneral


TAG = "[help]"

def log_e(log):
    Logger.log_e(f"{TAG} {log}")


def log_i(log):
    Logger.log_i(f"{TAG} {log}")


def log_d(log):
    Logger.log_d(f"{TAG} {log}")


class CommandHelp(object):
    
    CMND = 'help'
    
    # helloコマンド
    @classmethod
    async def command_help(cls, message):
        args = message.content.split(' ')[1:]
        BottibotGeneral.log_command(cls.CMND, args, message.author, message.guild, message.channel)
        response = ""
        response += "ぼっちぼっと使用可能コマンド一覧\n"
        response += "!msche\n"
        response += " - メッセージを送信予約します。\n"
        response += "!chat\n"
        response += " - OpenAIを使ったAIによる簡単な会話ができます。\n"
        response += "!hello\n"
        response += " - テスト用コマンド。\"Hello!\"と応答します。\n"
        response += "※ 詳しい使い方は各コマンドを実行して確認してください。"
        await message.channel.send(response)
        author = message.author
        ExecutableManager.task_done(author)
