import pika
import json

def callback(ch, method, properties, body):
    data = json.loads(body)
    global channel
    # Nachricht für Peregos (ohne Credits)
    peregos_data = {
        "name": data["name"],
        "matrikelnummer": data["matrikelnummer"],
        "studiengang": data["studiengang"]
    }
    
    # Nachricht für WyseFlow (mit Credits)
    wyseflow_data = {
        "name": data["name"],
        "matrikelnummer": data["matrikelnummer"],
        "studiengang": data["studiengang"],
        "credits": data["credits"]
    }

    # An beide Queues senden
    channel.basic_publish(
        exchange='',
        routing_key='peregos_queue',
        body=json.dumps(peregos_data)
    )
    channel.basic_publish(
        exchange='',
        routing_key='wyseflow_queue',
        body=json.dumps(wyseflow_data)
    )

    print(f"[Middleware] Weitergeleitet an beide Systeme: {data['name']}")
# Verbindung und Channel aufbauen
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Queues deklarieren
channel.queue_declare(queue="middleware_queue")
channel.queue_declare(queue="peregos_queue")
channel.queue_declare(queue="wyseflow_queue")

# Middleware konsumiert von der Eingangs-Queue
channel.basic_consume(
    queue="middleware_queue",
    on_message_callback=callback,
    auto_ack=True
)

print("[Middleware] Warte auf eingehende Anträge …")
channel.start_consuming()