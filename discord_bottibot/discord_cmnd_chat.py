from discord_cmnd_executable import CommandExecutable
import openai
from logger import Logger


TAG = "[chat]"

def log_e(log):
    Logger.log_e(f"{TAG} {log}")


def log_i(log):
    Logger.log_i(f"{TAG} {log}")


def log_d(log):
    Logger.log_d(f"{TAG} {log}")


class CommandChat(object):
    # chatコマンド
    @classmethod
    async def command_chat(self, message):
        contents = message.content.split(' ')
        if len(message.content.split(' ')) <= 1:
            await message.channel.send("会話内容を入力してください!")
            await message.channel.send("Format: !chat [会話内容]")
            await message.channel.send("Example: !chat なんか おもしろい話して")
            return
        args = contents[1:]
        self.log_command('chat', args, message.author, message.guild, message.channel)
        prompt = ' '.join(args)
        response_text = await self._generate_text(prompt)
        await message.channel.send(response_text)
        author = message.author
        CommandExecutable.command_task_done(author)


    # メッセージに対するOpenAIの返信を生成
    @classmethod
    async def _generate_text(self, message):
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