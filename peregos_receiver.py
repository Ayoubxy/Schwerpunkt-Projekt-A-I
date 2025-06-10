import pika
import json

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"\n[PEREGOS] Antrag erhalten vom Studenten:")
    print(f"Name: {data['name']}")
    print(f"Matrikelnummer: {data['matrikelnummer']}")
    print(f"Studiengang: {data['studiengang']}")

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="peregos_queue")

channel.basic_consume(
    queue="peregos_queue",
    on_message_callback=callback,
    auto_ack=True
)

print("[PEREGOS] Warte auf Anträge …")
channel.start_consuming()
