#!/usr/bin/env python3
"""
Moduł zawierający podstawowe funkcje translatora kodu Morse'a
"""

# Słownik mapujący znaki alfabetu łacińskiego na kod Morse'a
CHAR_TO_MORSE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
    'Y': '-.--', 'Z': '--..', 
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', 
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', 
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--', 
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...', 
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-', 
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'
}

# Odwrócenie słownika dla tłumaczenia z kodu Morse'a na znaki
MORSE_TO_CHAR = {value: key for key, value in CHAR_TO_MORSE.items()}

def text_to_morse(text):
    """
    Konwertuje tekst na kod Morse'a.
    
    Args:
        text (str): Tekst do konwersji
        
    Returns:
        str: Tekst przekonwertowany na kod Morse'a
    """
    morse_code = []
    for char in text.upper():
        if char in CHAR_TO_MORSE:
            morse_code.append(CHAR_TO_MORSE[char])
        else:
            # Jeśli znak nie jest obsługiwany, pozostawiamy go bez zmian
            morse_code.append(char)
    
    # Łączymy kod Morse'a używając spacji pomiędzy znakami
    return ' '.join(morse_code)

def morse_to_text(morse_code):
    """
    Konwertuje kod Morse'a na tekst.
    
    Args:
        morse_code (str): Kod Morse'a do konwersji
        
    Returns:
        str: Tekst odkodowany z kodu Morse'a
    """
    # Dzielimy kod na znaki
    morse_chars = morse_code.split(' ')
    
    text = []
    for morse_char in morse_chars:
        if morse_char in MORSE_TO_CHAR:
            text.append(MORSE_TO_CHAR[morse_char])
        elif morse_char == '':
            # Podwójna spacja oznacza spację między słowami
            continue
        else:
            # Jeśli kod nie jest obsługiwany, pozostawiamy go bez zmian
            text.append(morse_char)
    
    # Łączymy znaki w tekst i zastępujemy znak '/' spacją
    result = ''.join(text)
    return result.replace('/', ' ')

# Funkcja testowa
if __name__ == "__main__":
    test_text = "HELLO WORLD"
    morse = text_to_morse(test_text)
    print(f"Tekst: {test_text} -> Morse: {morse}")
    
    decoded = morse_to_text(morse)
    print(f"Morse: {morse} -> Tekst: {decoded}")