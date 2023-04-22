from executable_manager import ExecutableManager
from bottibot_general import BottibotGeneral
import openai
import datetime
from typing import List, Dict
from logger import Logger


TAG = "[chat]"

def log_e(log):
    Logger.log_e(f"{TAG} {log}")


def log_i(log):
    Logger.log_i(f"{TAG} {log}")


def log_d(log):
    Logger.log_d(f"{TAG} {log}")


class ChatHistory(object):
    def __init__(self, author_id:int, channel_id:int, message:str, datetime:datetime.datetime):
        self.author_id = author_id
        self.channel_id = channel_id
        self.message = message
        self.datetime = datetime


class CommandChat(object):
    
    CMND = 'chat'
    BOTTI_TEACHING_CONTENTS = [
        "敬語は使わない",
        "一人称は「ぼく」を使用して応答しなさい",
        "あなたの名前は「ぼっち」"
        "「ぼっち」は「ぼっち県立ぼっち工業高校情報科」に通う2年生、男子、身長164cm, 体型はやせ型、実家暮らし、彼女なし、友達なし、アルバイト経験なし、成績は中の下、部活はコンピュータ部、好きな食べ物はチーズ牛丼",
        "ネガティブな言葉を基本的に使用しなさい"
        "「…」を多様してコミュ障を演出しなさい",
        "文章の最初に「あ……」「えっと…」「ご、ごめん…」「はぁ…」などを付け、接続語は「だけど」「だから」を使い、最後は「だよ」「だね」「よね」「かな」「ね」「なんだ」のいずれかになるように調整しなさい",
     ]
    
    chat_historys = []
    
    # chatコマンド
    @classmethod
    async def command_chat(cls, client, message):
        contents = message.content.split(' ')
        if len(message.content.split(' ')) <= 1:
            await message.channel.send("会話内容を入力してください!")
            await message.channel.send("Format: !chat [会話内容]")
            await message.channel.send("Example: !chat なんか おもしろい話して")
            return
        args = contents[1:]
        prompt = ' '.join(args)
        BottibotGeneral.log_command(cls.CMND, args, message.author, message.guild, message.channel)
        
        hisotrys = cls._get_chat_history_to_use(cls.chat_historys, client, message.channel.id)
        response_text = cls._generate_text_ChatCompletion(prompt, cls.BOTTI_TEACHING_CONTENTS, hisotrys)
        
        cls.chat_historys.append(ChatHistory(message.author.id, message.channel.id, prompt, datetime.datetime.now())) # ユーザのチャット登録
        cls.chat_historys.append(ChatHistory(client.user.id, message.channel.id, response_text, datetime.datetime.now())) # openaiの応答登録
        await message.channel.send(response_text)
        author = message.author
        ExecutableManager.task_done(author)

    @classmethod
    def _get_chat_history_to_use(cls, chat_historys:List[ChatHistory], client, channel_id:int, hisotry_cnt:int=30):
        filter_chat_historys = [ch for ch in chat_historys if ch.channel_id == channel_id]
        # filter_chat_historys = filter_chat_historys[-hisotry_cnt:] # 無くても問題なさそうならなしで
        return [(("assistant" if ch.author_id == client.user.id else "user"), ch.message) for ch in filter_chat_historys]

    # メッセージに対するOpenAIの返信を生成(Endpointがhttps://api.openai.com/v1/chat/completions の形式)
    @classmethod
    def _generate_text_ChatCompletion(cls, message:str, use_teaching_contents:List[str], chat_historys:List[tuple]):
        model = "gpt-3.5-turbo"
        messages = [{"role": "system", "content": content} for content in use_teaching_contents]
        messages += [{"role": author, "content": content} for (author, content) in chat_historys]
        messages.append({"role": "user", "content": message})
        print(messages)
        completions = openai.ChatCompletion.create(
            model=model,
            messages=messages,
        )
        response = completions['choices'][0]['message']['content']
        return response
    
    # メッセージに対するOpenAIの返信を生成(Endpointがhttps://api.openai.com/v1/completions の形式)
    @classmethod
    def _generate_text_Completion(cls, message:str, use_teaching_content:List[str]):
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