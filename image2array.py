"""
Created on 12th June 2024

@author: raiktin on GitHub
@version: 1.2

Nutzung:

    Wenn man das Programm startet erscheint eine Benutzeroberflaeche, dort kann man eine Bilddatei
    hochladen um diese in eine .txt-Datei zu konvertieren, welche das Bild als Array darstellt. Laedt man eine
    solche .txt-Datei hoch, transformiert das Programe diese wieder zu einem Bild zurueck


Installation:

    Man benoetigt die verschiedenen Bibliotheken damit das Programm laeuft, dafür sollte man erstmal
    versuchen diese ueber die IDE zu installieren (drüber hovern -> install package)
    Es kann allerdings vorkommen, dass PIL (pillow) Probleme macht, Fix siehe 'PIL fix'


PIL fix:

    Folgenden Befehl in das Terminal schreiben:

        'py -m pip install --upgrade Pillow'

    Sollten hier Probleme auftreten wird es vermutlich an pip liegen, ab hier muss man individuell schauen was die
    Fehlermeldungen sagen. Exemplarisch kann man unter 'pip fix' eine grobe Anleitung finden


pip fix:

    Zunaechst wechselt man im Terminal zu dem Ordner wo man lokal python gespeichert hat

        'cd C:\\Users\\*username here*\\AppData\\Local\\Programs\\Python\\Python312\\' bei mir unter Windows

    Danach installiert man pip (auch wieder im Terminal)

        'py -m pip install --upgrade pip'

    Danache sollte man Pillow installieren können

"""


import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import numpy as np
import os


def load_greyscale(path):
    return Image.open(path).convert('L')


def resize_image(image, size):
    if size == 0:
        if image.size[0] >= image.size[1]:
            powerof2 = np.log2(image.size[1])
        else:
            powerof2 = np.log2(image.size[0])
        return image.resize((2 ** int(powerof2), 2 ** int(powerof2)), Image.LANCZOS)
    else:
        return image.resize((size, size), Image.LANCZOS)


def image_to_array(image):
    return np.resize(np.asarray(image.getdata(), dtype=np.uint8), (image.size[1], image.size[0]))


def write_array(array, path):
    array1D = np.resize(array, (int(len(array) ** 2),))
    with open(path, 'w') as f:
        f.write(str(len(array1D)) + "\n")
        for i in range(len(array1D)):
            f.write(f"{i}\t{array1D[i]} 0\n")


def array_to_image(array):
    if isinstance(array.size, int):
        resolution = int(np.sqrt(len(array)))
        array_2d = np.resize(array, (resolution, resolution))
        return Image.fromarray(array_2d, mode='L')
    else:
        return Image.fromarray(array, mode='L')


def read_array(path):
    array1D = []
    with open(path, "r") as f:
        lines = f.readlines()
        lines.pop(0)
        for line in lines:
            value = round(float(line.split()[1]))
            if value < 0:
                array1D.append(0)
            elif value > 255:
                array1D.append(255)
            else:
                array1D.append(value)
    return np.resize(np.asarray(array1D, dtype=np.uint8), (len(array1D),))

def upload_files():
    global file_paths
    file_paths = filedialog.askopenfilenames(title="Wähle Dateien aus", filetypes=[("Alle Dateien", "*.*"), ("Textdateien", "*.txt"), ("Bilddateien", "*.bmp *.png *.jpg")])
    if file_paths:
        file_list_label.config(text="\n".join([os.path.basename(path) for path in file_paths]))


def transform():
    if not file_paths:
        messagebox.showerror("Fehler", "Bitte lade zuerst Dateien hoch.")
        return

    size = int(resolution_var.get())
    if size == 0:
        messagebox.showerror("Fehler", "Bitte wähle zuerst eine Auflösung aus.")
        return

    for path in file_paths:
        ext = os.path.splitext(path)[1].lower()
        if ext == '.txt':
            array = read_array(path)
            image = array_to_image(array)
            new_path = os.path.splitext(path)[0] + "_.png"
            image.save(new_path)
        elif ext in ['.png', '.jpg', '.jpeg', '.bmp']:
            image = load_greyscale(path)
            image = resize_image(image, size)
            array = image_to_array(image)
            new_path = os.path.splitext(path)[0] + ".txt"
            write_array(array, new_path)
        else:
            messagebox.showerror("Fehler", f"Ungültige Datei: {path}")
            continue

    messagebox.showinfo("Erfolgreich", "Transformation aller Dateien war erfolgreich.")


root = tk.Tk()
root.title("Bild-Daten-Transformation")

label = tk.Label(root,
                 text="Transformation eines (Grau-)Bilds (*.bmp, *.png, *.jpg) in eine Datendatei (*.txt) und umgekehrt")
label.pack(pady=10)

upload_button = tk.Button(root, text="Dateien hochladen", command=upload_files)
upload_button.pack(pady=20)

file_list_label = tk.Label(root, text="Keine Dateien ausgewählt")
file_list_label.pack(pady=5)

resolution_label = tk.Label(root, text="Wähle eine Auflösung (quadratisch):")
resolution_label.pack(pady=10)

resolution_var = tk.StringVar()
resolution_combobox = ttk.Combobox(root, textvariable=resolution_var, state="readonly")
resolution_combobox['values'] = [2 ** x for x in range(4, 13)]
resolution_combobox.current(2)  # Set default value to 16
resolution_combobox.pack(pady=10)

transform_button = tk.Button(root, text="Transformieren", command=transform)
transform_button.pack(pady=20)

file_paths = []

root.mainloop()