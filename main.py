import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame
import os
from listas import ListaReproduccion 
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from io import BytesIO

# INICIALIZACIÓN 
pygame.mixer.init()
Canciones = ListaReproduccion()
pausado = False 

# CONFIGURACIÓN DE VENTANA 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
ventana = ctk.CTk()
ventana.title("Reproductor Cool")
ventana.geometry("1080x720")

# ETIQUETAS PRINCIPALES 
label_cancion = ctk.CTkLabel(
    ventana, text="Ninguna canción cargada",
    text_color="white", font=ctk.CTkFont("Arial", 20, weight="bold")
)
label_cancion.pack(pady=40)

caratula_label = ctk.CTkLabel(ventana, text="")
caratula_label.pack(pady=50)
nombre_cancion_label = ctk.CTkLabel(ventana, text="", text_color="white", font=ctk.CTkFont("Arial", 16))
nombre_cancion_label.pack(pady=5)

#  ÍCONOS 
def cargar_icono(ruta, tamaño=(60, 60)):
    img = Image.open(ruta).resize(tamaño)
    return ImageTk.PhotoImage(img)

iconos = {
    "play": cargar_icono("path_to_play_image.png"),
    "pause": cargar_icono("path_to_pause_image.png"),
    "next": cargar_icono("path_to_next_image.png"),
    "prev": cargar_icono("anterior.png"),
    "shuffle": cargar_icono("path_to_shuffle_image.png"),
    "repeat": cargar_icono("path_to_repeat_image.png"),
    "folder": cargar_icono("folder.png")
}

# INDICADORES DE MODOS 
etiqueta_shuffle = ctk.CTkLabel(ventana, text="🔀", text_color="white", font=ctk.CTkFont(size=20))
etiqueta_repeat = ctk.CTkLabel(ventana, text="🔁", text_color="white", font=ctk.CTkFont(size=20))
etiqueta_shuffle.place_forget()
etiqueta_repeat.place_forget()

# FUNCIONES DE UTILIDAD 
def obtener_carátula_mp3(ruta_mp3):
    try:
        audio = MP3(ruta_mp3, ID3=ID3)
        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                return Image.open(BytesIO(tag.data))
    except Exception as e:
        print(f"No se pudo leer la carátula: {e}")
    return None

# FUNCIONES DE REPRODUCCIÓN 
def cambiar_play_pause():
    global pausado
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        pausado = True
        play_button.configure(image=iconos["play"], command=cambiar_play_pause)
    else:
        pygame.mixer.music.unpause()
        pausado = False
        play_button.configure(image=iconos["pause"], command=cambiar_play_pause)

def reproducir_cancion():
    if Canciones.cabeza:
        pygame.mixer.music.load(Canciones.cabeza.ruta_audio)
        pygame.mixer.music.play()
        label_cancion.configure(text="")  # Oculta el texto grande
        nombre_cancion_label.configure(text=Canciones.cabeza.nombre)
        play_button.configure(image=iconos["pause"], command=cambiar_play_pause)
        img = obtener_carátula_mp3(Canciones.cabeza.ruta_audio)
        if img:
            img = img.resize((300, 300))
            img_tk = ImageTk.PhotoImage(img)
            caratula_label.configure(image=img_tk, text="")
            caratula_label.image = img_tk
        else:
            caratula_label.configure(image=None, text="Sin carátula")

def pause_cancion():
    pygame.mixer.music.pause()
    play_button.configure(image=iconos["play"], command=cambiar_play_pause)

def detener_cancion():
    pygame.mixer.music.stop()
    label_cancion.configure(text="Canción detenida")
    play_button.configure(image=iconos["play"], command=reproducir_cancion)

# FUNCIONES DE LISTA 
def agregar_cancion():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de audio", "*.mp3;*.wav")])
    if archivo:
        nombre = os.path.basename(archivo)
        artista = "Desconocido"
        duracion = "3:00"
        Canciones.agregar_cancion(nombre, artista, duracion, archivo)
        label_cancion.configure(text=f"Canción '{nombre}' agregada")
        img = obtener_carátula_mp3(archivo)
        if img:
            img = img.resize((300, 300))
            img_tk = ImageTk.PhotoImage(img)
            caratula_label.configure(image=img_tk, text="")
            caratula_label.image = img_tk
        else:
            caratula_label.configure(image=None, text="Sin carátula")

