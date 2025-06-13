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

        # --- Nachricht an Peregos vorbereiten (ohne Credits) ---
        student_peregos = dict(student)
        student_peregos.pop("credits", None)

        channel.basic_publish(
            exchange='student_exchange',
            routing_key='peregos',
            body=json.dumps(student_peregos)
        )
        print(f"[MIDDLEWARE] Sent to Peregos: {student['name']}")

        # --- Nachricht an WyseFlow nur wenn Bedingungen erfüllt ---
        if monate_diff > 3 and student["credits"] > 0:
            channel.basic_publish(
                exchange='student_exchange',
                routing_key='wyseflow',
                body=json.dumps(student)
            )
            print(f"[MIDDLEWARE] Sent to Wyseflow: {student['name']}")

    except Exception as e:
        print("[MIDDLEWARE] Error during processing:", e)

channel.basic_consume(queue='middleware_queue', on_message_callback=callback, auto_ack=True)

print("[MIDDLEWARE] Running and waiting for messages...")
channel.start_consuming()
