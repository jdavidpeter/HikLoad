CONFIG = {
    "server": "192.168.1.69",
    "cameras": [
        "101",
        "201"
    ],
    "user": "admin",
    "password": "",
    "downloadPath": "./Downloads/"
}
import os


def getConfig(text):
    try:
        if text is "cameras":
            return os.environ["cameras"].split(' ')
        if os.environ[text]:
            return os.environ[text]
    except:
        pass
    return CONFIG[text]
