import threading
from parkingGate import main as gate_main
from testReceiver import run_receiver
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import json

# Plik do przechowywania danych o parkowaniu
PARKING_DATA_FILE = "parking_data.json"

# Funkcje pomocnicze
def load_parking_data():
    try:
        with open(PARKING_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_parking_data(data):
    with open(PARKING_DATA_FILE, "w") as file:
        json.dump(data, file)

def handle_card_read(uid, entrance):
    parking_data = load_parking_data()
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if entrance:
        if str(uid) in parking_data:
            messagebox.showerror("Błąd", "Karta już zarejestrowana.")
        else:
            parking_data[str(uid)] = {"entry_time": time_stamp}
            save_parking_data(parking_data)
            messagebox.showinfo("Sukces", f"Karta {uid} zarejestrowana przy wjeździe o {time_stamp}.")
    else:
        if str(uid) not in parking_data:
            messagebox.showerror("Błąd", "Karta nieznaleziona.")
        else:
            entry_time = datetime.strptime(parking_data[str(uid)]['entry_time'], "%Y-%m-%d %H:%M:%S")
            exit_time = datetime.now()
            duration = (exit_time - entry_time).total_seconds() / 60
            payment = round((duration - 60) * 0.5, 2)
            if duration <= 60:  # Pierwsza godzina darmowa
                messagebox.showinfo("Czas postoju", f"Czas postoju: {duration:.2f} minut. Karta {uid}. Pierwsza godzina jest darmowa.")
                del parking_data[str(uid)]
                save_parking_data(parking_data)
            else:
                if not messagebox.askyesno("Wyjazd", f"Czas postoju: {duration:.2f} minut. Do zapłaty: {payment:.2f} zł. Czy zapłacono?"):
                    messagebox.showinfo("Zapłać",f"Aby wyjechać musisz zapłacić: {payment:.2f} zł.")
                else:
                    del parking_data[str(uid)]
                    save_parking_data(parking_data)
                #messagebox.showinfo("Wyjazd", f"Czas postoju: {duration:.2f} minut. Do zapłaty: {payment:.2f} zł. Aby zapłacić kliknij Ok")
            #del parking_data[str(uid)]
            #save_parking_data(parking_data)

# GUI

def create_gui():
    root = tk.Tk()
    root.title("System Parkingowy")

    tk.Label(root, text="System parkingowy uruchomiony.", font=("Arial", 14)).pack(pady=20)
    root.mainloop()

# Uruchomienie bramki parkingowej w osobnym wątku
def start_parking_gate():
    gate_main()

# Uruchomienie odbiornika w osobnym wątku
def start_receiver():
    run_receiver()

# Funkcja główna
if __name__ == "__main__":
    # Wątki dla niezależnego działania funkcji
    gate_thread = threading.Thread(target=start_parking_gate, daemon=True)
    receiver_thread = threading.Thread(target=start_receiver, daemon=True)

    gate_thread.start()
    receiver_thread.start()

    #handle_card_read("dsdsad", True)
    #handle_card_read("dsdsad", False)
    create_gui()
