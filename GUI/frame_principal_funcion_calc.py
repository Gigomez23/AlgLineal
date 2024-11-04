"""
Archivo: frame_principal_fucnion_calc.py 1.0.0
Descripción: archivo que contiene la construcción de la calculadora de matrices y vectores.
"""
from customtkinter import *
from Historial.historial_matriz.matriz_historial import Historial
from GUI.gui_calc_matriz.submenu.matrices_seleccion import CalculadoraMatricesFrame
from GUI.gui_calc_matriz.submenu.vectores_seleccion import CalculadoraVectoresFrame
from GUI.gui_calc_matriz.submenu.mixtas_seleccion import CalculadoraMixtaFrame
from GUI.gui_calc_matriz.submenu.historial_general_ui import HistorialGeneralFrame


class CalculadoraMatricesApp(CTkFrame):
    """App de calculadora de matrices y vectores, convertida en Frame para integración."""

    def __init__(self, parent, regresar_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.historial = Historial()
        self.regresar_callback = regresar_callback  # Callback para regresar a la pantalla de inicio

        # Frame principal que contendrá el menú y el área de visualización
        self.frame_principal = CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True)

        # Frame para el contenido principal
        self.frame_contenido = CTkFrame(self.frame_principal)
        self.frame_contenido.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Frame para el menú de navegación (inicialmente oculto)
        self.frame_menu = CTkFrame(self.frame_principal, width=200)
        self.label_menu = CTkLabel(self.frame_menu, text="Seleccione el tipo \nde operación:",
                                   font=CTkFont(family="Consolas", size=14))
        self.label_menu.pack(padx=5, pady=10)

        self.btn_matrices = CTkButton(self.frame_menu, text="Funciones Mixtas",
                                      command=lambda: self.mostrar_contenido('General'))
        self.btn_matrices.pack(pady=10, padx=5)

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
        self.mostrar_contenido('matrices')

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

        if opcion == 'General':
            frame = CalculadoraVectoresFrame(self.frame_contenido, self.historial) #todo: add the calc frame here
            frame.pack(fill="both", expand=True)
        # elif opcion == 'matrices':
        #     frame = CalculadoraMatricesFrame(self.frame_contenido, self.historial)
        #     frame.pack(fill="both", expand=True)
        # elif opcion == 'mixta':
        #     frame = CalculadoraMixtaFrame(self.frame_contenido, self.historial)
        #     frame.pack(fill="both", expand=True)
        # elif opcion == 'historial':
        #     frame = HistorialGeneralFrame(self.frame_contenido, self.historial)
        #     frame.pack(fill="both", expand=True)

    def regresar_a_inicio(self):
        """Llama al callback para regresar a la pantalla de inicio."""
        self.regresar_callback()



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
        self.calculadora_otra_frame = CTkFrame(self)
        label = CTkLabel(self.calculadora_otra_frame, text="Calculadora en desarrollo")
        label.pack(pady=10)

    def mostrar_calculadora_matrices(self):
        """Muestra la calculadora de matrices y oculta la pantalla de selección."""
        self.frame_seleccion.pack_forget()
        self.calculadora_otra_frame.pack_forget()
        self.calculadora_matrices_frame.pack(fill="both", expand=True)

    def mostrar_calculadora_otra(self):
        """Muestra la calculadora en desarrollo y oculta la pantalla de selección."""
        self.frame_seleccion.pack_forget()
        self.calculadora_matrices_frame.pack_forget()
        self.calculadora_otra_frame.pack(fill="both", expand=True)

    def mostrar_inicio(self):
        """Muestra la pantalla de inicio."""
        self.calculadora_matrices_frame.pack_forget()
        self.calculadora_otra_frame.pack_forget()
        self.frame_seleccion.pack(fill="both", expand=True)


# Configuración y ejecución de la pantalla de inicio
if __name__ == "__main__":
    app = PantallaInicio()
    set_default_color_theme("green")
    app.mainloop()
