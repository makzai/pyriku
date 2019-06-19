import requests
import time
import datetime
import threading
import logging
import db
import pytz

# 根据SPU批量拉
shop = 'sephora'

logger = logging.getLogger(shop)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./log/info.log')
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

tz = pytz.timezone("Asia/Shanghai")

def get_data(spuCode):
    r = requests.get("https://www.sephora.com/api/users/profiles/current/product/" + spuCode)
    j = r.json()
    return j


def worker():
    logger.info('working...')
    db.cursor.execute("SELECT * FROM products WHERE shop_name = '%s' GROUP BY spu_code" % shop)
    if db.cursor.rowcount > 0:
        products = db.cursor.fetchall()
        for r in products:
            spu_code = r['spu_code']
            logger.info('handling...' + r['spu_code'])
            j = get_data(spu_code)
            print(j)
            db.cursor.execute("SELECT * FROM products WHERE shop_name = '%s' AND spu_code = '%s'" % (shop, spu_code))
            if db.cursor.rowcount > 0:
                skus = db.cursor.fetchall()
                for s in skus:
                    # currentSku
                    if j['currentSku']['skuId'] == s['sku_code']:
                        if j['currentSku']['actionFlags']['isAddToBasket']:
                            if s['stock'] == 0:
                                now = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
                                db.cursor.execute(
                                    "UPDATE products SET stock = '%s', last_stock_time = '%s' WHERE shop_name = '%s' AND spu_code = '%s' AND sku_code = '%s'" %
                                    (1, now, shop, spu_code, s['sku_code']))
                        else:
                            db.cursor.execute(
                                "UPDATE products SET value = '%s', stock = '%s' WHERE shop_name = '%s' AND spu_code = '%s' AND sku_code = '%s'" %
                                (0, 0, shop, spu_code, s['sku_code']))
                        continue

                    # regularChildSkus
                    zero = 1
                    for i in j['regularChildSkus']:
                        if i['skuId'] == s['sku_code']:
                            zero = 0
                            if i['actionFlags']['isAddToBasket']:
                                if s['stock'] == 0:
                                    now = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
                                    db.cursor.execute(
                                        "UPDATE products SET stock = '%s', last_stock_time = '%s' WHERE shop_name = '%s' AND spu_code = '%s' AND sku_code = '%s'" %
                                        (1, now, shop, spu_code, s['sku_code']))
                            break

                    # 没返回兜底stock回0
                    if zero == 1:
                        db.cursor.execute(
                            "UPDATE products SET value = '%s', stock = '%s' WHERE shop_name = '%s' AND spu_code = '%s' AND sku_code = '%s'" %
                            (0, 0, shop, spu_code, s['sku_code']))

                time.sleep(1)

    global timer
    timer = threading.Timer(60*10, worker)
    timer.start()


worker()

