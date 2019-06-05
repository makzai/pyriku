import itchat
import threading
import logging
import time

logger = logging.getLogger('wechat')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./log/info.log')
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

itchat.auto_login()


def worker():
    logger.info('working...')
    author = itchat.search_chatrooms(name='琪琪快乐买货宝')[0]
    msg = '报时信号最后一响...现在是标准时间'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    author.send(msg)
    global timer
    timer = threading.Timer(60*60, worker)
    timer.start()


worker()


