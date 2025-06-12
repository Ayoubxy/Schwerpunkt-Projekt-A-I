import pika
import json

# --- Studiengangs-Daten im HIS (alle Keys in lowercase!) ---
studiengangs_info = {
    "wirtschaft": {"startdatum": "2025-05-01", "credits": 0},
    "maschinenbau": {"startdatum": "2025-04-15", "credits": 0},
    "elektrotechnik": {"startdatum": "2022-04-01", "credits": 90},
    "medieninformatik": {"startdatum": "2023-09-01", "credits": 50},
    "informatik": {"startdatum": "2021-10-01", "credits": 180},
    "soziale arbeit": {"startdatum": "2025-06-01", "credits": 0},
    "bauingenieurwesen": {"startdatum": "2024-12-01", "credits": 10},
    "wirtschaftsinformatik": {"startdatum": "2025-03-01", "credits": 0},
    "biotechnologie": {"startdatum": "2023-03-01", "credits": 60},
    "architektur": {"startdatum": "2025-04-10", "credits": 5},
    "politikwissenschaft": {"startdatum": "2022-09-01", "credits": 120},
    "psychologie": {"startdatum": "2025-01-20", "credits": 2}
}

def eingabe_student():
    name = input("Name des Studenten: ")
    matrikelnummer = input("Matrikelnummer: ")
    studiengang_input = input("Studiengang: ").strip().lower()

    if studiengang_input not in studiengangs_info:
        print("[HIS] Fehler: Studiengang nicht bekannt.")
        print("[HIS] Verfügbare Studiengänge:", ", ".join(studiengangs_info.keys()))
        return None

    info = studiengangs_info[studiengang_input]

    student = {
        "name": name,
        "matrikelNummer": matrikelnummer,
        "studiengang": studiengang_input,
        "startdatum": info["startdatum"],
        "credits": info["credits"]
    }
    return student

# Verbindung zu RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="middleware_queue")

student = eingabe_student()
if student:
    message = json.dumps(student)
    channel.basic_publish(
        exchange='',
        routing_key='middleware_queue',
        body=message
    )
    print(f"[SENDER] Gesendet: {student['name']} ({student['studiengang']})")

connection.close()
