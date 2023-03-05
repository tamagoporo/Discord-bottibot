from logger import Logger
from enum import Enum
import discord


TAG = "[gene]"

def log_e(log):
    Logger.log_e(f"{TAG} {log}")


def log_i(log):
    Logger.log_i(f"{TAG} {log}")


def log_d(log):
    Logger.log_d(f"{TAG} {log}")


class EmbedType(Enum):
    OTHER = 0
    INFO1 = 1
    INFO2 = 2
    WARN = 3
    ERROR = 4
    CRITICAL = 5


class BottibotGeneral(object):
    @classmethod
    async def get_bottibot_notify_channel(cls, guild):
        BOT_NOTIFY_CATE_NAME = "bottibot"
        BOT_NOTIFY_CH_NAME = "bot_notify"
        bottibot_categorys = [cate for cate in guild.categories if cate.name == BOT_NOTIFY_CATE_NAME]
        if len(bottibot_categorys) == 0:
            log_i(f"Create bottibot cate {BOT_NOTIFY_CATE_NAME} in {guild}")
            cate = await guild.create_category(BOT_NOTIFY_CATE_NAME)
        else:
            cate = bottibot_categorys[0]
        notify_channels = [channel for channel in cate.channels if channel.name == BOT_NOTIFY_CH_NAME]
        if len(notify_channels) == 0:
            log_i(f"Create bottibot notify text ch {BOT_NOTIFY_CH_NAME} in {guild}")
            ch = await cate.create_text_channel(BOT_NOTIFY_CH_NAME)
        else:
            ch = notify_channels[0]
        return ch
    
    @classmethod
    def create_embed(cls, client, author, message, embed_type=EmbedType.INFO1):
        if embed_type == EmbedType.INFO1:
            color = 0x0000ff # 青
        elif embed_type == EmbedType.INFO2:
            color = 0x00ff00 # 緑
        elif embed_type == EmbedType.WARN:
            color = 0xffff00 # 黄
        elif embed_type == EmbedType.ERROR:
            color = 0xff4500 # 橙
        elif embed_type == EmbedType.CRITICAL:
            color = 0xcc0000 # 赤
        else:
            color = 0xaaaaaa # 灰
        embed = discord.Embed(title=message, color=color)
        embed.set_author(name=author, icon_url=author.avatar.url)
        embed.set_footer(text="serviced by bottibot", icon_url=client.user.avatar.url)
        return embed