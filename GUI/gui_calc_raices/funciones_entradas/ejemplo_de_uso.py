"""
Ejemplo de uso.
"""
import customtkinter as ctk
from GUI.gui_calc_raices.funciones_entradas.frame_grafica import *
from GUI.gui_calc_raices.funciones_entradas.frame_entrada_funcion import *


class AppPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Científica")
        self.geometry("400x600")

        # Crear un textbox para mostrar la expresión ingresada
        self.textbox = ctk.CTkEntry(self, width=300)
        self.textbox.pack(pady=10)

        # Crear el frame de la calculadora científica
        self.calculadora_cientifica_frame = CalculadoraCientificaFrame(self, self.textbox)
        self.calculadora_cientifica_frame.pack(pady=10, fill="both", expand=True)

        # Botón para imprimir la función ingresada
        self.boton_imprimir_funcion = ctk.CTkButton(self, text="Imprimir Función", command=self.imprimir_funcion)
        self.boton_imprimir_funcion.pack(pady=10)

        # Frame de la gráfica
        self.graficar_frame = GraficarFuncionFrame(self, self.textbox)
        self.graficar_frame.pack(pady=10, fill="both", expand=True)

    def imprimir_funcion(self):
        """Obtiene e imprime la función ingresada en el textbox usando obtener_funcion."""
        funcion = self.calculadora_cientifica_frame.obtener_funcion()
        print("Función ingresada:", funcion)


if __name__ == "__main__":
    app = AppPrincipal()
    app.mainloop()
