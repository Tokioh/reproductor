import random

class NodoCancion:
    def __init__(self, nombre, artista, duracion, ruta_audio):
        self.nombre = nombre  
        self.artista = artista 
        self.duracion = duracion  
        self.ruta_audio = ruta_audio  
        self.siguiente = None
        self.anterior = None

class ListaReproduccion:
    def __init__(self):
        self.cabeza = None
        self.modo_repetir = False
        self.modo_aleatorio = False

    def agregar_cancion(self, nombre, artista, duracion, ruta_audio):
        nueva_cancion = NodoCancion(nombre, artista, duracion, ruta_audio)
        if self.cabeza is None:
            self.cabeza = nueva_cancion
            nueva_cancion.siguiente = nueva_cancion
            nueva_cancion.anterior = nueva_cancion
        else:
            cola = self.cabeza.anterior
            cola.siguiente = nueva_cancion
            nueva_cancion.anterior = cola
            nueva_cancion.siguiente = self.cabeza
            self.cabeza.anterior = nueva_cancion

    def mostrar_lista(self):
        if self.cabeza is None:
            print("La lista está vacía.")
            return

        actual = self.cabeza
        while True:
            print(f"Nombre: {actual.nombre}, Artista: {actual.artista}, Duración: {actual.duracion}, Ruta: {actual.ruta_audio}")
            actual = actual.siguiente
            if actual == self.cabeza:
                break

    def eliminar_cancion(self, nombre):
        if self.cabeza is None:
            print("La lista está vacía.")
            return

        actual = self.cabeza
        while True:
            if actual.nombre == nombre:
                if actual.siguiente == actual:  
                    self.cabeza = None
                else:
                    actual.anterior.siguiente = actual.siguiente
                    actual.siguiente.anterior = actual.anterior
                    if actual == self.cabeza:
                        self.cabeza = actual.siguiente
                del actual
                print(f"Canción '{nombre}' eliminada.")
                return
            actual = actual.siguiente
            if actual == self.cabeza:
                break

        print("Canción no encontrada.")

    def activar_repetir(self):
        self.modo_repetir = not self.modo_repetir

    def activar_aleatorio(self):
        self.modo_aleatorio = not self.modo_aleatorio

    def siguiente_cancion(self):
        if not self.cabeza:
            return
        if self.modo_repetir:
            return self.cabeza
        elif self.modo_aleatorio:
            canciones = []
            actual = self.cabeza
            while True:
                canciones.append(actual)
                actual = actual.siguiente
                if actual == self.cabeza:
                    break
            self.cabeza = random.choice(canciones)
        else:
            self.cabeza = self.cabeza.siguiente
        return self.cabeza

    def anterior_cancion(self):
        if not self.cabeza:
            return None
        if self.modo_repetir:
            return self.cabeza
        elif self.modo_aleatorio:
            canciones = []
            actual = self.cabeza
            while True:
                canciones.append(actual)
                actual = actual.siguiente
                if actual == self.cabeza:
                    break
            self.cabeza = random.choice(canciones)
        else:
            self.cabeza = self.cabeza.anterior
        return self.cabeza
        