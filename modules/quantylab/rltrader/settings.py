import os
import locale
import platform


# 로거 이름
LOGGER_NAME = 'rltrader'


# 경로 설정
BASE_DIR = "/app"


# 로케일 설정
if 'Linux' in platform.system() or 'Darwin' in platform.system():
    locale.setlocale(locale.LC_ALL, '')
elif 'Windows' in platform.system():
    locale.setlocale(locale.LC_ALL, '')
