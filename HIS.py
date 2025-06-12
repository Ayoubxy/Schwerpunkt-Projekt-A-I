import pika
import json
import tkinter as tk
from tkinter import messagebox

# Studiengangsdatenbank
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

def sende_student():
    name = entry_name.get()
    matrikelnummer = entry_matrikel.get()
    studiengang = entry_studiengang.get().strip().lower()

    if not name or not matrikelnummer or not studiengang:
        messagebox.showerror("Fehler", "Bitte alle Felder ausfüllen.")
        return

    if studiengang not in studiengangs_info:
        messagebox.showerror("Fehler", f"Studiengang nicht bekannt.\n\nVerfügbare:\n" +
                             ", ".join(studiengangs_info.keys()))
        return

    info = studiengangs_info[studiengang]

    student = {
        "name": name,
        "matrikelNummer": matrikelnummer,
        "studiengang": studiengang,
        "startdatum": info["startdatum"],
        "credits": info["credits"]
    }

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.queue_declare(queue="middleware_queue")
        message = json.dumps(student)
        channel.basic_publish(exchange='', routing_key='middleware_queue', body=message)
        connection.close()

        messagebox.showinfo("Gesendet", f"{name} ({studiengang}) wurde erfolgreich übermittelt.")
        entry_name.delete(0, tk.END)
        entry_matrikel.delete(0, tk.END)
        entry_studiengang.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("RabbitMQ Fehler", str(e))

# GUI Aufbau
root = tk.Tk()
root.title("HIS – Studentendaten eingeben")
root.geometry("400x300")

tk.Label(root, text="Name des Studenten").pack()
entry_name = tk.Entry(root, width=40)
entry_name.pack()

tk.Label(root, text="Matrikelnummer").pack()
entry_matrikel = tk.Entry(root, width=40)
entry_matrikel.pack()

tk.Label(root, text="Studiengang").pack()
entry_studiengang = tk.Entry(root, width=40)
entry_studiengang.pack()

tk.Button(root, text="Daten senden", command=sende_student).pack(pady=20)

root.mainloop()
