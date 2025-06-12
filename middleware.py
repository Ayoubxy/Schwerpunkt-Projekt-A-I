import pika
import json
from datetime import datetime

# Verbindung zu RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='middleware_queue')
channel.exchange_declare(exchange='student_exchange', exchange_type='direct')

def callback(ch, method, properties, body):
    student = json.loads(body)

    try:
        start = datetime.strptime(student["startdatum"], "%Y-%m-%d")
        heute = datetime.today()
        monate_diff = (heute.year - start.year) * 12 + (heute.month - start.month)

        # Routing-Logik basierend auf credits & Startzeit
        if monate_diff <= 3 or student["credits"] == 0:
            routing_key = "peregos"
        else:
            routing_key = "wyseflow"

        channel.basic_publish(
            exchange='student_exchange',
            routing_key=routing_key,
            body=json.dumps(student)
        )

        print(f"[MIDDLEWARE] Weitergeleitet an {routing_key}: {student['name']}")

    except Exception as e:
        print("[MIDDLEWARE] Fehler bei der Verarbeitung:", e)

channel.basic_consume(queue='middleware_queue', on_message_callback=callback, auto_ack=True)

print("[MIDDLEWARE] Läuft und wartet auf Nachrichten...")
channel.start_consuming()
