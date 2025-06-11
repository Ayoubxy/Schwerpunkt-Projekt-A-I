import pika
import json

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"\n[WYSEFLOW] Abschlussarbeit beantragt von:")
    print(f"Name: {data['name']}")
    print(f"Matrikelnummer: {data['matrikelNummer']}")
    print(f"Studiengang: {data['studiengang']}")
    print(f"Credits: {data['credits']}")

# Verbindung zu RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Gleiche Exchange wie in der Middleware
channel.exchange_declare(exchange="student_exchange", exchange_type="direct")

# Queue für WyseFlow
channel.queue_declare(queue="queue_wyseflow")

# Queue mit Exchange und Routing Key binden
channel.queue_bind(
    exchange="student_exchange",
    queue="queue_wyseflow",
    routing_key="wyseflow"
)

# Nachrichten empfangen
channel.basic_consume(
    queue="queue_wyseflow",
    on_message_callback=callback,
    auto_ack=True
)

print("[WYSEFLOW] Warte auf Abschlussarbeitsanträge …")
channel.start_consuming()
