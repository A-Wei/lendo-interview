import pika
import json


async def rmq_client(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue='lendo_queue')
    channel.basic_publish(
        exchange="",
        routing_key="lendo_queue",
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )
    print("message: ", message)

    connection.close()
