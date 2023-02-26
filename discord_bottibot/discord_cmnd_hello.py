from logger import Logger


TAG = "[gree]"

def log_e(log):
    Logger.log_e(f"{TAG} {log}")


def log_i(log):
    Logger.log_i(f"{TAG} {log}")


def log_d(log):
    Logger.log_d(f"{TAG} {log}")

class Command_hello(object):
    # helloコマンド
    @classmethod
    async def command_hello(self, message):
        args = message.content.split(' ')[1:]
        self.log_command('hello', args, message.author, message.guild, message.channel)
        await message.channel.send('Hello!')
