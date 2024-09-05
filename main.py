import tkinter as tk
from tkinter import ttk, messagebox
from ping3 import ping
from datetime import datetime
import threading
import queue
import json

class NetworkMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitorowanie urządzeń sieciowych")

        # Ustawienie położenia okna na środku ekranu
        self.center_window(850, 400)  # Szerokość: 600px, Wysokość: 400px

        # Rozszerzone dane urządzeń z dodatkowymi informacjami
        with open('devices.json', 'r') as file:
            self.devices = json.load(file)

        self.device_queue = queue.Queue()
        self.create_widgets()
        self.update_device_list()  # Na początku wyświetlamy domyślną listę urządzeń
        self.update_gui_periodically()  # Rozpocznij cykliczne aktualizowanie GUI
        self.ping_devices_periodically()  # Rozpocznij cykliczne pingowanie

    def create_widgets(self):
        # Typ urządzeń
        self.device_type_label = tk.Label(self.root, text="Wybierz typ urządzeń:")
        self.device_type_label.pack(pady=5)

        # Domyślnie ustawiony typ urządzenia to "komputery"
        self.device_type_combobox = ttk.Combobox(self.root, values=["wszystkie"] + list(self.devices.keys()))
        self.device_type_combobox.set("komputery")  # Ustawienie domyślnej wartości
        self.device_type_combobox.pack(pady=5)
        self.device_type_combobox.bind("<<ComboboxSelected>>", self.update_device_list)

        # Lista urządzeń
        self.device_list = ttk.Treeview(self.root, columns=("name", "status", "last_ping", "ping_value"), show='headings')
        self.device_list.heading("name", text="Nazwa")
        self.device_list.heading("status", text="Status")
        self.device_list.heading("last_ping", text="Ostatnie pingowanie")
        self.device_list.heading("ping_value", text="Wartość ostatniego pingu")

        # Style
        self.style = ttk.Style()
        self.style.configure("Online.TLabel", foreground="green")
        self.style.configure("Offline.TLabel", foreground="red")

        # Zarejestruj style w Treeview
        self.device_list.tag_configure("Online", foreground="green")
        self.device_list.tag_configure("Offline", foreground="red")

        # Wstaw do Treeview
        self.device_list.pack(pady=5, fill=tk.BOTH, expand=True)
        self.device_list.bind("<Double-1>", self.show_device_info)  # Bind na podwójne kliknięcie

        # Przycisk "Autor"
        self.author_button = tk.Button(self.root, text="Autor", command=self.show_author_info)
        self.author_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Adnotacja na dole
        self.footer_label = tk.Label(self.root, text="Twórca: Marcin Tomaszewski", fg="grey", font=("Arial", 8))
        self.footer_label.pack(side=tk.BOTTOM, pady=5)

    def center_window(self, width, height):
        # Pobierz szerokość i wysokość ekranu
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Oblicz współrzędne dla środka ekranu
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Ustaw rozmiar okna i położenie
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def update_device_list(self, event=None):
        # Pobierz wybrany typ urządzeń
        selected_type = self.device_type_combobox.get()

        # Wyczyść aktualną listę
        for item in self.device_list.get_children():
            self.device_list.delete(item)

        if selected_type == "wszystkie":
            # Dodaj wszystkie urządzenia
            self.devices_to_check = [(name, ip, owner, room, connection) for device_list in self.devices.values() for name, ip, owner, room, connection in device_list]
        elif selected_type in self.devices:
            # Dodaj urządzenia dla wybranego typu
            self.devices_to_check = self.devices[selected_type]
        else:
            self.devices_to_check = []

        # Dodaj nowe urządzenia do GUI
        for name, ip, owner, room, connection in self.devices_to_check:
            # Dodaj urządzenia do widoku tylko jeśli jeszcze ich tam nie ma
            if not self.device_list.exists(name):
                self.device_list.insert("", tk.END, iid=name, values=(name, "N/A", "N/A", "N/A"))

        # Natychmiastowe sprawdzenie pingów po zmianie typu urządzeń
        threading.Thread(target=self.ping_devices, args=(self.devices_to_check,), daemon=True).start()

    def ping_devices_periodically(self):
        # Rozpocznij wątek do pingowania urządzeń
        if self.devices_to_check:
            threading.Thread(target=self.ping_devices, args=(self.devices_to_check,), daemon=True).start()
        # Ustaw, aby ta funkcja była wywoływana ponownie za 10 sekund
        self.root.after(10000, self.ping_devices_periodically)

    def ping_devices(self, devices):
        results = []
        for name, ip, owner, room, connection in devices:
            try:
                status, last_ping, ping_value = self.check_device(ip)
                results.append((name, status, last_ping, ping_value, ip, owner, room, connection))
            except Exception as e:
                results.append((name, "Error", "N/A", "N/A", ip, owner, room, connection))
        
        # Dodaj wyniki do kolejki, aby zaktualizować GUI w głównym wątku
        self.device_queue.put(results)

    def update_gui_periodically(self):
        # Aktualizuj GUI
        self.update_gui()
        # Ustaw, aby ta funkcja była wywoływana ponownie za 100 ms
        self.root.after(100, self.update_gui_periodically)

    def update_gui(self):
        while not self.device_queue.empty():
            results = self.device_queue.get()
            for name, status, last_ping, ping_value, ip, owner, room, connection in results:
                # Sprawdź, czy urządzenie już istnieje, i zaktualizuj jego wartości
                if self.device_list.exists(name):
                    # Ustaw tag w zależności od statusu
                    tag = "Online" if status == "Online" else "Offline"
                    self.device_list.item(name, values=(name, status, last_ping, ping_value), tags=(tag,))

    def check_device(self, ip):
        try:
            response_time = ping(ip)
            
            if response_time is not None and response_time is not False:
                status = "Online"
                last_ping = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ping_value = f"{response_time * 1000:.2f} ms"
            else:
             status = "Offline"
             last_ping = "N/A"
             ping_value = "N/A"
        except Exception as e:
            status = "Error"
            last_ping = "N/A"
            ping_value = "N/A"
    
        return status, last_ping, ping_value

    def show_device_info(self, event):
        # Uzyskaj wybrany element
        item = self.device_list.selection()
        if not item:
            return

        # Pobierz szczegóły urządzenia
        name = self.device_list.item(item)["values"][0]
        for device in self.devices_to_check:
            if device[0] == name:
                _, ip, owner, room, connection = device
                break

        # Wyświetl informacje w messageboxie
        info_text = (
            f"Nazwa: {name}\n"
            f"Adres IP: {ip}\n"
            f"Właściciel: {owner}\n"
            f"Pokój: {room}\n"
            f"Typ połączenia: {connection}"
        )
        messagebox.showinfo("Szczegóły urządzenia", info_text)

    def show_author_info(self):
        # Wyświetl informacje o autorze
        author_info = (
        "Autor programu: \n"
        "Marcin Tomaszewski\n"
        "Email: tomaszewsky.marcin@gmail.com\n"
        "GitHub: github.com/martom93\n"
        "\n"
        "Program do minitorowania urządzeń w sieci SM.\n"
        )
        messagebox.showinfo("Informacje o autorze", author_info)

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkMonitor(root)
    root.mainloop()
