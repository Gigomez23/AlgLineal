import customtkinter as ctk
from fractions import Fraction
from customtkinter import CTkButton
from funciones_adicionales.dropdown_menu import CTkFloatingWindow
from funciones_adicionales.convertir_formato_lista import *


class FrameEntradaMatriz(ctk.CTkFrame):
    def __init__(self, padre):
        super().__init__(padre)

        # Frame superior para las entradas de dimensiones y botón
        self.frame_dimensiones = ctk.CTkFrame(self)
        self.frame_dimensiones.pack(pady=10)

        # Etiquetas y entradas para filas y columnas (alineadas horizontalmente)
        self.etiqueta_filas = ctk.CTkLabel(self.frame_dimensiones, text="Filas:")
        self.etiqueta_filas.grid(row=0, column=0, padx=5)

        self.entrada_filas = ctk.CTkEntry(self.frame_dimensiones, width=50)
        self.entrada_filas.grid(row=0, column=1, padx=5)
        self.entrada_filas.insert(0, "3")

        self.etiqueta_columnas = ctk.CTkLabel(self.frame_dimensiones, text="Columnas:")
        self.etiqueta_columnas.grid(row=0, column=2, padx=5)

        self.entrada_columnas = ctk.CTkEntry(self.frame_dimensiones, width=50)
        self.entrada_columnas.grid(row=0, column=3, padx=5)
        self.entrada_columnas.insert(0, "3")

        self.boton_establecer_matriz = ctk.CTkButton(
            self.frame_dimensiones, text="Establecer Matriz", command=self.establecer_matriz
        )
        self.boton_establecer_matriz.grid(row=0, column=4, padx=10)

        # Frame inferior para la matriz
        self.frame_matriz = ctk.CTkFrame(self)
        self.frame_matriz.pack(pady=20)

        menu_popup = CTkFloatingWindow(self.frame_matriz)  # menu popup

        self.frame_matriz.bind("<Button-3>", lambda event: do_popup(event, menu_popup))
        self.frame_matriz.bind("<Button-2>", lambda event: do_popup(event, menu_popup))

        # Add menu buttons in menu_popup.frame

        popup_boton = CTkButton(menu_popup.frame, text="Agregar Fila", fg_color="transparent",
                                command=self.agregar_fila)
        popup_boton.pack(expand=True, fill="x", padx=10, pady=(10, 0))

        popup_boton2 = CTkButton(menu_popup.frame, text="Eliminar Fila", fg_color="transparent",
                                 command=self.eliminar_fila)
        popup_boton2.pack(expand=True, fill="x", padx=10, pady=(5, 0))

        popup_boton3 = CTkButton(menu_popup.frame, text="Agregar Columna", fg_color="transparent",
                                 command=self.agregar_columna)
        popup_boton3.pack(expand=True, fill="x", padx=10, pady=(5, 10))

        popup_boton4 = CTkButton(menu_popup.frame, text="Eliminar Columna", fg_color="transparent",
                                 command=self.eliminar_columna)
        popup_boton4.pack(expand=True, fill="x", padx=10, pady=(5, 10))

        # Inicializar variables y construir matriz inicial
        self.filas = 3
        self.columnas = 3
        self.matriz = []
        self.construir_matriz()

    def establecer_matriz_para_multiplicacion(self, otro_marco):
        """
        Ajusta las dimensiones de este marco y otro para que las matrices sean multiplicables.
        La cantidad de columnas de esta matriz se igualará con las filas del otro marco.
        """
        self.columnas = otro_marco.filas  # Ajustar columnas de esta matriz
        self.entrada_columnas.delete(0, ctk.END)
        self.entrada_columnas.insert(0, str(self.columnas))

        otro_marco.filas = self.columnas  # Asegurar que coincidan las dimensiones
        otro_marco.entrada_filas.delete(0, ctk.END)
        otro_marco.entrada_filas.insert(0, str(otro_marco.filas))

        # Reconstruir ambas matrices con las nuevas dimensiones
        self.construir_matriz()
        otro_marco.construir_matriz()

    def agregar_fila(self):
        """Agrega una nueva fila vacía al final de la matriz."""
        self.filas += 1
        self.entrada_filas.delete(0, ctk.END)
        self.entrada_filas.insert(0, str(self.filas))
        nueva_fila = [ctk.CTkEntry(self.frame_matriz, width=50) for _ in range(self.columnas)]
        for c, entrada in enumerate(nueva_fila):
            entrada.grid(row=self.filas - 1, column=c, padx=5, pady=5)
        self.matriz.append(nueva_fila)

    def eliminar_fila(self):
        """Elimina la última fila de la matriz si es posible."""
        if self.filas > 1:
            for entrada in self.matriz.pop():
                entrada.destroy()
            self.filas -= 1
            self.entrada_filas.delete(0, ctk.END)
            self.entrada_filas.insert(0, str(self.filas))

    def agregar_columna(self):
        """Agrega una nueva columna vacía al final de cada fila."""
        self.columnas += 1
        self.entrada_columnas.delete(0, ctk.END)
        self.entrada_columnas.insert(0, str(self.columnas))
        for r, fila in enumerate(self.matriz):
            entrada = ctk.CTkEntry(self.frame_matriz, width=50)
            entrada.grid(row=r, column=self.columnas - 1, padx=5, pady=5)
            fila.append(entrada)

    def eliminar_columna(self):
        """Elimina la última columna de la matriz si es posible."""
        if self.columnas > 1:
            for fila in self.matriz:
                entrada = fila.pop()
                entrada.destroy()
            self.columnas -= 1
            self.entrada_columnas.delete(0, ctk.END)
            self.entrada_columnas.insert(0, str(self.columnas))

    def establecer_matriz(self):
        """Establece las dimensiones de la matriz según las entradas del usuario."""
        try:
            self.filas = int(self.entrada_filas.get())
            self.columnas = int(self.entrada_columnas.get())

            if self.filas <= 0 or self.columnas <= 0:
                raise ValueError("Las dimensiones deben ser enteros positivos")

            self.construir_matriz()

        except ValueError as e:
            print(f"Error: {e}. Por favor, ingrese enteros positivos válidos.")

    def construir_matriz(self):
        """Construye o reconstruye la matriz en el frame."""
        for widget in self.frame_matriz.winfo_children():
            widget.destroy()

        self.matriz = []
        for r in range(self.filas):
            fila = []
            for c in range(self.columnas):
                entrada = ctk.CTkEntry(self.frame_matriz, width=50)
                entrada.grid(row=r, column=c, padx=5, pady=5)
                entrada.bind("<space>", lambda e, row=r, col=c: self.focus_siguiente_entrada(row, col))
                fila.append(entrada)
            self.matriz.append(fila)

    def focus_siguiente_entrada(self, fila_actual, columna_actual):
        """Mueve el foco a la siguiente entrada al presionar espacio."""
        siguiente_columna = columna_actual + 1
        siguiente_fila = fila_actual

        if siguiente_columna >= self.columnas:
            siguiente_columna = 0
            siguiente_fila += 1

        if siguiente_fila < self.filas:
            siguiente_entrada = self.matriz[siguiente_fila][siguiente_columna]
            siguiente_entrada.focus_set()

    def obtener_matriz_como_array(self):
        """Devuelve los valores de la matriz como un array de fracciones."""
        matriz_array = []
        for fila in self.matriz:
            datos_fila = []
            for entrada in fila:
                valor = entrada.get()
                try:
                    fraccion = Fraction(valor)  # Convertir a fracción
                except ValueError:
                    fraccion = Fraction(0)  # Valor predeterminado en caso de error
                datos_fila.append(fraccion)
            matriz_array.append(datos_fila)
        return matriz_array

    def clonar_dimensiones(self, filas, columnas):
        """Clona las dimensiones y reconstruye la matriz en este frame."""
        self.filas = filas
        self.columnas = columnas

        # Establecer las dimensiones en las entradas correspondientes.
        self.entrada_filas.delete(0, ctk.END)
        self.entrada_filas.insert(0, str(filas))

        self.entrada_columnas.delete(0, ctk.END)
        self.entrada_columnas.insert(0, str(columnas))

        # Reconstruir la matriz según las nuevas dimensiones.
        self.construir_matriz()

    def limpiar_entradas(self):
        """Limpia todas las entradas de la matriz y las dimensiones."""
        # Limpiar las entradas de filas y columnas
        self.entrada_filas.delete(0, ctk.END)
        self.entrada_filas.insert(0, "3")

        self.entrada_columnas.delete(0, ctk.END)
        self.entrada_columnas.insert(0, "3")

        # Limpiar las entradas de la matriz
        for fila in self.matriz:
            for entrada in fila:
                entrada.delete(0, ctk.END)

    def importar_desde_historial(self, matriz_array):
        """Importa una matriz desde un historial y la coloca en las entradas."""
        matriz = matriz_array
        filas = len(matriz)
        columnas = len(matriz[0]) if filas > 0 else 0

        self.filas = filas
        self.columnas = columnas

        # Establecer las dimensiones en las entradas correspondientes.
        self.entrada_filas.delete(0, ctk.END)
        self.entrada_filas.insert(0, str(filas))

        self.entrada_columnas.delete(0, ctk.END)
        self.entrada_columnas.insert(0, str(columnas))

        # Reconstruir la matriz según las nuevas dimensiones.
        self.construir_matriz()

        # Colocar los valores importados en las entradas de la matriz.
        for r in range(filas):
            for c in range(columnas):
                valor = matriz[r][c]
                valor_num = valor  # Se usa directamente como Fraction.

                # Insertar el valor en el TextBox como string.
                self.matriz[r][c].insert(0, str(valor_num))

