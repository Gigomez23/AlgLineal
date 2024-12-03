"""
Archivo: graficadora_frame.py 1.0.0
Descripción: Este archivo contiene la interfáz gráficadora.
"""
import customtkinter as ctk
from CTkToolTip import *
from GUI.gui_calc_raices.funciones_entradas.frame_entrada_funcion import CalculadoraCientificaFrame
from GUI.gui_calc_raices.funciones_entradas.frame_grafica import *


class FrameGraficadora(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.frame_de_entradas = ctk.CTkFrame(self)
        self.frame_de_entradas.pack(padx=10, pady=10, expand=True, fill="x")

        self.frame_superior = ctk.CTkFrame(self)
        self.frame_superior.pack(padx=10, pady=10, expand=True, fill="x")

        self.frame_de_botones = ctk.CTkFrame(self)
        self.frame_de_botones.pack(padx=10, pady=10, expand=True, fill="x")

        ctk.CTkLabel(self.frame_de_entradas, text="Funcion f(x):", font=("Arial", 17)).grid(row=0, column=0, padx=10,
                                                                                            pady=10, sticky='n')
        self.entrada_de_funcion = ctk.CTkEntry(self.frame_de_entradas, width=300, height=50, font=("Arial", 17))
        self.entrada_de_funcion.grid(row=0, column=1, padx=10, pady=10, sticky='n')
        self.tooltip_entry_funcion = CTkToolTip(self.entrada_de_funcion,
                                                message="Presione shift para salir del modo exponencial. ",
                                                follow=False)

        self.frame_de_grafica = GraficarFuncionFrame(self.frame_superior, self.entrada_de_funcion)
        self.frame_de_grafica.grid(row=0, column=1, columnspan=2, sticky='nsew', padx=10, pady=10)

        # Crear el frame de la calculadora científica
        self.calculadora_cientifica_frame = CalculadoraCientificaFrame(self.frame_de_botones, self.entrada_de_funcion)
        self.calculadora_cientifica_frame.pack(pady=10, fill="both", expand=True)

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("App Principal")

        # Inicia el Frame de métodos de raíces
        metodos_frame = FrameGraficadora(self)
        metodos_frame.pack(expand=True, fill='both')


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
