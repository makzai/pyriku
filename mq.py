import pika

credentials = pika.PlainCredentials('miffy', 'miffy')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='47.240.41.82', port=5672, credentials=credentials))
