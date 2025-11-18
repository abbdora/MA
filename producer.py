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

messages = [
    {"routing_key": "fast", "message": "Быстрая задача"},
    {"routing_key": "medium", "message": "Средняя задача **"},
    {"routing_key": "slow", "message": "Медленная задача *****"},
]

for msg in messages:
    channel.basic_publish(
        exchange=exchange_name,
        routing_key=msg["routing_key"],
        body=msg["message"]
    )
    print(f"Отправлено: '{msg['message']}'")
    time.sleep(0.5)

connection.close()