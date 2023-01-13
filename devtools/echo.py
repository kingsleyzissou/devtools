BOLD = '\033[1m'
RESET = '\033[0m'
LEVELS = {
    "OK": { "color": '\033[32m', "level": "Ok" },
    "INFO": { "color": '\033[33m', "level": "Info" },
    "ERROR": { "color": '\033[31m', "level": "Error" },
}

def __color(level):
    return LEVELS[level]['color']

def __level(level):
    return LEVELS[level]['level']

def echo(message, level = "INFO"):
    print(f"{__color(level)}{BOLD}[ {__level(level)} ]:{RESET} {message}")
