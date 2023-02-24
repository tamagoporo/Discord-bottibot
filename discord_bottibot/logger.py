import logging
import os
import sys
from enum import Enum
import google.cloud.logging


class LogOutputType(Enum):
    STDOUT = 1
    GOOGLE = 2


class Logger(object):
    def __init__(self):
        self._logger = None
        
    @classmethod
    def setup(self):
        
        log_output_type = LogOutputType.GOOGLE

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

        # ロガーを作成
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        self._logger = logger

        if log_output_type == LogOutputType.STDOUT:
            self._setup_stdout_logging(logger)
            return
        if log_output_type == LogOutputType.GOOGLE:
            self._setup_google_logging()
            return

    # 標準出力用ハンドラの作成
    def _setup_stdout_logging(logger):
        LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S'))
        logger.addHandler(stdout_handler)

    # 標準のloggingモジュールにgoogle.loggingを統合
    def _setup_google_logging():
        client = google.cloud.logging.Client()
        client.setup_logging()

    @classmethod
    def log_e(self, log):
        self._logger.error(log)

    @classmethod
    def log_i(self, log):
        self._logger.info(log)

    @classmethod
    def log_d(self, log):
        self._logger.debug(log)
