"""
Programa Versión:  4.0.0 beta
Descripcion: archivo main
Clase: Algebra Lineal
Integrantes: Gabriel Gómez, Gessler Herrera, Gabriel Lacayo, Oliver Espinoza
"""
from customtkinter import set_default_color_theme  # Asegúrate de importar la función para aplicar el tema
from main_gui import PantallaInicio  # Importa la clase PantallaInicio desde main_gui.py
from PIL import Image

# Aplica el tema desde aquí antes de crear la instancia de la clase
set_default_color_theme("green")  # O el tema que prefieras, por ejemplo, "green", "dark", etc.

# Configuración y ejecución de la pantalla de inicio
if __name__ == "__main__":
    app = PantallaInicio()  # Crea una instancia de la clase PantallaInicio

    # Configura el ícono de la ventana usando el logo de Calinu
    app.iconbitmap("GUI/archivos_adicionales/calinu_logo.ico")  # Cambia la ruta si es necesario

    app.mainloop()  # Ejecuta la aplicación


