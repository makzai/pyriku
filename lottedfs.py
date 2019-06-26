import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import datetime
import threading
import logging
import db
import mq

# 根据SKU拉
shop = 'lottedfs'

logger = logging.getLogger(shop)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./log/info.log')
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)


def scan(prdNo, prdOptNo):
    url = 'http://chn.lottedfs.cn/kr/product/productDetailInfoAjax?prdNo='+prdNo+'&prdOptNo='+prdOptNo
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    request = urllib.request.Request(url=url, headers=headers)
    content = urllib.request.urlopen(request).read().decode('utf8')
    soup = BeautifulSoup(content, 'lxml')
    ret = soup.find('a', class_='btn1 gaEvtTg')
    if ret is not None:
        if ret.string == '立即购买':
            return True
    return False


def worker():
    logger.info('working...')
    db.cursor.execute("SELECT * FROM products WHERE shop_name = '%s' GROUP BY spu_code" % shop)
    if db.cursor.rowcount > 0:
        products = db.cursor.fetchall()
        for r in products:
            spu_code = r['spu_code']
            logger.info('handling...' + r['spu_code'])
            db.cursor.execute("SELECT * FROM products WHERE shop_name = '%s' AND spu_code = '%s'" % (shop, spu_code))
            if db.cursor.rowcount > 0:
                skus = db.cursor.fetchall()
                for s in skus:
                    if scan(s['spu_code'], s['sku_code']):
                        if s['stock'] == 0:
                            # 突然有货
                            mq.connect_and_send(s)

                            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            db.cursor.execute(
                                "UPDATE products SET stock = '%s', last_stock_time = '%s' WHERE shop_name = '%s' AND spu_code = '%s' AND sku_code = '%s'" %
                                (1, now, shop, spu_code, s['sku_code']))
                    else:
                        if s['stock'] == 1:
                            db.cursor.execute(
                                "UPDATE products SET value = '%s', stock = '%s' WHERE shop_name = '%s' AND spu_code = '%s' AND sku_code = '%s'" %
                                (0, 0, shop, spu_code, s['sku_code']))

    global timer
    timer = threading.Timer(60*3, worker)
    timer.start()


worker()
