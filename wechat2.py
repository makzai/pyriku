import itchat
import logging
import mq
import json

logger = logging.getLogger('wechat2')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./log/info.log')
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

itchat.auto_login()
author = itchat.search_chatrooms(name='【禁言】补货通知群')
if len(author) > 0:
    room = author[0]
else:
    raise RuntimeError('missing chatrooms')


def callback(ch, method, properties, body):
    info = json.loads(body)
    # print(info)
    msg = info['shop_name']+'的'+info['spu_name']+'补货啦!'+'\n'+'【规格】'+info['sku_name']+'\n'+'【货号】'+info['sku_code']
    # print(msg)
    room.send(msg)


def worker():
    # 监听数据
    logger.info('listening...')

    channel = mq.connection_init().channel()
    channel.queue_declare('miffy_queue')
    # channel.basic_consume(queue='miffy_queue', on_message_callback=callback, auto_ack=False)
    channel.basic_consume(queue='miffy_queue', on_message_callback=callback, auto_ack=True)  # 不放回
    channel.start_consuming()


worker()


