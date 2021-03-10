import logging
import datetime
import os

dirname = os.path.dirname(__file__)


def logger_setup(bot):
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    time: datetime.datetime = datetime.datetime.now()
    time = time.strftime(r"%m%d%Y %H%M%S")
    filename = os.path.join(dirname, f'../logs/{time}.log')
    print(filename)
    open(filename, "x").close()
    handler = logging.FileHandler(
        filename=filename, encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter(
        '%(filename)s - %(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    bot.loggingfilename = filename
    return bot