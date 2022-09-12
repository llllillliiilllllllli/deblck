import logging
import sys
from Styles import Color

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
>>> Log implements Logger from logging  
>>> Log includes below logging levels
>>> funct: debug    lvl: DEBUG    val: 10
>>> funct: info     lvl: INFO     val: 20
>>> funct: warning  lvl: WARNING  val: 30
>>> funct: error    lvl: ERROR    val: 40
>>> funct: critical lvl: CRITICAL val: 50 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

logger = logging.Logger("log", logging.DEBUG)

formatter = logging.Formatter(
    fmt="\n%(asctime)s | %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S")

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

def debug(msg:str):
    return logger.debug(f"{Color.Yellow}DEBUG{Color.Reset} | {msg}")

def info(msg:str):
    return logger.info(f"{Color.Blue}INFO{Color.Reset}  | {msg}")

def warning(msg:str):
    return logger.warning(f"{Color.Magenta}WARNING{Color.Reset} | {msg}")

def error(msg:str):
    return logger.error(f"{Color.Red}ERROR{Color.Reset} | {msg}")

def critical(msg:str):
    return logger.critical(f"{Color.Black}CRITICAL{Color.Reset} | {msg}")