def eliminar_cancion():
    if Canciones.cabeza:
        nombre = Canciones.cabeza.nombre
        Canciones.eliminar_cancion(nombre)
        label_cancion.configure(text=f"Canción '{nombre}' eliminada")
        nombre_cancion_label.configure(text="")
        label_cancion.configure(text="Ninguna canción cargada")
        caratula_label.configure(image=None, text="Sin carátula")
        if Canciones.cabeza:
            reproducir_cancion()
        else:
            label_cancion.configure(text="Ninguna canción cargada")

def cargar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        for archivo in os.listdir(carpeta):
            if archivo.endswith(('.mp3', '.wav')):
                ruta_audio = os.path.join(carpeta, archivo)
                nombre = os.path.basename(ruta_audio)
                artista = "Desconocido"
                duracion = "3:00"
                Canciones.agregar_cancion(nombre, artista, duracion, ruta_audio)
        label_cancion.configure(text="Canciones cargadas desde la carpeta")

# FUNCIONES DE MODO Y NAVEGACIÓN 
def toggle_aleatorio():
    Canciones.activar_aleatorio()
    if Canciones.modo_aleatorio:
        shuffle_button.configure(fg_color="#666666")  # Gris cuando está activo
    else:
        shuffle_button.configure(fg_color="black")

def toggle_repetir():
    Canciones.activar_repetir()
    if Canciones.modo_repetir:
        repeat_button.configure(fg_color="#666666")
    else:
        repeat_button.configure(fg_color="black")

def siguiente_cancion():
    Canciones.siguiente_cancion()
    reproducir_cancion()

def cancion_anterior():
    Canciones.anterior_cancion()
    reproducir_cancion()

def verificar_estado():
    if Canciones.cabeza and not pygame.mixer.music.get_busy() and not pausado:
        siguiente_cancion()
    ventana.after(1000, verificar_estado)

# BOTONES DESPLEGABLES 
#  Botón flotante desplegable (esquina inferior derecha) 
botonera_frame = ctk.CTkFrame(ventana, fg_color="transparent", width=60, height=240)
botonera_frame.place(relx=1.0, rely=1.0, anchor="se", x=-30, y=-30)



#  BOTONERA PRINCIPAL DE REPRODUCCIÓN 
frame_botones = ctk.CTkFrame(ventana, fg_color="transparent")
frame_botones.pack(pady=30)
ctk.CTkButton(frame_botones, image=iconos["prev"], text="", width=30, height=60,
              fg_color="black", hover_color="#333333", corner_radius=10, border_width=0,
              command=cancion_anterior).grid(row=0, column=1, padx=10)

play_button = ctk.CTkButton(frame_botones, image=iconos["play"], text="", width=60, height=60,
              fg_color="black", hover_color="#333333", corner_radius=10, border_width=0,
              command=reproducir_cancion)
play_button.grid(row=0, column=2, padx=10)

ctk.CTkButton(frame_botones, image=iconos["next"], text="", width=60, height=60,
              fg_color="black", hover_color="#333333", corner_radius=10, border_width=0,
              command=siguiente_cancion).grid(row=0, column=3, padx=10)
shuffle_button = ctk.CTkButton(frame_botones, image=iconos["shuffle"], text="", width=60, height=60,
    fg_color="black", hover_color="#333333", corner_radius=10, border_width=0,
    command=toggle_aleatorio)
shuffle_button.grid(row=0, column=0, padx=10)

repeat_button = ctk.CTkButton(frame_botones, image=iconos["repeat"], text="", width=60, height=60,
    fg_color="black", hover_color="#333333", corner_radius=10, border_width=0,
    command=toggle_repetir)
repeat_button.grid(row=0, column=4, padx=10)
# BOTONES INFERIORES IZQUIERDA 
frame_inferior = ctk.CTkFrame(ventana, fg_color="transparent")
frame_inferior.place(relx=0.0, rely=1.0, anchor="sw", x=20, y=-20)

btn_agregar = ctk.CTkButton(frame_inferior, text="🎵", width=50, height=50,
                             fg_color="black", corner_radius=25, command=agregar_cancion)
btn_folder = ctk.CTkButton(frame_inferior, text="📂", width=50, height=50,
                             fg_color="black", corner_radius=25, command=cargar_carpeta)
btn_eliminar = ctk.CTkButton(frame_inferior, text="🚮", width=50, height=50,
                              fg_color="black", corner_radius=25, command=eliminar_cancion)

btn_agregar.grid(row=0, column=0, padx=10)
btn_folder.grid(row=0, column=1, padx=10)
btn_eliminar.grid(row=0, column=2, padx=10)

verificar_estado()
ventana.mainloop()
