"""
Archivo: historial_importar_popup.py 1.0.0
Descripción: popup que muesta las entrada y la solución del problema para poder importar.
"""
import customtkinter as ctk
from CTkTable import *
from CTkToolTip import *


class HistorialImportarPopup(ctk.CTkToplevel):
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
        self.matriz4 = self.problema[indice]["matriz entrada 4"]
        self.matriz_solucion = self.problema[indice]["solucion"]
        self.matriz_importar = []  # Inicializado a None

        if self.matriz1 is not None:
            self.frame1 = ctk.CTkFrame(self)
            self.frame1.grid(row=0, column=0, padx=10, pady=10)

            self.label_importar1 = ctk.CTkLabel(self.frame1, text="Matriz/Vector 1:")
            self.label_importar1.pack(padx=10, pady=10)

            datos_tabla_1 = self.matriz1
            self.tabla1 = CTkTable(self.frame1, values=datos_tabla_1)
            self.tabla1.pack(padx=10, pady=10)

            self.btn_importar_matriz1 = ctk.CTkButton(self.frame1, text="Importar", command=self.importar_matriz1)
            self.btn_importar_matriz1.pack(padx=10, pady=10)
            self.tooltip_importar1 = CTkToolTip(self.btn_importar_matriz1,
                                                message="Importar datos de entrada 1")
        if self.matriz2 is not None:
            self.frame2 = ctk.CTkFrame(self)
            self.frame2.grid(row=0, column=1, padx=10, pady=10)

            self.label_importar2 = ctk.CTkLabel(self.frame2, text="Matriz/Vector 2:")
            self.label_importar2.pack(padx=10, pady=10)

            datos_tabla_2 = self.matriz2
            self.tabla2 = CTkTable(self.frame2, values=datos_tabla_2)
            self.tabla2.pack(padx=10, pady=10)

            self.btn_importar_matriz2 = ctk.CTkButton(self.frame2, text="Importar", command=self.importar_matriz2)
            self.btn_importar_matriz2.pack(padx=10, pady=10)
            self.tooltip_importar2 = CTkToolTip(self.btn_importar_matriz2,
                                                message="Importar datos de entrada 2")

        if self.matriz3 is not None:
            self.frame3 = ctk.CTkFrame(self)
            self.frame3.grid(row=0, column=2, padx=10, pady=10)

            self.label_importar3 = ctk.CTkLabel(self.frame3, text="Matriz/Vector 3:")
            self.label_importar3.pack(padx=10, pady=10)

            # Crear las tablas
            datos_tabla_3 = self.matriz3
            self.tabla3 = CTkTable(self.frame3, values=datos_tabla_3)
            self.tabla3.pack(padx=10, pady=10)

            self.btn_importar_matriz3 = ctk.CTkButton(self.frame3, text="Importar", command=self.importar_matriz3)
            self.btn_importar_matriz3.pack(padx=10, pady=10)
            self.tooltip_importar3 = CTkToolTip(self.btn_importar_matriz3,
                                                message="Importar datos de entrada 3")

        if self.matriz4 is not None:
            self.frame4 = ctk.CTkFrame(self)
            self.frame4.grid(row=0, column=2, padx=10, pady=10)

            self.label_importar4 = ctk.CTkLabel(self.frame4, text="Matriz/Vector 4:")
            self.label_importar4.pack(padx=10, pady=10)

            # Crear las tablas
            datos_tabla_4 = self.matriz4
            self.tabla4 = CTkTable(self.frame4, values=datos_tabla_4)
            self.tabla4.pack(padx=10, pady=10)

            self.btn_importar_matriz4 = ctk.CTkButton(self.frame4, text="Importar", command=self.importar_matriz4)
            self.btn_importar_matriz4.pack(padx=10, pady=10)
            self.tooltip_importar4 = CTkToolTip(self.btn_importar_matriz4,
                                                message="Importar datos de entrada 4")

        if self.matriz_solucion is not None:
            self.frame_solucion = ctk.CTkFrame(self)
            self.frame_solucion.grid(row=0, column=4, padx=10, pady=10)

            # Crear los labels
            self.label_importar_solucion = ctk.CTkLabel(self.frame_solucion, text="Solucion:")
            self.label_importar_solucion.pack(padx=10, pady=10)

            datos_tabla_solucion = self.matriz_solucion
            self.tabla_solucion = CTkTable(self.frame_solucion, values=datos_tabla_solucion)
            self.tabla_solucion.pack(padx=10, pady=10)

            self.btn_importar_solucion = ctk.CTkButton(self.frame_solucion, text="Importar", command=self.importar_matriz_solucion)
            self.btn_importar_solucion.pack(padx=10, pady=10)
            self.tooltip_importar_solucion = CTkToolTip(self.btn_importar_solucion,
                                                        message="Importar datos de solución")

    def importar_matriz1(self):
        self.matriz_importar = self.matriz1
        self.destroy()  # Cierra el popup cuando se selecciona una matriz

    def importar_matriz2(self):
        self.matriz_importar = self.matriz2
        self.destroy()  # Cierra el popup cuando se selecciona una matriz

    def importar_matriz3(self):
        self.matriz_importar = self.matriz3
        self.destroy()  # Cierra el popup cuando se selecciona una matriz

    def importar_matriz4(self):
        self.matriz_importar = self.matriz4
        self.destroy()

    def importar_matriz_solucion(self):
        self.matriz_importar = self.matriz_solucion
        self.destroy()  # Cierra el popup cuando se selecciona una matriz