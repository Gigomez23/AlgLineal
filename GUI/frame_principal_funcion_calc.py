"""
Archivo: frame_principal_fucnion_calc.py 1.0.2
Descripción: archivo que contiene la construcción de la calculadora de matrices y vectores.
"""
from customtkinter import *
from Historial.historial_matriz.matriz_historial import Historial
from GUI.gui_calc_raices.submenu.funciones_raices import FuncionesRaicesFrame
from GUI.gui_calc_raices.submenu.frame_raices import *

class CalculadoraFuncionApp(CTkFrame):
    """App de calculadora de matrices y vectores, convertida en Frame para integración."""

    def __init__(self, parent, regresar_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.historial = Historial()
        self.regresar_callback = regresar_callback  # Callback para regresar a la pantalla de inicio

        # Frame principal que contendrá el menú y el área de visualización
        self.frame_principal = CTkFrame(self)
        self.frame_principal.pack(side="left", fill="both", expand=True, padx=10)

        # Frame para el contenido principal
        self.frame_contenido = CTkFrame(self.frame_principal)
        self.frame_contenido.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Frame para el menú de navegación (inicialmente oculto)
        self.frame_menu = CTkFrame(self.frame_principal, width=200)
        self.label_menu = CTkLabel(self.frame_menu, text="Seleccione el tipo \nde operación:",
                                   font=CTkFont(family="Consolas", size=14))
        self.label_menu.pack(padx=5, pady=10)

        self.btn_matrices = CTkButton(self.frame_menu, text="Funciones Raices",
                                      command=lambda: self.mostrar_contenido('Raices'))
        self.btn_matrices.pack(pady=10, padx=5)

        self.btn_otros = CTkButton(self.frame_menu, text="Otros",
                                      command=lambda: self.mostrar_contenido('Otros'))
        self.btn_otros.pack(pady=10, padx=5)

        # Botón para regresar a la pantalla de inicio
        self.btn_regresar_inicio = CTkButton(self.frame_menu, text="Regresar a Inicio",
                                             command=self.regresar_a_inicio)
        self.btn_regresar_inicio.pack(side="bottom", pady=10, padx=5)

        # Botón en la parte superior derecha para mostrar el menú
        self.boton_menu_icono = CTkButton(
            self.frame_principal, text="☰", width=32, height=20,
            command=self.mostrar_menu
        )
        self.boton_menu_icono.place(relx=0.0, rely=0.0, anchor="nw", x=20, y=1)

        # Inicializa la primera calculadora directamente
        self.mostrar_contenido('Raices')

        # Área sensible para mostrar el menú
        self.area_sensible = CTkFrame(self.frame_principal, width=10, bg_color="transparent")
        self.area_sensible.pack(side="left", fill="y")
        self.area_sensible.bind("<Enter>", self.mostrar_menu)

        # Detectar cuando el mouse sale del menú
        self.frame_menu.bind("<Enter>", self.cancelar_ocultacion)
        self.frame_menu.bind("<Leave>", self.iniciar_ocultacion)
        self.ocultar_menu_id = None

    def mostrar_menu(self, event=None):
        """Muestra el menú y desplaza el contenido hacia la derecha."""
        if not self.frame_menu.winfo_ismapped():
            self.frame_menu.pack(side="left", fill="y", padx=10, pady=10)
            self.boton_menu_icono.place_forget()  # Oculta el ícono del botón del menú
        self.cancelar_ocultacion()

    def iniciar_ocultacion(self, event=None):
        """Inicia el temporizador para ocultar el menú."""
        self.ocultar_menu_id = self.after(1500, self.ocultar_menu)

    def cancelar_ocultacion(self, event=None):
        """Cancela el temporizador para ocultar el menú."""
        if self.ocultar_menu_id:
            self.after_cancel(self.ocultar_menu_id)
            self.ocultar_menu_id = None

    def ocultar_menu(self):
        """Oculta el menú y ajusta el contenido."""
        self.frame_menu.pack_forget()
        self.boton_menu_icono.place(relx=0.0, rely=0.0, anchor="nw", x=20, y=1)  # Muestra el ícono del botón del menú de nuevo

    def mostrar_contenido(self, opcion):
        """Función para cambiar el contenido principal basado en la opción seleccionada."""
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        frame = CTkFrame(self.frame_contenido)
        frame.pack(fill="both", expand=True)

        if opcion == 'Raices':
            frame_calculadora = FrameRaices(frame)
            frame_calculadora.pack(fill="both", expand=True)
        elif opcion == 'Otros':
            frame = FuncionesRaicesFrame(frame)
            frame.pack(fill="both", expand=True)
        # elif opcion == 'mixta':
        #     frame = CalculadoraMixtaFrame(self.frame_contenido, self.historial)
        #     frame.pack(fill="both", expand=True)
        # elif opcion == 'historial':
        #     frame = HistorialGeneralFrame(self.frame_contenido, self.historial)
        #     frame.pack(fill="both", expand=True)

    def regresar_a_inicio(self):
        """Llama al callback para regresar a la pantalla de inicio."""
        self.regresar_callback()


# Configuración inicial de la ventana principal
class MainApp(CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Matrices y Vectores")
        self.geometry("800x600")

        # Función de callback para regresar al inicio (no hace nada en este ejemplo)
        def regresar_callback():
            print("Regresando a la pantalla de inicio...")

        # Inicializa la frame de CalculadoraFuncionApp
        self.calculadora_frame = CalculadoraFuncionApp(self, regresar_callback)
        self.calculadora_frame.pack(fill="both", expand=True)


# Ejecución de la aplicación
if __name__ == "__main__":
    set_appearance_mode("dark")
    set_default_color_theme("blue")
    app = MainApp()
    app.mainloop()

