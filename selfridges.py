import requests
import pymysql
import time
import datetime
import threading
import logging

config = {
    'host': '47.103.20.2',
    'port': 3306,
    'user': 'riku',
    'passwd': 'riku0806',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

conn = pymysql.connect(**config)
conn.autocommit(1)
cursor = conn.cursor()
conn.select_db('riku')

# 根据SPU批量拉
shop = 'selfridges'


def get_data(spuCode):
    headers = {'Api-Key': 'xjut2p34999bad9dx7y868ng'}
    r = requests.get("https://www.selfridges.com/api/cms/ecom/v1/CN/zh/stock/byId/" + spuCode, headers=headers)
    j = r.json()
    return j


def worker():
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('./log/info.log')
    logger.addHandler(fh)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.info('working...')
    cursor.execute("SELECT * FROM products WHERE shop_name = '%s' GROUP BY spu_code" % shop)
    if cursor.rowcount > 0:
        results = cursor.fetchall()
        for r in results:
            spuCode = r['spu_code']
            print(spuCode)
            j = get_data(spuCode)
            for i in j['stocks']:
                print('SKUID:'+i['SKUID']+' , STOCK:'+i['Stock Quantity Available to Purchase'])
                if int(i['Stock Quantity Available to Purchase']) > 0:
                    cursor.execute("SELECT * FROM products WHERE shop_name = '%s' AND spu_code = '%s' AND sku_code = '%s' LIMIT 1" % (shop, spuCode, i['SKUID']))
                    if cursor.rowcount > 0:
                        result = cursor.fetchone()
                        if result['stock'] == 0:
                            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            cursor.execute(
                                "UPDATE products SET value = '%s', stock = '%s', last_stock_time = '%s' WHERE shop_name = '%s' AND spu_code = '%s' AND sku_code = '%s' LIMIT 1" %
                                (i['Stock Quantity Available to Purchase'], 1, now, shop, spuCode, i['SKUID']))
                        else:
                            cursor.execute(
                                "UPDATE products SET value = '%s' WHERE shop_name = '%s' AND spu_code = '%s' AND sku_code = '%s' LIMIT 1" %
                                (i['Stock Quantity Available to Purchase'], shop, spuCode, i['SKUID']))
                time.sleep(0.1)
        time.sleep(1)

    global timer
    timer = threading.Timer(60*1, worker)
    timer.start()


worker()

