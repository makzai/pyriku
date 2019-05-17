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

cursor.execute("SELECT * FROM products")
for r in cursor:
    print(r)
cursor.close()
conn.close()
