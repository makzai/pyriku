import pymysql

config = {
    'host': '47.240.41.82',
    'port': 3306,
    'user': 'root',
    'passwd': 'kkriku',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

conn = pymysql.connect(**config)
conn.autocommit(1)
cursor = conn.cursor()
conn.select_db('riku')
