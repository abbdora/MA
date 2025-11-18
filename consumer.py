import pika

RABBIT_HOST = "51.250.26.59"
RABBIT_PORT = 5672
USERNAME = "guest"
PASSWORD = "guest123"

credentials = pika.PlainCredentials(USERNAME, PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RABBIT_HOST,
        port=RABBIT_PORT,
        credentials=credentials
    )
)
channel = connection.channel()

queue_name = "ikbo-06_abarenova"
channel.queue_declare(queue=queue_name, durable=True)

print(f"Ожидаем сообщения из очереди: {queue_name}")


def process_message(channel, method, properties, body):
    print(f"ПОЛУЧЕНО: '{body.decode()}'")

    channel.basic_ack(delivery_tag=method.delivery_tag)
    print("Сообщение обработано")

channel.basic_consume(
    queue=queue_name,
    on_message_callback=process_message,
    auto_ack=False
)

channel.start_consuming()