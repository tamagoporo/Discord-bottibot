from logger import Logger


TAG = "[gene]"

def log_e(log):
    Logger.log_e(f"{TAG} {log}")


def log_i(log):
    Logger.log_i(f"{TAG} {log}")


def log_d(log):
    Logger.log_d(f"{TAG} {log}")


class BottibotGeneral(object):
    @classmethod
    async def get_bottibot_notify_channel(self, guild):
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