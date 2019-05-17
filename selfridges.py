import requests
import pymysql

config = {
    'host': '192.168.10.10',
    'port': 3306,
    'user': 'homestead',
    'passwd': 'secret',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}
conn = pymysql.connect(**config)
conn.autocommit(1)
cursor = conn.cursor()
conn.select_db('miffy')

shop = 'selfridges'
spuCode = '456-84033258-L8453000'

headers = {'Api-Key': 'xjut2p34999bad9dx7y868ng'}
r = requests.get("https://www.selfridges.com/api/cms/ecom/v1/CN/zh/stock/byId/"+spuCode, headers=headers)
j = r.json()

for i in j['stocks']:
    cursor.execute(
        "SELECT * FROM products WHERE shop_name = '%s' AND spu_code = '%s' AND sku_code = '%s'" % (shop, spuCode, i['SKUID']))
    results = cursor.fetchall()
    print(cursor.rowcount)
    print(results)
    print(i['SKUID'])
    print(i['value'])
    print(i['Stock Quantity Available to Purchase'])


