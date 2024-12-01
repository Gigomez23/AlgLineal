"""
Programa Versión:  4.4.0
Descripcion: archivo main
Clase: Algebra Lineal
Integrantes: Gabriel Gómez, Gessler Herrera, Gabriel Lacayo, Oliver Espinoza
"""
from customtkinter import set_default_color_theme  # Asegúrate de importar la función para aplicar el tema
from main_gui import PantallaInicio  # Importa la clase PantallaInicio desde main_gui.py
from PIL import Image
from CTkMenuBar import *


def ejecutar_acerca_de():
    print('Se ejecuta acerca de')


# Aplica el tema desde aquí antes de crear la instancia de la clase
set_default_color_theme("green")  # O el tema que prefieras, por ejemplo, "green", "dark", etc.

# Configuración y ejecución de la pantalla de inicio
if __name__ == "__main__":
    app = PantallaInicio()  # Crea una instancia de la clase PantallaInicio

    # crea el menu de titulo
    menu = CTkTitleMenu(master=app)
    opcion_configuracion = menu.add_cascade("Configuración")
    opcion_historial = menu.add_cascade("Historial")
    opcion_acerca_de = menu.add_cascade("Acerca De", command=ejecutar_acerca_de)

    # submenus de menu de titulo
    configuracion_opcion = CustomDropdownMenu(widget=opcion_configuracion)
    configuracion_opcion.add_option(option="Apariencia", command=lambda: print("Cambio de apariencia"))
    configuracion_opcion.add_option(option="Activar teclado de pantalla", command=lambda:
    print("Actiavar on-screen keyboard"))

    historial_opcion = CustomDropdownMenu(widget=opcion_historial)
    historial_opcion.add_option(option="Subir Historial", command=lambda: print("Sube historial de archivo local"))
    historial_opcion.add_option(option="Guardar Historial", command=lambda: print("Guardar historial"))

    # acerca_de_opcion = CustomDropdownMenu(widget=opcion_acerca_de)
    # acerca_de_opcion.add_option(option="Acerca De", command=ejecutar_acerca_de)

    # Configura el ícono de la ventana usando el logo de Calinu
    app.iconbitmap("GUI/archivos_adicionales/calinu_logo.ico")  # Cambia la ruta si es necesario

    app.mainloop()  # Ejecuta la aplicación


