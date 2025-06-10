import pika
import json

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"\n[WYSEFLOW] Abschlussarbeit beantragt von:")
    print(f"Name: {data['name']}")
    print(f"Matrikelnummer: {data['matrikelnummer']}")
    print(f"Studiengang: {data['studiengang']}")
    print(f"Credits: {data['credits']}")

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="wyseflow_queue")

channel.basic_consume(
    queue="wyseflow_queue",
    on_message_callback=callback,
    auto_ack=True
)

print("[WYSEFLOW] Warte auf Abschlussarbeitsanträge …")
channel.start_consuming()
