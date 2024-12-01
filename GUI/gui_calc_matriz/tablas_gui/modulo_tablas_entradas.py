"""
Archivo: modulo_tablas_entradas.py 1.0.8
Descripción: Diseño de modulo que contiene la propagación de las tablas.
"""
import customtkinter as ctk
from fractions import Fraction
from customtkinter import CTkButton
from CTkMessagebox import CTkMessagebox
from CTkTable import CTkTable
from funciones_adicionales.dropdown_menu import CTkFloatingWindow


class TablasFrame(ctk.CTkFrame):
    def __init__(self, padre, tabla1=None, tabla2=None, tabla3=None, tabla4=None,
                 texto1=None, texto2=None, texto3=None, texto4=None):
        super().__init__(padre)

        # se inicializan atributos
        self.tabla_matriz1 = tabla1
        self.tabla_matriz2 = tabla2
        self.tabla_matriz3 = tabla3
        self.tabla_matriz4 = tabla4
        self.texto1 = texto1
        self.texto2 = texto2
        self.texto3 = texto3
        self.texto4 = texto4

        # se inicializa el frame
        self.frame_entradas = ctk.CTkFrame(self)
        self.frame_entradas.pack(padx=10, pady=10)

        # se crean las tablas
        if self.tabla_matriz1 is not None:
            self.lbl_matriz1 = ctk.CTkLabel(self.frame_entradas, text=texto1, font=("Arial", 17))
            self.lbl_matriz1.pack(padx=10, pady=10)

            # tablas para la frame 1 que contiene los datos de entrada
            datos_tabla1 = self.tabla_matriz1  # Usamos la matriz original
            self.tabla1 = CTkTable(self.frame_entradas, values=datos_tabla1)
            self.tabla1.pack(padx=10, pady=10)

        if self.tabla_matriz2 is not None:
            self.lbl_matriz2 = ctk.CTkLabel(self.frame_entradas, text=texto2, font=("Arial", 17))
            self.lbl_matriz2.pack(padx=10, pady=10)

            # tablas para la frame 1 que contiene los datos de entrada
            datos_tabla2 = self.tabla_matriz2  # Usamos la matriz original
            self.tabla2 = CTkTable(self.frame_entradas, values=datos_tabla2)
            self.tabla2.pack(padx=10, pady=10)

        if self.tabla_matriz3 is not None:
            self.lbl_matriz3 = ctk.CTkLabel(self.frame_entradas, text=texto3, font=("Arial", 17))
            self.lbl_matriz3.pack(padx=10, pady=10)

            # tablas para la frame 1 que contiene los datos de entrada
            datos_tabla3 = self.tabla_matriz3  # Usamos la matriz original
            self.tabla3 = CTkTable(self.frame_entradas, values=datos_tabla3)
            self.tabla3.pack(padx=10, pady=10)

        if self.tabla_matriz4 is not None:
            self.lbl_matriz4 = ctk.CTkLabel(self.frame_entradas, text=texto4, font=("Arial", 17))
            self.lbl_matriz4.pack(padx=10, pady=10)

            # tablas para la frame 1 que contiene los datos de entrada
            datos_tabla4 = self.tabla_matriz4  # Usamos la matriz original
            self.tabla4 = CTkTable(self.frame_entradas, values=datos_tabla4)
            self.tabla4.pack(padx=10, pady=10)

    def limpiar_tablas(self):
        """Elimina los frames con las tablas y reinicia las soluciones."""

        # Destruir los frames de las tablas si existen
        if self.frame_entradas:
            self.frame_entradas.destroy()
            self.frame_entradas = None

        # Reiniciar las tablas de entrada, salida y matriz reducida
        if self.tabla_matriz1:
            self.tabla1.destroy()
            self.tabla1 = None
        if self.tabla_matriz2:
            self.tabla2.destroy()
            self.tabla2 = None
        if self.tabla_matriz3:
            self.tabla3.destroy()
            self.tabla3 = None
        if self.tabla_matriz4:
            self.tabla4.destroy()
            self.tabla4 = None
        self.destroy()


class Aplicacion(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación Principal con MarcoMatriz")
        self.geometry("600x600")
        self.ejemplo = [[1, 2, 3], [2, 3, 4], [95, 5, 1]]
        self.ejemplo2 = [[3, 2, 1], [2, 5, 8], [7, 8, 9]]
        self.ejemplo3 = [[-1, 5, 6], [2 / 8, 3, 5], [1, 2, 3]]
        self.ejemplo4 = [[2], [5], [8]]

        self.marco_prueba = None  # optional

        # Botón para obtener los datos de la matriz.
        self.boton_obtener_datos_matriz = ctk.CTkButton(
            self, text="Obtener Datos de la Matriz", command=self.obtener_datos_matriz
        )
        self.boton_obtener_datos_matriz.pack(pady=10)

        # Botón para limpiar las entradas.
        self.boton_limpiar = ctk.CTkButton(
            self, text="Limpiar Entradas", command=self.limpiar_tablas
        )
        self.boton_limpiar.pack(pady=10)

    def limpiar_tablas(self):
        self.marco_prueba.limpiar_tablas()

    def obtener_datos_matriz(self):
        """Imprime los datos de la matriz como un array de fracciones."""
        # self.marco_prueba = TablasFrame(self, tabla1=self.ejemplo, tabla2=self.ejemplo2,
        #                                  tabla3=self.ejemplo3, tabla4=self.ejemplo4, texto1="Matriz 1:",
        #                                  texto2="Matriz 2", texto3="Matriz 3", texto4="vector Ejemplo")
        self.marco_prueba = TablasFrame(self, tabla1=self.ejemplo, texto1="Matriz 1:", texto2="Matriz 2",
                                        texto3="Matriz 3", texto4="vector Ejemplo")
        self.marco_prueba.pack(pady=20)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Opcional, modo de apariencia
    ctk.set_default_color_theme("blue")  # Opcional, tema de color
    app = Aplicacion()
    app.mainloop()
