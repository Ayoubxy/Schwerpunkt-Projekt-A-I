import pika
import json

# Verbindung zu RabbitMQ aufbauen
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Die zentrale Eingangsschlange der Middleware
channel.queue_declare(queue="middleware_queue")

# Benutzereingaben über die Konsole
def eingabe_student():
    name = input("Name des Studenten: ")
    matrikelnummer = input("Matrikelnummer: ")
    studiengang = input("Studiengang: ")

    return {
        "name": name,
        "matrikelNummer": matrikelnummer,
        "studiengang": studiengang
    }

# Einzelne Eingabe senden
student = eingabe_student()
message = json.dumps(student)
channel.basic_publish(
    exchange='',
    routing_key='middleware_queue',
    body=message
)
print(f"[SENDER] Gesendet: {student['name']} ({student['studiengang']})")

# Verbindung schließen
connection.close()
