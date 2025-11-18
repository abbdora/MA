import pika
import time

RABBIT_HOST = "51.250.26.59"
RABBIT_PORT = 5672
USERNAME = "guest"
PASSWORD = "guest123"

credentials = pika.PlainCredentials(USERNAME, PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT, credentials=credentials)
)
channel = connection.channel()

exchange_name = "ikbo-06_abarenova"
channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

queue_name = "ikbo-06_abarenova2"
channel.queue_declare(queue=queue_name)

for routing_key in ["fast", "medium", "slow"]:
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)


def process_message(channel, method, properties, body):
    message = body.decode()
    stars_count = message.count('*')

    print(f"Получено: '{message}' | Ключ: '{method.routing_key}' | Звезд: {stars_count}")

    time.sleep(stars_count)
    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=queue_name, on_message_callback=process_message, auto_ack=False)
channel.start_consuming()