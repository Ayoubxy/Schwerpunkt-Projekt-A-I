import pika
import json
import tkinter as tk
from tkinter import messagebox

# Funktion zum Senden an RabbitMQ
def sende_student():
    name = entry_name.get()
    matrikelnummer = entry_matrikel.get()
    studiengang = entry_studiengang.get()

    if not name or not matrikelnummer or not studiengang:
        messagebox.showerror("Fehler", "Bitte alle Felder ausfüllen.")
        return

    student = {
        "name": name,
        "matrikelNummer": matrikelnummer,
        "studiengang": studiengang
    }

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.queue_declare(queue="middleware_queue")

        message = json.dumps(student)
        channel.basic_publish(exchange='', routing_key='middleware_queue', body=message)
        connection.close()

        messagebox.showinfo("Erfolg", f"Daten gesendet: {student['name']} ({student['studiengang']})")
        entry_name.delete(0, tk.END)
        entry_matrikel.delete(0, tk.END)
        entry_studiengang.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Verbindungsfehler", str(e))

# GUI mit Tkinter erstellen
root = tk.Tk()
root.title("HIS - Studentendaten senden")
root.geometry("400x250")

# Eingabefelder und Labels
label_name = tk.Label(root, text="Name")
label_name.pack()
entry_name = tk.Entry(root, width=40)
entry_name.pack()

label_matrikel = tk.Label(root, text="Matrikelnummer")
label_matrikel.pack()
entry_matrikel = tk.Entry(root, width=40)
entry_matrikel.pack()

label_studiengang = tk.Label(root, text="Studiengang")
label_studiengang.pack()
entry_studiengang = tk.Entry(root, width=40)
entry_studiengang.pack()

# Sende-Button
sende_button = tk.Button(root, text="Daten senden", command=sende_student)
sende_button.pack(pady=10)

root.mainloop()
