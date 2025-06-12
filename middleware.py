import pika
import json
from datetime import datetime


# --- Studiengangs-Daten direkt in der Middleware ---
studiengangs_info = [
    {"studiengang": "Wirtschaft", "startdatum": "2025-05-01", "credits": 0},
    {"studiengang": "Maschinenbau", "startdatum": "2025-04-15", "credits": 0},
    {"studiengang": "Elektrotechnik", "startdatum": "2022-04-01", "credits": 90},
    {"studiengang": "Medieninformatik", "startdatum": "2023-09-01", "credits": 50},
    {"studiengang": "Informatik", "startdatum": "2021-10-01", "credits": 180},
    {"studiengang": "Soziale Arbeit", "startdatum": "2025-06-01", "credits": 0},
    {"studiengang": "Bauingenieurwesen", "startdatum": "2024-12-01", "credits": 10},
    {"studiengang": "Wirtschaftsinformatik", "startdatum": "2025-03-01", "credits": 0},
    {"studiengang": "Biotechnologie", "startdatum": "2023-03-01", "credits": 60},
    {"studiengang": "Architektur", "startdatum": "2025-04-10", "credits": 5},
    {"studiengang": "Politikwissenschaft", "startdatum": "2022-09-01", "credits": 120},
    {"studiengang": "Psychologie", "startdatum": "2025-01-20", "credits": 2}
]

# Mapping zur schnelleren Suche
studiengang_map = {eintrag["studiengang"].lower(): eintrag for eintrag in studiengangs_info}

# Verbindung zu RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='middleware_queue')
channel.exchange_declare(exchange='student_exchange', exchange_type='direct')

def callback(ch, method, properties, body):
    student = json.loads(body)
    studiengang_key = student.get("studiengang", "").lower()

    if studiengang_key not in studiengang_map:
        print(f"[MIDDLEWARE] Unbekannter Studiengang: {studiengang_key}")
        return

    # Daten ergänzen
    info = studiengang_map[studiengang_key]
    student["startdatum"] = info["startdatum"]
    student["credits"] = info["credits"]

    try:
        start = datetime.strptime(student["startdatum"], "%Y-%m-%d")
        heute = datetime.today()
        monate_diff = (heute.year - start.year) * 12 + (heute.month - start.month)

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
