import pika
import json

credentials = pika.PlainCredentials('miffy', 'miffy')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='47.240.41.82', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare("miffy_queue")


d = {'shop_name': 'sephora', 'spu_name': 'muf Matte Velvet Skin Blurring Powder Foundation', 'sku_name': 'R210 - Pink Alabaster', 'sku_code': '2210060'}
body = json.dumps(d)
print(body)

channel.basic_publish(exchange='', routing_key="miffy_queue", body=body)

print("send msg")

connection.close()
