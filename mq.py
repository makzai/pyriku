import pika
import json
import jsonext
import config


def connection_init():
    credentials = pika.PlainCredentials(config.configs['mq']['user'], config.configs['mq']['password'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.configs['mq']['host'], port=config.configs['mq']['port'], credentials=credentials))
    return connection


def connect_and_send(s):
    connection = connection_init()
    channel = connection.channel()
    channel.queue_declare(config.configs['mq']['queue'])
    body = json.dumps(s, cls=jsonext.DateEncoder)
    channel.basic_publish(exchange='', routing_key=config.configs['mq']['queue'], body=body)
    connection.close()
