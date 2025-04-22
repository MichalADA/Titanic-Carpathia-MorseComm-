#!/usr/bin/env python3
"""
Główny program uruchamiający symulację radiostacji Titanica i Carpathii w osobnych oknach
"""

import tkinter as tk
import threading
import sys
import os

# Dodaj ścieżkę do katalogów z modułami
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import klas radiostacji
from carphatia_station import CarpathiaRadioStation
from titanic_staion import TitanicRadioStation

def start_carpathia():
    """Uruchamia stację radiową Carpathii w osobnym oknie"""
    carpathia_root = tk.Tk()
    carpathia_root.title("RMS Carpathia - Stacja Radiowa")
    carpathia_app = CarpathiaRadioStation(carpathia_root)
    carpathia_root.mainloop()

def start_titanic():
    """Uruchamia stację radiową Titanica w osobnym oknie"""
    titanic_root = tk.Tk()
    titanic_root.title("RMS Titanic - Stacja Radiowa")
    titanic_app = TitanicRadioStation(titanic_root)
    titanic_root.mainloop()

def main():
    """Funkcja główna uruchamiająca obie aplikacje w osobnych oknach"""
    
    # Uruchom stację Carpathii w osobnym wątku
    carpathia_thread = threading.Thread(target=start_carpathia)
    carpathia_thread.daemon = True
    carpathia_thread.start()
    
    # Uruchom stację Titanica w głównym wątku
    start_titanic()
    
if __name__ == "__main__":
    main()