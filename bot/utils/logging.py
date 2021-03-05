import logging

def logger_setup():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(
        filename='/media/Elli0t/Elli0t/bot/logs/latest.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter(
        '%(filename)s - %(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
