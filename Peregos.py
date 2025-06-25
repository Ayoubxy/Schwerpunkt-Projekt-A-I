import pika
import json
import tkinter as tk
from threading import Thread

# GUI-Setup
root = tk.Tk()
root.title("Peregos – Applications")
root.geometry("500x400")

text_area = tk.Text(root, wrap=tk.WORD, height=20, width=60)
text_area.pack(padx=10, pady=10)
text_area.insert(tk.END, "[PEREGOS] Waiting for applications …\n")

def zeige_daten(data):
    antrag = (
        f"\n--- Application received ---\n"
        f"Name: {data['name']}\n"
        f"Matrikelnummer: {data['matrikelNummer']}\n"
        f"Studiengang: {data['studiengang']}\n"
    )
    text_area.insert(tk.END, antrag)
    text_area.see(tk.END)

# RabbitMQ-Empfang in separatem Thread
def empfange_nachrichten():
    def callback(ch, method, properties, body):
        data = json.loads(body)
        root.after(0, zeige_daten, data)

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()

        channel.exchange_declare(exchange="student_exchange", exchange_type="direct")
        channel.queue_declare(queue="queue_peregos")
        channel.queue_bind(exchange="student_exchange", queue="queue_peregos", routing_key="peregos")

        channel.basic_consume(queue="queue_peregos", on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except Exception as e:
        text_area.insert(tk.END, f"\n[Connection error. Rabbit MQ not available, please try again in a few minutes]: {e}\n")

# Starte den Empfangs-Thread
thread = Thread(target=empfange_nachrichten, daemon=True)
thread.start()

root.mainloop()
