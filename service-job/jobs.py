import pika
import sys
import os
import json
import threading
from retry import retry
import requests


class StatusException(Exception):
    pass


def rmq_client(message, queue_name, exchange=''):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(
        exchange=exchange,
        routing_key=str(queue_name),
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )

    connection.close()


@retry(delay=5, tries=6)
def application_evaluate(message_body):
    message = json.loads(message_body)
    print(f"[x] Message received from lendo queue {message}")

    bank_resp = requests.post(url="http://bank_partner_api:8000/api/applications", json=message)
    resp_json = bank_resp.json()
    print(f"[x] Response from bank partner api {resp_json}")

    print("[x] Sending response to bank queue")
    resp_json["application_id"] = resp_json["id"]
    rmq_client(message=resp_json, queue_name="bank_queue")


@retry(StatusException, delay=10, tries=6)
def application_check_status(message_body):
    message = json.loads(message_body)
    print(f"[x] Received from bank queue {message}")

    bank_resp = requests.get(
        url=f"http://bank_partner_api:8000/api/jobs?application_id={message['application_id']}"
    )
    resp_json = bank_resp.json()
    print(f"[x] Response from bank partner api {resp_json}")

    if resp_json["status"] == "pending":
        print("[x] Application still pending")
        raise StatusException

    elif resp_json["status"]:
        print(f"[x] Application {resp_json['status']}")
        print(type(resp_json))
        print(resp_json)
        service_resp = requests.put(
            url=f"http://service-application:8001/application/{resp_json['application_id']}",
            json=resp_json
        )

    if service_resp.status_code != 200:
        print("Update application status failed")
        print(service_resp.json())


class Consumer(threading.Thread):
    def __init__(self, queue_name, function):
        threading.Thread.__init__(self)
        parameters = pika.ConnectionParameters(host='rabbitmq')
        connection = pika.BlockingConnection(parameters)
        self.queue_name = queue_name
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback,
            auto_ack=True
        )
        self.function = function

    def callback(self, channel, method, properties, body):
        self.function(body)

    def run(self):
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback,
            auto_ack=True
        )

        print(f'[*] {self.queue_name} Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()


if __name__ == '__main__':
    try:
        threads = [
            Consumer("lendo_queue", application_evaluate),
            Consumer("bank_queue", application_check_status)
        ]
        for thread in threads:
            thread.start()

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os.exit(0)
            