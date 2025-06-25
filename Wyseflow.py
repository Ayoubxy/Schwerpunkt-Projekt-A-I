import pika
import json
import tkinter as tk
from threading import Thread

# GUI-Fenster vorbereiten
root = tk.Tk()
root.title("WyseFlow – Thesis applications")
root.geometry("600x400")

text_area = tk.Text(root, wrap=tk.WORD, height=20, width=70)
text_area.pack(padx=10, pady=10)
text_area.insert(tk.END, "[WYSEFLOW] Waiting for thesis applications …\n")

def zeige_daten(data):
    antrag = (
        f"\n--- Thesis application submitted ---\n"
        f"Name: {data['name']}\n"
        f"Matrikelnummer: {data['matrikelNummer']}\n"
        f"Studiengang: {data['studiengang']}\n"
        f"Credits: {data['credits']}\n"
        f"Startdatum: {data['startdatum']}\n"
    )
    text_area.insert(tk.END, antrag)
    text_area.see(tk.END)

# RabbitMQ-Verbindung in Hintergrundthread
def empfange_nachrichten():
    def callback(ch, method, properties, body):
        data = json.loads(body)
        root.after(0, zeige_daten, data)

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()

        channel.exchange_declare(exchange="student_exchange", exchange_type="direct")
        channel.queue_declare(queue="queue_wyseflow")
        channel.queue_bind(exchange="student_exchange", queue="queue_wyseflow", routing_key="wyseflow")

        channel.basic_consume(queue="queue_wyseflow", on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except Exception as e:
        text_area.insert(tk.END, f"\n[Connection error] , [Rabbit MQ not available, please try again in a few minutes]: {e}\n")

# Starte Empfang im Thread
thread = Thread(target=empfange_nachrichten, daemon=True)
thread.start()

root.mainloop()
