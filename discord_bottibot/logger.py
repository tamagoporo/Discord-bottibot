import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys


class Logger(object):
    def __init__(self):
        self._logger = None
        
    @classmethod
    def setup(self):
        # ログのフォーマットを設定
        LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"

        # ログファイル名を指定
        LOG_FILE = "./log/bottibot.log"
        LOG_DIR = os.path.dirname(LOG_FILE)
        if not os.path.isdir(LOG_DIR):
            os.makedirs(LOG_DIR)

        # ログレベルの名前を3文字の略語に設定
        logging.addLevelName(logging.DEBUG, "DBG")
        logging.addLevelName(logging.INFO, "INF")
        logging.addLevelName(logging.WARNING, "WRN")
        logging.addLevelName(logging.ERROR, "ERR")
        logging.addLevelName(logging.CRITICAL, "CRT")

        # ログファイル出力(ローテーション)用ハンドラの作成
        rotation_file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight", interval=1, backupCount=7)
        rotation_file_handler.suffix="_%Y%m%d.log"
        rotation_file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S'))

        # 標準出力用ハンドラの作成
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S'))

        # ロガーを作成
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger.addHandler(rotation_file_handler)
        logger.addHandler(stdout_handler)
        self._logger = logger

    @classmethod
    def log_e(self, log):
        self._logger.error(log)

    @classmethod
    def log_i(self, log):
        self._logger.info(log)

    @classmethod
    def log_d(self, log):
        self._logger.debug(log)
