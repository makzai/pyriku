import requests
import datetime
import threading
import logging
import db
import pytz
import mq
import json
import jsonext

# 根据SPU批量拉
shop = 'sephora'

logger = logging.getLogger(shop)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./log/info.log')
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

tz = pytz.timezone("Asia/Shanghai")

channel = mq.connection.channel()
channel.queue_declare('miffy_queue')
exchange = ''
routing_key = 'miffy_queue'


def get_data(spuCode):
    try:
        r = requests.get("https://www.sephora.com/api/users/profiles/current/product/" + spuCode, timeout=5)
        # http状态
        if r.status_code != requests.codes.ok:
            logger.error(spuCode+" request status code:%s" % r.status_code)
            return {}

        j = r.json()
        # 接口错误
        if 'errorCode' in j.keys():
            logger.error(spuCode+" error code:%s" % j['errorCode'])
            return {}

        return j
    except requests.exceptions.RequestException as e:
        logger.error(e)
        return {}


def worker():
    logger.info('working...')
    db.cursor.execute("SELECT * FROM products WHERE shop_name = '%s' GROUP BY spu_code" % shop)
    if db.cursor.rowcount > 0:
        products = db.cursor.fetchall()
        for r in products:
            spu_code = r['spu_code']
            logger.info('handling...' + r['spu_code'])
            j = get_data(spu_code)
            if len(j) == 0:
                logger.info('err in ' + r['spu_code'])
                continue
            # print(j)
            db.cursor.execute("SELECT * FROM products WHERE shop_name = '%s' AND spu_code = '%s'" % (shop, spu_code))
            if db.cursor.rowcount > 0:
                skus = db.cursor.fetchall()
                for s in skus:
                    # currentSku
                    if 'currentSku' in j.keys():
                        if j['currentSku']['skuId'] == s['sku_code']:
                            if j['currentSku']['actionFlags']['isAddToBasket']:
                                if s['stock'] == 0:
                                    # 突然有货
                                    body = json.dumps(s, cls=jsonext.DateEncoder)
                                    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body)

                                    now = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
                                    db.cursor.execute(
                                        "UPDATE products SET stock = '%s', last_stock_time = '%s' WHERE shop_name = '%s' AND spu_code = '%s' AND sku_code = '%s'" %
                                        (1, now, shop, spu_code, s['sku_code']))
                            else:
                                if s['stock'] == 1:
                                    db.cursor.execute(
                                        "UPDATE products SET value = '%s', stock = '%s' WHERE shop_name = '%s' AND spu_code = '%s' AND sku_code = '%s'" %
                                        (0, 0, shop, spu_code, s['sku_code']))
                            continue

                    set_zero = 1
                    # regularChildSkus
                    if 'regularChildSkus' in j.keys():
                        for i in j['regularChildSkus']:
                            if i['skuId'] == s['sku_code']:
                                set_zero = 0
                                if i['actionFlags']['isAddToBasket']:
                                    if s['stock'] == 0:
                                        # 突然有货
                                        body = json.dumps(s, cls=jsonext.DateEncoder)
                                        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body)

                                        now = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
                                        db.cursor.execute(
                                            "UPDATE products SET stock = '%s', last_stock_time = '%s' WHERE shop_name = '%s' AND spu_code = '%s' AND sku_code = '%s'" %
                                            (1, now, shop, spu_code, s['sku_code']))
                                else:
                                    if s['stock'] == 1:
                                        db.cursor.execute(
                                            "UPDATE products SET value = '%s', stock = '%s' WHERE shop_name = '%s' AND spu_code = '%s' AND sku_code = '%s'" %
                                            (0, 0, shop, spu_code, s['sku_code']))
                                break

                    # 没返回兜底stock回0
                    if set_zero == 1:
                        if s['stock'] == 1:
                            db.cursor.execute(
                                "UPDATE products SET value = '%s', stock = '%s' WHERE shop_name = '%s' AND spu_code = '%s' AND sku_code = '%s'" %
                                (0, 0, shop, spu_code, s['sku_code']))

    global timer
    timer = threading.Timer(60*3, worker)
    timer.start()


worker()

