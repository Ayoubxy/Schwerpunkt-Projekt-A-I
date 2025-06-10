import pika
import json
from student_data import students  # Importiere deine Student:innen-Liste

# Verbindung zu RabbitMQ aufbauen
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Die zentrale Eingangsschlange der Middleware
channel.queue_declare(queue="middleware_queue")

# Alle Student:innen nacheinander senden
for student in students:
    message = json.dumps(student.to_dict())
    channel.basic_publish(
        exchange='',
        routing_key='middleware_queue',
        body=message
    )
    print(f"[SENDER] Gesendet: {student.name} ({student.studiengang})")

# Verbindung schließen
connection.close()
