"""
Archivo: main_gui.py 2.0.0
Descripción: archivo que contiene la construcción de la aplicación principal.
"""
from customtkinter import *
from GUI.frame_principal_vect_matr_calc import CalculadoraMatricesApp
from GUI.frame_principal_funcion_calc import CalculadoraFuncionApp


class PantallaInicio(CTk):
    """Pantalla de inicio para seleccionar entre diferentes calculadoras."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1200x800")
        self.title("Pantalla de Inicio - Calculadoras")

        # Frame principal para contener los botones de selección
        self.frame_seleccion = CTkFrame(self)
        self.frame_seleccion.pack(fill="both", expand=True)

        # Botón para abrir la Calculadora de Matrices y Vectores
        self.btn_calculadora_matrices = CTkButton(
            self.frame_seleccion, text="Calculadora de Matrices/Vectores",
            command=self.mostrar_calculadora_matrices
        )
        self.btn_calculadora_matrices.pack(pady=20)

        # Botón para abrir la Calculadora en desarrollo
        self.btn_calculadora_otra = CTkButton(
            self.frame_seleccion, text="Otra Calculadora (en desarrollo)",
            command=self.mostrar_calculadora_otra
        )
        self.btn_calculadora_otra.pack(pady=20)

        # Frame para la Calculadora de Matrices y Vectores
        self.calculadora_matrices_frame = CalculadoraMatricesApp(self, self.mostrar_inicio)

        # Frame de la otra calculadora (en proceso de desarrollo)
        self.calculadora_funcion_frame = CalculadoraFuncionApp(self, self.mostrar_inicio)

    def mostrar_calculadora_matrices(self):
        """Muestra la calculadora de matrices y oculta la pantalla de selección."""
        self.frame_seleccion.pack_forget()
        self.calculadora_funcion_frame.pack_forget()
        self.calculadora_matrices_frame.pack(fill="both", expand=True)

    def mostrar_calculadora_otra(self):
        """Muestra la calculadora en desarrollo y oculta la pantalla de selección."""
        self.frame_seleccion.pack_forget()
        self.calculadora_matrices_frame.pack_forget()
        self.calculadora_funcion_frame.pack(fill="both", expand=True)

    def mostrar_inicio(self):
        """Muestra la pantalla de inicio."""
        self.calculadora_matrices_frame.pack_forget()
        self.calculadora_funcion_frame.pack_forget()
        self.frame_seleccion.pack(fill="both", expand=True)


# Configuración y ejecución de la pantalla de inicio
if __name__ == "__main__":
    app = PantallaInicio()
    set_default_color_theme("green")
    app.mainloop()


