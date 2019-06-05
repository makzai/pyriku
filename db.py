import pymysql

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
