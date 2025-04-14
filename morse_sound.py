#!/usr/bin/env python3
"""
Moduł zawierający funkcje do odtwarzania kodu Morse'a jako dźwięku
"""

import time
import platform
import subprocess

# Parametry dla odtwarzania dźwięku
DOT_DURATION = 100  # ms
DASH_DURATION = 300  # ms
SYMBOL_PAUSE = 100   # ms
LETTER_PAUSE = 300   # ms
WORD_PAUSE = 700    # ms
FREQUENCY = 800      # Hz

def play_morse_with_simple_beep(morse_code, status_callback=None):
    """
    Odtwarza kod Morse'a jako dźwięk używając prostej metody dostępnej na każdym systemie.
    Ta metoda nie wymaga instalacji numpy ani pygame.
    
    Args:
        morse_code (str): Kod Morse'a do odtworzenia
        status_callback (function, optional): Callback do aktualizacji statusu
    """
    system = platform.system()
    
    if status_callback:
        status_callback(f"Odtwarzanie na systemie {system}...")
    
    for i, symbol in enumerate(morse_code):
        if status_callback and i % 5 == 0:
            progress = min(100, int((i / len(morse_code)) * 100))
            status_callback(f"Odtwarzanie: {progress}%")
            
        if symbol == '.':
            # Odtwórz kropkę (krótki dźwięk)
            beep(FREQUENCY, DOT_DURATION, system)
            time.sleep(SYMBOL_PAUSE / 1000)
            
        elif symbol == '-':
            # Odtwórz kreskę (długi dźwięk)
            beep(FREQUENCY, DASH_DURATION, system)
            time.sleep(SYMBOL_PAUSE / 1000)
            
        elif symbol == ' ':
            # Przerwa między literami
            time.sleep(LETTER_PAUSE / 1000)
            
        elif symbol == '/':
            # Przerwa między słowami
            time.sleep(WORD_PAUSE / 1000)
    
    if status_callback:
        status_callback("Odtwarzanie zakończone.")

def beep(frequency, duration, system):
    """
    Generuje sygnał dźwiękowy na różnych systemach operacyjnych
    
    Args:
        frequency (int): Częstotliwość dźwięku w Hz
        duration (int): Czas trwania dźwięku w ms
        system (str): Nazwa systemu operacyjnego
    """
    try:
        if system == "Windows":
            # Użyj wbudowanej funkcji winsound.Beep dla Windows
            try:
                import winsound
                winsound.Beep(frequency, duration)
            except ImportError:
                # Jeśli nie można zaimportować winsound, używamy print
                print("\a")  # Standardowy sygnał dźwiękowy
                time.sleep(duration / 1000)
        else:  # Linux, macOS i inne systemy
            # Użyj wyświetlenia znaku dzwonka w terminalu
            print("\a", end="", flush=True)
            time.sleep(duration / 1000)
    except Exception as e:
        # W razie błędu, po prostu symulujemy dźwięk poprzez pauzę
        print(f"[BEEP: {'.' if duration == DOT_DURATION else '-'}]", end="", flush=True)
        time.sleep(duration / 1000)

# Proste testowanie modułu
if __name__ == "__main__":
    test_morse = "... --- ..."  # SOS
    print(f"Odtwarzam kod Morse'a: {test_morse}")
    play_morse_with_simple_beep(test_morse)