from logger import Logger
from executable_manager import ExecutableManager
from bottibot_general import BottibotGeneral


TAG = "[gree]"

def log_e(log):
    Logger.log_e(f"{TAG} {log}")


def log_i(log):
    Logger.log_i(f"{TAG} {log}")


def log_d(log):
    Logger.log_d(f"{TAG} {log}")

class CommandHello(object):
    
    CMND = 'hello'
    
    # helloコマンド
    @classmethod
    async def command_hello(cls, message):
        args = message.content.split(' ')[1:]
        BottibotGeneral.log_command(cls.CMND, args, message.author, message.guild, message.channel)
        await message.channel.send('Hello!')
        author = message.author
        ExecutableManager.task_done(author)
