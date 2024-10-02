"""
Archivo: jauss_jorda_calc.py 1.1.2
Descripción: Este archivo contiene el diseño del frame para la calculadora de matrices
por método escalonado o de Gauss-Jordan.
"""
import customtkinter as ctk
from models.clase_sistema_ecuaciones import *
from CTkMessagebox import CTkMessagebox
from fractions import Fraction
#todo: fix this
class GaussJordanFrame(ctk.CTkFrame):
    """
    Frame para realizar la reducción de matrices usando el método de Gauss-Jordan.

    Args:
        parent (CTk): El widget padre que contendrá este frame.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.gauss_jordan = CreadorDeEcuaciones()

        # Frame para entradas
        self.entrada_frame = ctk.CTkFrame(self)
        self.entrada_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame para resultados
        self.resultado_frame = ctk.CTkFrame(self)
        self.resultado_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Componentes del frame de entrada
        self.label_matriz = ctk.CTkLabel(self.entrada_frame,
                                         text="Matriz (filas separadas "
                                              "por enter, valores separados por espacios):")
        self.label_matriz.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        # Aumentar la altura del Textbox
        self.text_matriz = ctk.CTkTextbox(self.entrada_frame, width=400, height=150)
        self.text_matriz.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        # Botones para operaciones
        self.btn_reducir = ctk.CTkButton(self.entrada_frame, text="Reducir", command=self.reducir_matriz)
        self.btn_reducir.grid(row=3, column=0, padx=10, pady=10)

        self.btn_mostrar_solucion = ctk.CTkButton(self.entrada_frame, text="Mostrar Solución",
                                                  command=self.mostrar_solucion)
        self.btn_mostrar_solucion.grid(row=3, column=1, padx=10, pady=10)

        # Frame para resultados
        self.label_salida = ctk.CTkLabel(self.resultado_frame, text="Solución:")
        self.label_salida.grid(row=0, column=0, padx=10, pady=10)

        self.text_salida_frame = ctk.CTkFrame(self.resultado_frame)
        self.text_salida_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.text_salida = ctk.CTkTextbox(self.text_salida_frame, width=400, height=150, wrap="none")
        self.text_salida.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.text_salida_frame, command=self.text_salida.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.text_salida.configure(yscrollcommand=self.scrollbar.set)

        # Botón para limpiar entradas, ahora en el frame de resultados
        self.btn_limpiar = ctk.CTkButton(self.resultado_frame, text="Limpiar", command=self.limpiar_entradas)
        self.btn_limpiar.grid(row=2, column=0, padx=10, pady=10)

    def reducir_matriz(self):
        """Realiza la reducción de la matriz introducida por el usuario."""
        matriz_text = self.text_matriz.get("1.0", "end-1c")

        if not matriz_text.strip():
            CTkMessagebox(title="Error", message="Las entradas de la matriz están vacías.", icon="warning",
                          option_1="Entendido", button_hover_color="green")
            return

        matriz_filas = matriz_text.split("\n")
        matriz = []
        try:
            for fila in matriz_filas:
                if fila.strip():
                    matriz.append([Fraction(x) for x in fila.split()])

            if not matriz:
                raise ValueError("Matriz vacía")

        except ValueError:
            CTkMessagebox(title="Error", message="Las entradas de la matriz contienen caracteres inválidos.",
                          icon="warning", option_1="Entendido", button_hover_color="green")
            return

        self.gauss_jordan.matriz = matriz
        self.gauss_jordan.filas = len(matriz)
        self.gauss_jordan.columnas = len(matriz[0]) - 1

        self.text_salida.delete("1.0", "end")
        self.gauss_jordan.pasos = 0
        self.gauss_jordan.reducir(self.mostrar_paso)

    def mostrar_paso(self, texto):
        """Muestra un paso del proceso de reducción en el textbox de salida."""
        self.text_salida.insert("end", texto + "\n")

    def mostrar_solucion(self):
        """Muestra la solución de la matriz reducida."""
        matriz_text = self.text_matriz.get("1.0", "end-1c")

        if not matriz_text.strip():
            CTkMessagebox(title="Error", message="Las entradas de la matriz están vacías.", icon="warning",
                          option_1="Entendido", button_hover_color="green")
            return

        try:
            matriz_filas = matriz_text.split("\n")
            matriz = []
            for fila in matriz_filas:
                if fila.strip():
                    matriz.append([Fraction(x) for x in fila.split()])
            if not matriz:
                raise ValueError("Matriz vacía")

        except ValueError:
            CTkMessagebox(title="Error", message="Las entradas de la matriz contienen caracteres inválidos.",
                          icon="warning", option_1="Entendido", button_hover_color="green")
            return

        self.gauss_jordan.matriz = matriz
        self.gauss_jordan.filas = len(matriz)
        self.gauss_jordan.columnas = len(matriz[0]) - 1

        self.text_salida.delete("1.0", "end")
        self.gauss_jordan.mostrar_solucion(self.mostrar_paso)

    def limpiar_entradas(self):
        """Limpia los campos de entrada y la salida."""
        self.text_matriz.delete("1.0", "end")
        self.text_salida.delete("1.0", "end")


# Uso del frame
if __name__ == "__main__":
    root = ctk.CTk()
    app_frame = GaussJordanFrame(root)
    app_frame.pack(padx=10, pady=10, fill="both", expand=True)
    root.mainloop()
