import requests
import datetime
import threading
import logging
import db
import mq

# 根据SPU批量拉
shop = 'selfridges'

logger = logging.getLogger(shop)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./log/info.log')
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)


def get_data(spu_code):
    headers = {'Api-Key': 'xjut2p34999bad9dx7y868ng'}
    try:
        r = requests.get("https://www.selfridges.com/api/cms/ecom/v1/GB/en/stock/byId/" + spu_code, timeout=5, headers=headers)

        # http状态
        if r.status_code != requests.codes.ok:
            logger.error(spu_code+" request status code:%s" % r.status_code)
            return {}

        j = r.json()
        # 接口错误
        # if 'errorCode' in j.keys():
        #     logger.error(spu_code+" error code:%s" % j['errorCode'])
        #     return {}

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
                    set_zero = 1
                    # stocks
                    if 'stocks' in j.keys():
                        for i in j['stocks']:
                            if i['SKUID'] == s['sku_code']:
                                set_zero = 0
                                if int(i['Stock Quantity Available to Purchase']) > 0:
                                    if s['stock'] == 0:
                                        # 突然有货
                                        mq.connect_and_send(s)

                                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        db.cursor.execute(
                                            "UPDATE products SET value = '%s', stock = '%s', last_stock_time = '%s' WHERE shop_name = '%s' AND spu_code = '%s' AND sku_code = '%s'" %
                                            (i['Stock Quantity Available to Purchase'], 1, now, shop, spu_code,
                                             s['sku_code']))
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
    timer = threading.Timer(60*10, worker)
    timer.start()


worker()

