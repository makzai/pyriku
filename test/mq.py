
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='47.107.118.91'))

channel = connection.channel()

channel.queue_declare("miffy_queue")

channel.basic_publish(exchange='', routing_key="miffy_queue", body="hello!")

print("send msg")

connection.close()
