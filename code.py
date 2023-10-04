import requests
import winsound
import time
import tkinter as tk
from tkinter import simpledialog, messagebox
import threading

# Ruta al archivo de sonido
sound_file = 'C:\\Windows\\Media\\Ring02.wav'

def play_sound():
    winsound.PlaySound(sound_file, winsound.SND_FILENAME)

def get_transaction_details(api_key, transaction_hash):
    url = f'https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={transaction_hash}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('result', {})
    else:
        print(f'Error: {response.status_code}')
        return None

def get_current_block_number(api_key):
    url = f'https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return int(response.json().get('result', '0x0'), 16)
    else:
        print(f'Error: {response.status_code}')
        return None

def check_confirmations(api_key, transaction_hash):
    confirmations_target = 400
    while True:
        transaction_details = get_transaction_details(api_key, transaction_hash)
        if transaction_details:
            transaction_block_number = int(transaction_details.get('blockNumber', '0x0'), 16)
            current_block_number = get_current_block_number(api_key)
            if current_block_number and transaction_block_number:
                confirmations = current_block_number - transaction_block_number
                confirmation_label.config(text=f"Confirmations: {confirmations}")
                if confirmations >= confirmations_target:
                    play_sound()  # Reproduce el archivo de sonido
                    messagebox.showinfo("Notification", "Target confirmations reached!")
                    break
        time.sleep(1)  # Espera 60 segundos antes de revisar de nuevo

def start_checking():
    api_key = api_key_entry.get()
    transaction_hash = tx_hash_entry.get()
    thread = threading.Thread(target=check_confirmations, args=(api_key, transaction_hash))  # <--- Crea un hilo
    thread.start()  # <--- Inicia el hilo

app = tk.Tk()
app.title("Etherscan Checker")

# Frame
frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

# Labels and Entry widgets
tk.Label(frame, text="API Key:").grid(row=0, column=0, sticky="w", pady=5)
api_key_entry = tk.Entry(frame, width=50)
api_key_entry.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Transaction Hash:").grid(row=1, column=0, sticky="w", pady=5)
tx_hash_entry = tk.Entry(frame, width=50)
tx_hash_entry.grid(row=1, column=1, pady=5)

# Label to show confirmations
confirmation_label = tk.Label(frame, text="Confirmations: 0")
confirmation_label.grid(row=2, column=0, columnspan=2, pady=5)

# Button to start checking
btn = tk.Button(frame, text="Start Checking", command=start_checking)
btn.grid(row=3, column=0, columnspan=2, pady=10)

app.mainloop()
