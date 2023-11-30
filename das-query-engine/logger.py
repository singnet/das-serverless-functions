import logging
import os


class Logger:
    __instance = None

    @staticmethod
    def get_instance():
        if Logger.__instance is None:
            return Logger()
        return Logger.__instance

    def __init__(self):
        if Logger.__instance is not None:
            raise Exception("Invalid re-instantiation of Logger")
        else:
            logging.basicConfig(
                filename="/var/log/das/das-query-engine.log",
                level=logging.INFO,
                format="%(asctime)s %(levelname)-8s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            Logger.__instance = self

    def _prefix(self):
        return ""

    def debug(self, msg):
        logging.debug(self._prefix() + msg)

    def info(self, msg):
        logging.info(self._prefix() + msg)

    def warning(self, msg):
        logging.warning(self._prefix() + msg)

    def error(self, msg):
        logging.error(self._prefix() + msg)
