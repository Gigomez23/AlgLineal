"""
Archivo: main_gui.py 2.0.0
Descripción: archivo que contiene la construcción de la aplicación principal.
"""
from customtkinter import *
from Historial.matriz_historial import Historial
from GUI.submenu.matrices_seleccion import CalculadoraMatricesFrame
from GUI.submenu.vectores_seleccion import CalculadoraVectoresFrame
from GUI.submenu.mixtas_seleccion import CalculadoraMixtaFrame
from GUI.submenu.historial_general_ui import HistorialGeneralFrame


class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.historial = Historial()

        # Establecer el ícono de la ventana
        self.iconbitmap("GUI/archivos_adicionales/logo_uam.ico")

        # Frame principal que contendrá el menú y el área de visualización
        self.frame_principal = CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True)

        # Frame para el menú de navegación
        self.frame_menu = CTkFrame(self.frame_principal, width=200)
        self.frame_menu.pack(side="left", fill="y", padx=10, pady=10)

        # Botones del menú
        self.btn_matrices = CTkButton(self.frame_menu, text="Calculadora de Matrices", command=lambda: self.mostrar_contenido('matrices'))
        self.btn_matrices.pack(pady=10)

        self.btn_mixta = CTkButton(self.frame_menu, text="Calculadora Mixta", command=lambda: self.mostrar_contenido('mixta'))
        self.btn_mixta.pack(pady=10)

        self.btn_vectores = CTkButton(self.frame_menu, text="Calculadora de Vectores",
                                      command=lambda: self.mostrar_contenido('vectores'))
        self.btn_vectores.pack(pady=10)

        # todo: desarollar frame de Historial
        self.btn_historial = CTkButton(self.frame_menu, text="Historial", command=lambda: self.mostrar_contenido('historial'))
        self.btn_historial.pack(pady=10)

        # Frame para el contenido principal
        self.frame_contenido = CTkFrame(self.frame_principal)
        self.frame_contenido.pack(fill="both", expand=True, padx=10, pady=10)

        # Inicializa la primera calculadora directamente
        self.mostrar_contenido('matrices')

    def mostrar_contenido(self, opcion):
        """Función para cambiar el contenido principal basado en la opción seleccionada."""
        # Eliminar el contenido anterior
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        # Muestra el frame correspondiente según la opción
        if opcion == 'vectores':
            frame = CalculadoraVectoresFrame(self.frame_contenido, self.historial)
            frame.pack(fill="both", expand=True)
        elif opcion == 'matrices':
            frame = CalculadoraMatricesFrame(self.frame_contenido, self.historial)
            frame.pack(fill="both", expand=True)
        elif opcion == 'mixta':
            frame = CalculadoraMixtaFrame(self.frame_contenido, self.historial)
            frame.pack(fill="both", expand=True)
        elif opcion == 'historial':
            frame = HistorialGeneralFrame(self.frame_contenido, self.historial)  # Asumiendo que el historial ya es un frame
            frame.pack(fill="both", expand=True)

set_default_color_theme("green")

# Configuración de la ventana
if __name__ == "__main__":
    root = App()
    root.geometry("1200x800")
    root.title("Calculadora de Álgebra Lineal")
    root.mainloop()
