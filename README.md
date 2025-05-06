# 🎧 Reproductor Cool – Music Player GUI en Python

Este proyecto es un reproductor de música gráfico desarrollado con `CustomTkinter`, `pygame` y `mutagen`, que permite reproducir archivos `.mp3` o `.wav`, mostrar carátulas de álbumes y gestionar una lista circular doblemente enlazada con funciones como: reproducir, pausar, siguiente, anterior, eliminar, cargar carpetas, modo aleatorio y repetir.

---

## 📸 Características principales

- Interfaz moderna con CustomTkinter (modo oscuro).
- Reproduce canciones `.mp3` y `.wav`.
- Muestra carátula del álbum automáticamente.
- Lista de reproducción con navegación circular.
- Controles visuales (Play, Pause, Next, Previous).
- Modo aleatorio y modo repetir.
- Carga individual o masiva desde carpetas.

---

## ⚠️ IMPORTANTE

Para que el reproductor funcione correctamente:

1. **Asegúrate de tener todos los íconos en la misma carpeta o actualiza las rutas** dentro del diccionario `iconos`.
2. **El archivo `listas.py` debe contener la clase `ListaReproduccion` implementada correctamente** (con funciones como `agregar_cancion`, `eliminar_cancion`, `siguiente_cancion`, `anterior_cancion`, etc.).
3. **Solo se admiten archivos `.mp3` y `.wav`.**
4. Las carátulas solo se mostrarán si el archivo `.mp3` contiene una imagen embebida en sus metadatos ID3 (APIC).
5. El programa fue diseñado con resolución 1080x720. Si tienes una pantalla más pequeña, algunos elementos podrían desalinearse.

---

## 🧰 Librerías necesarias

Antes de ejecutar el programa, instala estas dependencias con `pip`:

```bash
pip install customtkinter pygame pillow mutagen
