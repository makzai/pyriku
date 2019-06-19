import itchat
import threading
import logging
import db
import datetime

interval = 1  # 频率(间隔多少分钟)
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

    # 拉数据
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # print("SELECT * FROM products WHERE last_stock_time >= DATE_ADD('%s', INTERVAL '-%s' MINUTE)" % (now, interval))
    db.cursor.execute("SELECT * FROM products WHERE last_stock_time >= DATE_ADD('%s', INTERVAL '-%s' MINUTE)" % (now, interval))
    if db.cursor.rowcount > 0:
        ps = db.cursor.fetchall()
        msg = ''
        for p in ps:
            m = p['shop_name']+'的'+p['spu_name']+' ['+p['sku_name']+'] '+'有货喇!!!'+'\n'
            msg += m

        author.send(msg)

    logger.info('nothing happen...')

    global timer
    timer = threading.Timer(60*interval, worker)
    timer.start()


worker()


