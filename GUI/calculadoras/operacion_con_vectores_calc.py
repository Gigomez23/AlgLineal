"""
Archivo: coperacion_con_vectores_calc.py 1.0.5
Descripcion: Archivo que contiene el diseño del frame para operaciones con vectores.
"""
import customtkinter as ctk
from fractions import Fraction
from tkinter import messagebox
from models.clase_vector import *


class VectorOperacionesFrame(ctk.CTkFrame):
    """
    Frame para realizar operaciones con vectores escalados (suma y resta).

    Args:
        parent (CTk): El widget padre que contendrá este frame.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label_dim = ctk.CTkLabel(self, text="Dimensión de los vectores:")
        self.label_dim.pack(pady=10)
        self.entry_dim = ctk.CTkEntry(self)
        self.entry_dim.pack(pady=10)

        self.label_num = ctk.CTkLabel(self, text="Número de vectores:")
        self.label_num.pack(pady=10)
        self.entry_num = ctk.CTkEntry(self)
        self.entry_num.pack(pady=10)

        self.button_create = ctk.CTkButton(self, text="Generar Entradas", command=self.generar_entradas)
        self.button_create.pack(pady=20)

        self.result_text = ctk.CTkTextbox(self, height=200, width=500)
        self.result_text.pack(pady=10)
        self.result_text.configure(state="disabled")  # Deshabilitar edición inicial del textbox

    def generar_entradas(self):
        """
        Genera las entradas necesarias para los vectores y escalares según el número de vectores y dimensión.
        """
        try:
            self.dimension = int(self.entry_dim.get())
            self.num_vectores = int(self.entry_num.get())
            if self.dimension <= 0 or self.num_vectores < 2:
                raise ValueError("Dimensión o número de vectores inválidos.")
        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")
            return

        for widget in self.winfo_children():
            widget.destroy()

        self.label_op = ctk.CTkLabel(self, text="Selecciona la operación:")
        self.label_op.pack(pady=10)

        self.op_var = ctk.StringVar()
        self.op_add = ctk.CTkRadioButton(self, text="Suma", variable=self.op_var, value='suma')
        self.op_add.pack(pady=5)
        self.op_sub = ctk.CTkRadioButton(self, text="Resta", variable=self.op_var, value='resta')
        self.op_sub.pack(pady=5)
        self.op_both = ctk.CTkRadioButton(self, text="Ambas", variable=self.op_var, value='ambas')
        self.op_both.pack(pady=5)

        self.entries = []
        self.scalars = []

        for i in range(self.num_vectores):
            ctk.CTkLabel(self, text=f"Vector {i + 1} (separados por comas):").pack(pady=5)
            entry = ctk.CTkEntry(self)
            entry.pack(pady=5)
            self.entries.append(entry)

            ctk.CTkLabel(self, text=f"Escalar para el Vector {i + 1}:").pack(pady=5)
            scalar = ctk.CTkEntry(self)
            scalar.pack(pady=5)
            self.scalars.append(scalar)

        self.button_calculate = ctk.CTkButton(self, text="Calcular", command=self.calcular_resultados)
        self.button_calculate.pack(pady=20)

        self.result_text = ctk.CTkTextbox(self, height=200, width=500)
        self.result_text.pack(pady=10)
        self.result_text.configure(state="disabled")  # Deshabilitar edición del resultado

    def calcular_resultados(self):
        """
        Calcula las operaciones seleccionadas (suma, resta o ambas) con los vectores ingresados.
        """
        try:
            vectores = [Vector(*entry.get().split(',')) for entry in self.entries]
            escalares = [Fraction(scalar.get()) for scalar in self.scalars]

            vectores_escalados = [v.multiplicar_por_escalar(e) for v, e in zip(vectores, escalares)]

            operacion = self.op_var.get()

            if operacion not in {'suma', 'resta', 'ambas'}:
                raise ValueError("Operación no válida.")

            resultados = []

            if operacion == 'suma' or operacion == 'ambas':
                resultado_suma = vectores_escalados[0]
                for v in vectores_escalados[1:]:
                    resultado_suma = resultado_suma + v
                resultados.append(
                    "\nResultado de la suma:\n" + mostrar_vectores_lado_a_lado(vectores_escalados, resultado_suma,
                                                                               'suma'))

            if operacion == 'resta' or operacion == 'ambas':
                resultado_resta = vectores_escalados[0]
                for v in vectores_escalados[1:]:
                    resultado_resta = resultado_resta - v
                resultados.append(
                    "\nResultado de la resta:\n" + mostrar_vectores_lado_a_lado(vectores_escalados, resultado_resta,
                                                                                'resta'))

            self.result_text.configure(state="normal")
            self.result_text.delete(1.0, ctk.END)
            self.result_text.insert(ctk.END, "\n".join(resultados))
            self.result_text.configure(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {e}")


# Uso en una aplicación más grande
if __name__ == "__main__":
    class AplicacionPrincipal(ctk.CTk):
        """
        Aplicación principal que contiene el frame de operaciones con vectores.
        """

        def __init__(self):
            super().__init__()

            self.title("Operaciones con Vectores Escalados")
            self.geometry("600x600")

            # Frame de operaciones con vectores
            self.vector_operaciones_frame = VectorOperacionesFrame(self)
            self.vector_operaciones_frame.pack(padx=20, pady=20, fill="both", expand=True)


    app = AplicacionPrincipal()
    app.mainloop()
