import itchat
import threading
import logging
import time
import db
import datetime
import pytz

interval = 1  # 频率(间隔多少分钟)
logger = logging.getLogger('wechat')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./log/info.log')
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# itchat.auto_login()


def worker():
    logger.info('working...')
    # author = itchat.search_chatrooms(name='琪琪快乐买货宝')[0]

    # 拉数据
    tz = pytz.timezone("Asia/Shanghai")
    now = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    print(now)

    # print("SELECT * FROM products WHERE last_stock_time >= DATE_ADD('%s', INTERVAL '-%s' MINUTE)" % (now, interval))

    # db.cursor.execute("SELECT * FROM products WHERE last_stock_time >= DATE_ADD('%s', INTERVAL '-%s' MINUTE)" % (now, interval))
    # if db.cursor.rowcount > 0:
    #     products = db.cursor.fetchall()
    # print(products)

    # msg = '报时信号最后一响...现在是标准时间'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # author.send(msg)
    # global timer
    # timer = threading.Timer(60*interval, worker)
    # timer.start()


worker()


