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
