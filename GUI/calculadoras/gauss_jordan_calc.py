"""
Archivo: jauss_jorda_calc.py 1.0.5
Descripcion: archivo contiene el diseño del frame para la calculadora de matrices
por metodo escalonado o de Gauss Jordan.
"""
import customtkinter as ctk
from models.clase_sistema_ecuaciones import *


class GaussJordanFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.gauss_jordan = CreadorDeEcuaciones()

        self.entrada_frame = ctk.CTkFrame(self)
        self.entrada_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.resultado_frame = ctk.CTkFrame(self)
        self.resultado_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.label_nombre = ctk.CTkLabel(self.entrada_frame, text="Nombre de la matriz:")
        self.label_nombre.grid(row=0, column=0, padx=10, pady=10)

        self.entry_nombre = ctk.CTkEntry(self.entrada_frame)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        self.label_matriz = ctk.CTkLabel(self.entrada_frame, text="Matriz (separada por espacios, cada fila en una línea):")
        self.label_matriz.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.text_matriz = ctk.CTkTextbox(self.entrada_frame, width=400, height=100)
        self.text_matriz.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        # Botones
        self.btn_reducir = ctk.CTkButton(self.entrada_frame, text="Reducir", command=self.reducir_matriz)
        self.btn_reducir.grid(row=3, column=0, padx=10, pady=10)

        self.btn_mostrar_solucion = ctk.CTkButton(self.entrada_frame, text="Mostrar Solución", command=self.mostrar_solucion)
        self.btn_mostrar_solucion.grid(row=3, column=1, padx=10, pady=10)

        # Botón para limpiar entradas
        self.btn_limpiar = ctk.CTkButton(self.entrada_frame, text="Limpiar", command=self.limpiar_entradas)
        self.btn_limpiar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.label_salida = ctk.CTkLabel(self.resultado_frame, text="Salida:")
        self.label_salida.grid(row=0, column=0, padx=10, pady=10)

        self.text_salida_frame = ctk.CTkFrame(self.resultado_frame)
        self.text_salida_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.text_salida = ctk.CTkTextbox(self.text_salida_frame, width=400, height=150, wrap="none")
        self.text_salida.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.text_salida_frame, command=self.text_salida.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.text_salida.configure(yscrollcommand=self.scrollbar.set)

    def reducir_matriz(self):
        nombre = self.entry_nombre.get()
        matriz_text = self.text_matriz.get("1.0", "end-1c")
        matriz_filas = matriz_text.split("\n")

        matriz = []
        for fila in matriz_filas:
            if fila.strip():
                matriz.append([Fraction(x) for x in fila.split()])

        self.gauss_jordan.nombre = nombre
        self.gauss_jordan.matriz = matriz
        self.gauss_jordan.filas = len(matriz)
        self.gauss_jordan.columnas = len(matriz[0]) - 1

        self.text_salida.delete("1.0", "end")

        self.gauss_jordan.pasos = 0
        self.gauss_jordan.reducir(self.mostrar_paso)

    def mostrar_paso(self, texto):
        self.text_salida.insert("end", texto + "\n")

    def mostrar_solucion(self):
        self.gauss_jordan.mostrar_solucion(self.mostrar_paso)

    def limpiar_entradas(self):
        """Limpia los campos de entrada y la salida."""
        self.entry_nombre.delete(0, "end")
        self.text_matriz.delete("1.0", "end")
        self.text_salida.delete("1.0", "end")

# Uso del frame
if __name__ == "__main__":
    root = ctk.CTk()
    app_frame = GaussJordanFrame(root)
    app_frame.pack(padx=10, pady=10, fill="both", expand=True)
    root.mainloop()

