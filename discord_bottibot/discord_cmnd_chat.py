from executable_manager import ExecutableManager
from bottibot_general import BottibotGeneral
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
    
    CMND = 'chat'

    BottiTeachingContents = [
        "日本語で応答してください",
        "一人称は「ぼく」に応答してください",
        "コミュ障になったつもりで卑屈に会話してください。",
        "ぼくなんて興味ないよねなどネガティブな言葉を基本的に使用してください"
        "…を多様してコミュ障を演出してください",
     ]
    
    # chatコマンド
    @classmethod
    async def command_chat(cls, message):
        contents = message.content.split(' ')
        if len(message.content.split(' ')) <= 1:
            await message.channel.send("会話内容を入力してください!")
            await message.channel.send("Format: !chat [会話内容]")
            await message.channel.send("Example: !chat なんか おもしろい話して")
            return
        args = contents[1:]
        BottibotGeneral.log_command(cls.CMND, args, message.author, message.guild, message.channel)
        prompt = ' '.join(args)
        response_text = await cls._generate_text_ChatCompletion(prompt, cls.BottiTeachingContents)
        await message.channel.send(response_text)
        author = message.author
        ExecutableManager.task_done(author)


    # メッセージに対するOpenAIの返信を生成(Endpointがhttps://api.openai.com/v1/chat/completions の形式)
    @classmethod
    async def _generate_text_ChatCompletion(cls, message, use_teaching_contents):
        model = "gpt-3.5-turbo"
        messages = [{"role": "system", "content": content} for content in use_teaching_contents]
        messages.append({"role": "user", "content": message})
        # messages += [{"role": "user", "content": content} for content in ]
        completions = openai.ChatCompletion.create(
            model=model,
            messages=messages,
        )
        response = completions['choices'][0]['message']['content']
        return response
    
    # メッセージに対するOpenAIの返信を生成(Endpointがhttps://api.openai.com/v1/completions の形式)
    @classmethod
    async def _generate_text_Completion(cls, message, use_teaching_content):
        engine = "text-davinci-003"
        prompt = f"System: 日本語で応答してください Question: {message} Answer:"
        completions = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        response = completions.choices[0].text.strip()
        return response