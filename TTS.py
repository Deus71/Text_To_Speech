import tkinter as tk
from tkinter import filedialog
from gtts import gTTS
import tempfile
import threading
import pygame

pygame.mixer.init()

tts = None  # Inicjalizujemy zmienną tts na None
stop_thread = True  # Zmienna do zatrzymywania wątku odczytu
paused = False  # Zmienna do śledzenia stanu pauzy

def wczytaj_plik():
    global stop_thread
    global paused
    stop_thread = True  # Zatrzymujemy wątek, jeśli był aktywny
    paused = False

    nazwa_pliku = filedialog.askopenfilename(filetypes=[("Pliki tekstowe", "*.txt")])
    if nazwa_pliku:
        try:
            with open(nazwa_pliku, 'r', encoding='utf-8') as plik:
                zawartosc = plik.read()
                tekst.config(state="normal")
                tekst.delete("1.0", "end")
                tekst.insert("1.0", zawartosc)
                tekst.config(state="disabled")
                wynik.config(text="")
        except FileNotFoundError:
            wynik.config(text="Plik nie został znaleziony.")
        except Exception as e:
            wynik.config(text="Wystąpił błąd: " + str(e))

def czytaj_zawartosc():
    global tts
    global stop_thread
    global paused

    zawartosc = tekst.get("1.0", "end")
    if zawartosc.strip():
        try:
            if not tts or stop_thread:
                tts = gTTS(text=zawartosc, lang='pl')
                tts.save("temp.mp3")
                pygame.mixer.music.load("temp.mp3")
                pygame.mixer.music.play()
            else:
                if stop_thread:
                    tts = gTTS(text=zawartosc, lang='pl')
                    tts.save("temp.mp3")
                    pygame.mixer.music.load("temp.mp3")
                    pygame.mixer.music.play()
                else:
                    if paused:
                        pygame.mixer.music.unpause()  # Wznawiamy odczytywanie tekstu
                        paused = False
                    else:
                        pygame.mixer.music.pause()  # Pauzujemy odczytywanie tekstu
                        paused = True
        except Exception as e:
            wynik.config(text="Wystąpił błąd: " + str(e))
    else:
        wynik.config(text="Brak tekstu do odczytania.")

def koniec_czytania():
    global tts
    pygame.mixer.music.stop()  # Przerywamy odczytywanie tekstu
    tts = None  # Resetujemy tts na None

# Tworzymy główne okno aplikacji
root = tk.Tk()
root.title("Odczyt pliku tekstowego")

# Tworzymy przycisk do wyboru pliku
wybierz_plik_btn = tk.Button(root, text="Wybierz plik", command=wczytaj_plik)
wybierz_plik_btn.pack()

# Tworzymy pole tekstowe do wyświetlenia zawartości pliku
tekst = tk.Text(root, wrap=tk.WORD, state="disabled")
tekst.pack()

# Tworzymy etykietę na ewentualne komunikaty o błędach
wynik = tk.Label(root, text="", fg="red")
wynik.pack()

# Tworzymy ramkę na przyciski
przyciski_ramka = tk.Frame(root)
przyciski_ramka.pack()

# Tworzymy przycisk "Czytaj"
czytaj_btn = tk.Button(przyciski_ramka, text="Czytaj", command=czytaj_zawartosc)
czytaj_btn.pack(side="left")

# Tworzymy przycisk "Pauza"
pauza_btn = tk.Button(przyciski_ramka, text="Pauza", command=czytaj_zawartosc)
pauza_btn.pack(side="left")

# Tworzymy przycisk "Koniec"
koniec_btn = tk.Button(przyciski_ramka, text="Koniec", command=koniec_czytania)
koniec_btn.pack(side="left")

root.mainloop()

