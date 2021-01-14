import json

def get_default_prefix():
    '''
    Returns the default prefix
    '''
    with open('/media/Elli0t/Elli0t/bot/json/data.json', 'r') as f:
        prefixes = json.load(f)
    
    return prefixes["defaults"]["prefix"]


def get_prefix(bot, message):
    '''
    Returns the prefix for the given guild
    '''
    with open('/media/Elli0t/Elli0t/bot/json/data.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes["servers"][str(message.guild.id)]["prefix"]


def get_cogs():
    with open("/media/Elli0t/Elli0t/bot/json/cogs.json", "r") as f:
        cogs = json.load(f)

    return cogs


def timeInSeconds(timeout):
    parts = timeout.split(" ")
    sleep = 0

    for i in parts:
        value = int(i[0:len(i)-1])
        period = i[len(i)-1:].lower()
        if period == "d":
            sleep += value * 24 * 60 * 60
        elif period == "h":
            sleep += value * 60 * 60
        elif period == "m":
            sleep += value * 60
        elif period == "s":
            sleep += value
        else:
            raise ValueError(
                "Please specify duration in a valid format, example: 1d 6h 7m 2s")
            
    return sleep