import pika
import json

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"\n[PEREGOS] Antrag erhalten vom Studenten:")
    print(f"Name: {data['name']}")
    print(f"Matrikelnummer: {data['matrikelNummer']}")
    print(f"Studiengang: {data['studiengang']}")

# Verbindung zu RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Wichtig: dieselbe Exchange wie in der Middleware
channel.exchange_declare(exchange="student_exchange", exchange_type="direct")

# Peregos-Queue deklarieren
channel.queue_declare(queue="queue_peregos")

# Queue mit Routing Key verbinden
channel.queue_bind(
    exchange="student_exchange",
    queue="queue_peregos",
    routing_key="peregos"
)

# Nachrichten empfangen
channel.basic_consume(
    queue="queue_peregos",
    on_message_callback=callback,
    auto_ack=True
)

print("[PEREGOS] Warte auf Anträge …")
channel.start_consuming()