def do_popup(event, frame):
    """ open the popup menu """
    try:
        frame.popup(event.x_root, event.y_root)
    finally:
        frame.grab_release()


class Aplicacion(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación Principal con MarcoMatriz")
        self.geometry("600x600")
        self.ejemplo = [[10, 3, 4], [12, 1/9, 3.5]]

        # Crear la primera instancia del frame de entrada de matriz.
        self.marco_matriz = FrameEntradaMatriz(self)
        self.marco_matriz.pack(pady=20)

        # Botón para obtener los datos de la matriz.
        self.boton_obtener_datos_matriz = ctk.CTkButton(
            self, text="Obtener Datos de la Matriz", command=self.obtener_datos_matriz
        )
        self.boton_obtener_datos_matriz.pack(pady=10)

        # Botón para limpiar las entradas.
        self.boton_limpiar = ctk.CTkButton(
            self, text="Limpiar Entradas", command=self.marco_matriz.limpiar_entradas
        )
        self.boton_limpiar.pack(pady=10)

        # Botón para clonar el frame de entrada.
        self.boton_clonar = ctk.CTkButton(
            self, text="Clonar Frame", command=self.clonar_frame_matriz
        )
        self.boton_clonar.pack(pady=10)

    def obtener_datos_matriz(self):
        """Imprime los datos de la matriz como un array de fracciones."""
        datos_matriz = self.marco_matriz.obtener_matriz_como_array()
        print(datos_matriz)

    def clonar_frame_matriz(self):
        """Clona el frame de entrada con las mismas dimensiones que el original."""
        filas = self.marco_matriz.filas
        columnas = self.marco_matriz.columnas

        # Crear una nueva instancia del frame de entrada.
        nuevo_marco_matriz = FrameEntradaMatriz(self)
        nuevo_marco_matriz.clonar_dimensiones(filas, columnas)
        nuevo_marco_matriz.pack(pady=20)

