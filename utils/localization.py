from urllib.request import Request
from core.config import config


def getValueByKey(dic: dict, path: str):
    keys = path.split('.')
    val = dic
    for key in keys:
        if key in val:
            val = val[key]
        else:
            return path
    return val


def getText(language: str, path: str):
    if language not in config.language.LANGUAGES:
        language = config.language.DEFAULT
    return getValueByKey(config.language.LANGUAGES[language], path)


def _(req: Request, path: str):
    return getText(req.state.language, path)