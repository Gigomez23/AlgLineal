import customtkinter as ctk
from CTkTable import *


class HistorialVisualizacionPopup3(ctk.CTkToplevel):
    def __init__(self, parent, historial, indice, *args, **kwargs):
        """
        Ventana emergente que muestra las matrices de entrada y solución para importar.

        Args:
            parent: El widget padre donde se inserta la ventana.
            historial: Lista de matrices guardadas en el historial.
            indice: (int) Numero que representa la posición de la matriz seleccionada.
            callback_importar: Función que se llama cuando se selecciona una matriz para importar.
        """
        super().__init__(parent, *args, **kwargs)
        self.title("Visualización de Problema")  # Título de la ventana emergente
        # self.callback_importar = callback_importar  # Callback para enviar la matriz seleccionada

        # Inicialización de atributos
        self.problema = historial.problemas
        self.matriz1 = self.problema[indice]["matriz entrada 1"]
        self.matriz2 = self.problema[indice]["matriz entrada 2"]
        self.matriz3 = self.problema[indice]["matriz entrada 3"]
        self.matriz_solucion = self.problema[indice]["solucion"]
        self.matriz_importar = None  # Inicializado a None

        # Crear los frames
        self.frame1 = ctk.CTkFrame(self)
        self.frame1.grid(row=0, column=0, padx=10, pady=10)

        self.frame2 = ctk.CTkFrame(self)
        self.frame2.grid(row=0, column=1, padx=10, pady=10)

        self.frame3 = ctk.CTkFrame(self)
        self.frame3.grid(row=0, column=2, padx=10, pady=10)

        self.frame4 = ctk.CTkFrame(self)
        self.frame4.grid(row=0, column=3, padx=10, pady=10)

        # Crear los labels
        self.label_importar1 = ctk.CTkLabel(self.frame1, text="Entrada 1:")
        self.label_importar1.pack(padx=10, pady=10)

        self.label_importar2 = ctk.CTkLabel(self.frame2, text="Entrada 2:")
        self.label_importar2.pack(padx=10, pady=10)

        self.label_importar3 = ctk.CTkLabel(self.frame3, text="Entrada 3:")
        self.label_importar3.pack(padx=10, pady=10)

        self.label_importar_solucion = ctk.CTkLabel(self.frame4, text="Solucion:")
        self.label_importar_solucion.pack(padx=10, pady=10)

        # Crear las tablas
        datos_tabla_1 = self.matriz1
        self.tabla1 = CTkTable(self.frame1, values=datos_tabla_1)
        self.tabla1.pack(padx=10, pady=10)

        datos_tabla_2 = self.matriz2
        self.tabla2 = CTkTable(self.frame2, values=datos_tabla_2)
        self.tabla2.pack(padx=10, pady=10)

        datos_tabla_3 = self.matriz3
        self.tabla3 = CTkTable(self.frame3, values=datos_tabla_3)
        self.tabla3.pack(padx=10, pady=10)

        datos_tabla_solucion = self.matriz_solucion
        self.tabla_solucion = CTkTable(self.frame4, values=datos_tabla_solucion)
        self.tabla_solucion.pack(padx=10, pady=10)

