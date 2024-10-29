"""
Archivo: multi_fila_x_columna_calc.py 2.1.0
Descripcion: Archivo que contiene el diseño del frame para operaciones de vector x vector.
"""
import customtkinter as ctk
from fractions import Fraction
from CTkMessagebox import CTkMessagebox
from models.clase_muli_vectores import VectorMultiplicacionCalculadora
from GUI.interfaz_entrada.entrada_vector_frame import *
from funciones_adicionales.convertir_formato_lista import *


class VectorMultiplicacionFrame(ctk.CTkFrame):
    """
    Frame para la multiplicación de un vector fila por un vector columna utilizando customtkinter.

    Args:
        parent (CTkWidget): El widget padre que contendrá este frame.
    """

    def __init__(self, parent, historial):
        super().__init__(parent)
        self.historial = historial
        self.calculadora = VectorMultiplicacionCalculadora()

        # Frame para entrada
        self.entrada_frame = ctk.CTkFrame(self)
        self.entrada_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame para resultados
        self.resultado_frame = ctk.CTkFrame(self)
        self.resultado_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")


        # Configuración del frame
        self.label_fila = ctk.CTkLabel(self.entrada_frame, text="Introduce el vector fila:")
        self.label_fila.grid(row=0, column=0, padx=10, pady=10)

        self.entry_fila = FrameEntradaVector(self.entrada_frame)
        self.entry_fila.grid(row=1, column=0, padx=10, pady=10)

        self.label_columna = ctk.CTkLabel(self.entrada_frame, text="Introduce el vector columna:")
        self.label_columna.grid(row=0, column=1, padx=10, pady=10)

        self.entry_columna = FrameEntradaVector(self.entrada_frame)
        self.entry_columna.grid(row=1, column=1, padx=10, pady=10)

        self.button_calculate = ctk.CTkButton(self.entrada_frame, text="Calcular Multiplicación",
                                              command=self.calcular_multiplicacion)
        self.button_calculate.grid(row=2, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

        self.result_text = ctk.CTkTextbox(self.resultado_frame, height=200, width=300)
        self.result_text.pack(pady=10, padx=10)
        self.result_text.configure(state="disabled")  # Hacer que el textbox sea de solo lectura

        self.button_clear = ctk.CTkButton(self.resultado_frame, text="Limpiar", command=self.limpiar_entradas)
        self.button_clear.pack(pady=10)

    def calcular_multiplicacion(self):
        """
        Función que obtiene los vectores de entrada, realiza el cálculo y muestra el resultado.
        """
        try:
            # Obtener valores de entrada
            fila_str = self.entry_fila.obtener_matriz_como_array()
            columna_str = self.entry_columna.obtener_matriz_como_array()

            # Parsear vectores como fracciones
            fila = a_lista_simple(fila_str)
            columna = a_lista_simple(columna_str)

            # Configurar vectores en la calculadora
            self.calculadora.set_vectores(fila, columna)
            proceso_y_resultado = self.calculadora.calcular()

            # Mostrar el proceso y el resultado
            self.result_text.configure(state="normal")
            self.result_text.delete(1.0, ctk.END)
            self.result_text.insert(ctk.END, f"Proceso de la multiplicación:\n{proceso_y_resultado}")
            self.result_text.configure(state="disabled")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error en el cálculo: {e}",
                          icon="cancel", option_1="Entendido", button_hover_color="green", fade_in_duration=2)

    def limpiar_entradas(self):
        """Limpia los campos de entrada y el texto de salida."""
        self.entry_fila.limpiar_entradas()
        self.entry_columna.limpiar_entradas()
        self.result_text.configure(state="normal")
        self.result_text.delete(1.0, ctk.END)
        self.result_text.configure(state="disabled")


# Uso en una aplicación más grande
if __name__ == "__main__":
    class AplicacionPrincipal(ctk.CTk):
        """
        Aplicación principal que contiene el frame de multiplicación de vectores.
        """
        def __init__(self):
            super().__init__()

            historial = []
            self.title("Multiplicación de Vectores Fila y Columna")
            self.geometry("600x600")

            # Frame de Multiplicación de Vectores
            self.vector_multiplicacion_frame = VectorMultiplicacionFrame(self, historial)
            self.vector_multiplicacion_frame.pack(padx=20, pady=20, fill="both", expand=True)


    app = AplicacionPrincipal()
    app.mainloop()

