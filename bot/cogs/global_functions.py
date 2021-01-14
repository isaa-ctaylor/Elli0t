import json


def get_default_prefix():
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    
    return prefixes["default"]


def get_prefix(guild_id):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(guild_id)]


def get_cogs():
    with open("cogs.json", "r") as f:
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