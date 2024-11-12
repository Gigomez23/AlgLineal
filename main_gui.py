"""
Archivo: main_gui.py 3.0.0
Descripción: archivo que contiene la construcción de la aplicación principal.
"""
from customtkinter import *
from GUI.frame_principal_vect_matr_calc import CalculadoraMatricesApp
from GUI.frame_principal_funcion_calc import CalculadoraFuncionApp
from PIL import Image


class PantallaInicio(CTk):
    """Pantalla de inicio para seleccionar entre diferentes calculadoras."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1200x800")
        self.title("Pantalla de Inicio - Calculadoras")
        self.configure(bg="#2b2b2b")

        # Frame principal para contener los elementos
        self.frame_seleccion = CTkFrame(self, corner_radius=15, bg_color="#1e1e1e")
        self.frame_seleccion.pack(padx=50, pady=50, fill="both", expand=True)

        # Logo en la esquina superior izquierda
        self.logo_image = CTkImage(Image.open("GUI/archivos_adicionales/logo_uam.ico"), size=(50, 50))
        self.logo_label = CTkLabel(self.frame_seleccion, image=self.logo_image, text="")
        self.logo_label.place(x=10, y=10)  # Posición en la esquina superior izquierda

        # Título principal
        self.label_titulo = CTkLabel(
            self.frame_seleccion,
            text="Bienvenido Usuario <3",
            font=("Arial", 28, "bold"),
            text_color="#ffffff"
        )
        self.label_titulo.pack(pady=(80, 20))  # Espaciado para dejar lugar para la imagen central

        # Imagen en el centro
        self.central_image = CTkImage(Image.open("GUI/archivos_adicionales/calinu_logo.png"), size=(400, 400))
        self.image_label = CTkLabel(self.frame_seleccion, image=self.central_image, text="")
        self.image_label.pack(pady=(10, 30))  # Ubicación debajo del título

        # Botón para abrir la Calculadora de Matrices y Vectores
        self.btn_calculadora_matrices = CTkButton(
            self.frame_seleccion,
            text="Calculadora de Matrices/Vectores",
            command=self.mostrar_calculadora_matrices,
            font=("Arial", 16),
            fg_color="#007ACC",
            hover_color="#005A8D",
            corner_radius=8
        )
        self.btn_calculadora_matrices.pack(pady=20, padx=20, fill="x")

        # Botón para abrir la Calculadora en desarrollo
        self.btn_calculadora_otra = CTkButton(
            self.frame_seleccion,
            text="Calculadora de Funciones",
            command=self.mostrar_calculadora_otra,
            font=("Arial", 16),
            fg_color="#007ACC",
            hover_color="#005A8D",
            corner_radius=8
        )
        self.btn_calculadora_otra.pack(pady=20, padx=20, fill="x")

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
#
