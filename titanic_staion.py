#!/usr/bin/env python3
"""
Symulacja stacji radiowej Titanica używającej kodu Morse'a
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socket
import threading
import time
import random
from datetime import datetime
import os
import sys

# Dodaj ścieżkę do modułów morse_translator
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    # Próba importu z pakietu
    from morse_utils import text_to_morse, morse_to_text
    from morse_sound import play_morse_with_simple_beep
except ImportError:
    # Wersja rezerwowa - bezpośredni import
    from bezposredni_start import text_to_morse, morse_to_text, play_morse_with_simple_beep

# Konfiguracja połączenia
CARPATHIA_HOST = 'localhost'  # Adres IP Carpathii (ten sam komputer)
CARPATHIA_PORT = 5678         # Port nasłuchiwania Carpathii
TITANIC_PORT = 5679           # Port nasłuchiwania Titanica

# Historyczne wiadomości Titanica
TITANIC_MESSAGES = [
    "CQD CQD SOS SOS FROM TITANIC. WE ARE SINKING FAST. PASSENGERS BEING PUT INTO BOATS.",
    "CQD CQD SOS TITANIC 41.46 N 50.14 W REQUIRE IMMEDIATE ASSISTANCE.",
    "WE HAVE STRUCK ICEBERG SINKING NEED IMMEDIATE ASSISTANCE.",
    "TITANIC SINKING HEAD DOWN NEED IMMEDIATE ASSISTANCE.",
    "SOS TITANIC POSITION 41.44 N 50.24 W. REQUIRE IMMEDIATE ASSISTANCE.",
    "COME AT ONCE. WE HAVE STRUCK A BERG.",
    "SINKING, COME QUICKLY.",
    "WE ARE PUTTING PASSENGERS OFF IN SMALL BOATS.",
    "WOMEN AND CHILDREN IN BOATS, CANNOT LAST MUCH LONGER."
]

class TitanicRadioStation:
    """Klasa symulująca radiostację Titanica"""
    
    def __init__(self, root):
        """
        Inicjalizuje aplikację stacji radiowej
        
        Args:
            root (tk.Tk lub tk.Frame): Główne okno lub ramka aplikacji
        """
        self.root = root
        
        # Sprawdzamy czy root jest głównym oknem czy ramką
        if isinstance(root, tk.Tk):
            self.is_main_window = True
            self.root.title("Radio Titanica - RMS Titanic")
            self.root.geometry("800x600")
            self.root.minsize(600, 500)
        else:
            self.is_main_window = False
        
        # Ustawienie stylu historycznego
        self.set_historical_style()
        
        # Stan komunikacji
        self.receiving = False
        self.is_playing = False
        self.server_thread = None
        
        # Tworzenie interfejsu
        self.create_widgets()
        
        # Uruchomienie serwera nasłuchującego
        self.start_server()
        
    def set_historical_style(self):
        """Ustawia historyczny styl GUI"""
        style = ttk.Style()
        style.configure("TFrame", background="#d2b48c")
        style.configure("Historical.TLabel", 
                      font=("Times New Roman", 12),
                      background="#d2b48c", 
                      foreground="#000000")
        style.configure("Title.TLabel", 
                      font=("Times New Roman", 16, "bold"),
                      background="#d2b48c", 
                      foreground="#8B0000")
        style.configure("Historical.TButton", 
                      font=("Times New Roman", 11),
                      background="#8B4513")
        
        if self.is_main_window:
            self.root.configure(background="#d2b48c")  # Ustawienie koloru tła
        
    def create_widgets(self):
        """Tworzy wszystkie widgety dla interfejsu użytkownika"""
        # Nagłówek
        header_frame = ttk.Frame(self.root, padding="10", style="TFrame")
        header_frame.pack(fill=tk.X)
        
        ttk.Label(
            header_frame, 
            text="RMS Titanic - Stacja Radiowa", 
            style="Title.TLabel"
        ).pack()
        
        # Data i położenie
        info_frame = ttk.Frame(self.root, padding="5", style="TFrame")
        info_frame.pack(fill=tk.X)
        
        ttk.Label(
            info_frame, 
            text="14 kwietnia 1912, Położenie: 41.46 N 50.14 W", 
            style="Historical.TLabel"
        ).pack()
        
        # Ramka główna podzielona na nadawanie i odbieranie
        main_frame = ttk.Frame(self.root, padding="10", style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Lewa kolumna - nadawanie
        transmit_frame = ttk.LabelFrame(main_frame, text="Nadawanie", padding="10", style="TFrame")
        transmit_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Predefiniowane wiadomości
        ttk.Label(
            transmit_frame, 
            text="Wybierz wiadomość alarmową:", 
            style="Historical.TLabel"
        ).pack(anchor=tk.W)
        
        self.message_var = tk.StringVar()
        message_combo = ttk.Combobox(
            transmit_frame, 
            textvariable=self.message_var,
            values=TITANIC_MESSAGES,
            width=50
        )
        message_combo.pack(fill=tk.X, pady=(0, 10))
        message_combo.bind("<<ComboboxSelected>>", self.update_custom_message)
        
        # Niestandardowa wiadomość
        ttk.Label(
            transmit_frame, 
            text="Lub wpisz własną wiadomość:", 
            style="Historical.TLabel"
        ).pack(anchor=tk.W)
        
        self.custom_message = scrolledtext.ScrolledText(
            transmit_frame, 
            height=5,
            wrap=tk.WORD
        )
        self.custom_message.pack(fill=tk.X, pady=(0, 10))
        
        # Przyciski nadawania
        buttons_frame = ttk.Frame(transmit_frame, style="TFrame")
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(
            buttons_frame, 
            text="Nadaj wiadomość", 
            command=self.transmit_message,
            style="Historical.TButton"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            buttons_frame, 
            text="Nadaj SOS", 
            command=self.transmit_sos,
            style="Historical.TButton"
        ).pack(side=tk.LEFT)
        
        # Prawa kolumna - odbieranie
        receive_frame = ttk.LabelFrame(main_frame, text="Odbieranie", padding="10", style="TFrame")
        receive_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Wskaźnik odbierania
        self.signal_indicator = tk.Canvas(
            receive_frame, 
            width=20, 
            height=20, 
            bg="black",
            highlightthickness=1,
            highlightbackground="gray"
        )
        self.signal_indicator.pack(anchor=tk.W, pady=(0, 5))
        
        # Log komunikacji
        ttk.Label(
            receive_frame, 
            text="Log komunikacji:", 
            style="Historical.TLabel"
        ).pack(anchor=tk.W)
        
        self.communication_log = scrolledtext.ScrolledText(
            receive_frame, 
            height=15,
            wrap=tk.WORD,
            bg="#f5f5dc",  # Kolor starego papieru
            fg="#000000"
        )
        self.communication_log.pack(fill=tk.BOTH, expand=True)
        self.communication_log.config(state=tk.DISABLED)
        
        # Status bar
        self.status_var = tk.StringVar(value="Stacja gotowa do pracy")
        status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var,
            relief=tk.SUNKEN, 
            anchor=tk.W,
            style="Historical.TLabel"
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_custom_message(self, event):
        """Aktualizuje pole wiadomości własnej po wybraniu opcji z listy"""
        self.custom_message.delete("1.0", tk.END)
        self.custom_message.insert(tk.END, self.message_var.get())
    
    def log_message(self, message, is_transmitted=False):
        """Dodaje wiadomość do logu komunikacji"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = "NADANO: " if is_transmitted else "ODEBRANO: "
        
        self.communication_log.config(state=tk.NORMAL)
        self.communication_log.insert(tk.END, f"[{timestamp}] {prefix}{message}\n\n")
        self.communication_log.see(tk.END)
        self.communication_log.config(state=tk.DISABLED)
    
    def transmit_message(self):
        """Nadaje wiadomość do Carpathii"""
        message = self.custom_message.get("1.0", tk.END).strip()
        
        if not message:
            messagebox.showinfo("Informacja", "Wpisz wiadomość do nadania")
            return
        
        try:
            # Konwersja wiadomości na kod Morse'a
            morse_code = text_to_morse(message)
            
            # Symulacja zakłóceń i opóźnień z 1912 roku
            self.status_var.set("Nawiązywanie połączenia radiowego...")
            self.root.update()
            time.sleep(1 + random.random())  # Opóźnienie nawiązywania łączności
            
            # Odtworzenie dźwięku podczas nadawania
            threading.Thread(target=play_morse_with_simple_beep, args=(morse_code, self.status_callback), daemon=True).start()
            
            # Odtworzenie dźwięku przed nadaniem
            self.status_var.set("Nadawanie wiadomości...")
            self.root.update()
            
            # Blink lamp indicator during transmission
            self.blink_indicator(morse_code)
            
            # Nadanie wiadomości do Carpathii
            threading.Thread(
                target=self.send_message_to_carpathia,
                args=(message, morse_code),
                daemon=True
            ).start()
            
            # Rejestracja w logu
            self.log_message(message, is_transmitted=True)
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas nadawania: {str(e)}")
            self.status_var.set("Błąd nadawania")
    
    def transmit_sos(self):
        """Szybkie nadanie SOS"""
        sos_message = "SOS SOS SOS TITANIC NEEDS IMMEDIATE ASSISTANCE"
        self.custom_message.delete("1.0", tk.END)
        self.custom_message.insert("1.0", sos_message)
        self.transmit_message()
    
    def send_message_to_carpathia(self, message, morse_code):
        """Wysyła wiadomość do stacji Carpathii"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((CARPATHIA_HOST, CARPATHIA_PORT))
                
                # Symulacja szumów i zakłóceń radiowych
                if random.random() < 0.3:  # 30% szans na zakłócenia
                    # Dodanie losowych zakłóceń do kodu Morse'a
                    noise_chars = ['.', '-', ' ']
                    noise_positions = random.sample(range(len(morse_code)), 
                                                 k=min(3, len(morse_code) // 10))
                    morse_list = list(morse_code)
                    for pos in noise_positions:
                        morse_list[pos] = random.choice(noise_chars)
                    morse_code = ''.join(morse_list)
                
                # Wysłanie wiadomości
                packet = f"{message}|{morse_code}"
                s.sendall(packet.encode('utf-8'))
                
                self.status_var.set("Wiadomość nadana pomyślnie")
                
        except ConnectionRefusedError:
            self.status_var.set("Nie można nawiązać połączenia z Carpathią")
        except Exception as e:
            self.status_var.set(f"Błąd: {str(e)}")
    
    def start_server(self):
        """Uruchamia serwer nasłuchujący dla wiadomości od Carpathii"""
        self.server_thread = threading.Thread(
            target=self._run_server, 
            daemon=True
        )
        self.server_thread.start()
    
    def _run_server(self):
        """Wewnętrzna metoda uruchamiająca serwer nasłuchujący"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', TITANIC_PORT))
                s.listen()
                self.status_var.set("Nasłuchiwanie wiadomości...")
                
                while True:
                    conn, addr = s.accept()
                    with conn:
                        data = conn.recv(2048)
                        if data:
                            # Przetworzenie odebranej wiadomości
                            packet = data.decode('utf-8')
                            if '|' in packet:
                                message, morse_code = packet.split('|', 1)
                                self.receive_message(message, morse_code)
        except Exception as e:
            print(f"Błąd serwera: {e}")
    
    def receive_message(self, message, morse_code):
        """Obsługuje odebraną wiadomość od Carpathii"""
        if self.receiving:
            return
        
        self.receiving = True
        
        try:
            # Aktualizacja statusu
            self.status_var.set("Odbieranie wiadomości...")
            
            # Symulacja odbioru - migająca lampka
            self.blink_indicator(morse_code)
            
            # Odtwarzanie dźwięku odebranej wiadomości
            threading.Thread(target=play_morse_with_simple_beep, args=(morse_code, self.status_callback), daemon=True).start()
            
            # Dodanie wiadomości do logu
            self.log_message(message)
            
            self.status_var.set("Wiadomość odebrana")
        except Exception as e:
            self.status_var.set(f"Błąd odbierania: {str(e)}")
        finally:
            self.receiving = False
    
    def status_callback(self, message):
        """Callback do aktualizacji statusu podczas odtwarzania dźwięku"""
        self.status_var.set(message)
        self.root.update()
    
    def blink_indicator(self, morse_code):
        """Powoduje miganie wskaźnika zgodnie z kodem Morse'a"""
        for symbol in morse_code:
            if symbol == '.':
                # Kropka - krótkie mignięcie
                self.signal_indicator.config(bg="yellow")
                self.root.update()
                time.sleep(0.2)
                self.signal_indicator.config(bg="black")
                self.root.update()
                time.sleep(0.2)
            elif symbol == '-':
                # Kreska - długie mignięcie
                self.signal_indicator.config(bg="yellow")
                self.root.update()
                time.sleep(0.6)
                self.signal_indicator.config(bg="black")
                self.root.update()
                time.sleep(0.2)
            elif symbol == ' ':
                # Przerwa między znakami
                time.sleep(0.4)
            elif symbol == '/':
                # Przerwa między słowami
                time.sleep(1.0)

def main():
    """Funkcja główna uruchamiająca aplikację"""
    root = tk.Tk()
    app = TitanicRadioStation(root)
    root.mainloop()

if __name__ == "__main__":
    main()