import pymysql
import config

db_config = {
    'host': config.configs['db']['host'],
    'port': config.configs['db']['port'],
    'user': config.configs['db']['user'],
    'passwd': config.configs['db']['password'],
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

conn = pymysql.connect(**db_config)
conn.autocommit(1)
cursor = conn.cursor()
conn.select_db(config.configs['db']['database'])
