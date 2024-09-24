"""
Archivo: main_gui.py 1.3.5
Descripción: archivo que contiene la construcción de la aplicación principal.
"""

from customtkinter import *  # Importa CustomTkinter para los componentes de la UI
from PIL import Image  # Importa PIL para posibles manipulaciones de imágenes
from GUI.calculadoras.gauss_jordan_calc import GaussJordanFrame
from GUI.calculadoras.ecuacion_matricial_matrizxvector_calc import MultiplicacionMatricesFrame
from GUI.calculadoras.multi_fila_x_columna_calc import VectorMultiplicacionFrame
from GUI.calculadoras.operacion_con_vectores_calc import VectorOperacionesFrame
from GUI.calculadoras.Au_Ax_calc import CalculadoraDeMatrizxVectoresFrame

# Clase principal de la aplicación
class App(CTk):
    def __init__(self, *args, **kwargs):
        """Inicializa la aplicación principal."""
        super().__init__(*args, **kwargs)

        # Establecer el ícono de la ventana
        self.iconbitmap("GUI/archivos_adicionales/logo_uam.ico")

        # # Frame superior (barra superior)
        # self.frame_top_bar = CTkFrame(master=self, width=0, height=50)
        # self.frame_top_bar.pack_propagate(False)
        # self.frame_top_bar.pack(fill="x")
        #
        # # Menú desplegable en la barra superior
        # self.om_menu_de_opciones = CTkOptionMenu(
        #     master=self.frame_top_bar,
        #     anchor="e",
        #     values=['Calculadora', 'Historial', 'Salir'],
        #     font=CTkFont(family="Consolas", slant="roman", size=14)
        # )
        # self.om_menu_de_opciones.pack(padx=(5, 0), side="left")

        # Frame de encabezado para el texto y menú de selección
        self.frame_encabezado = CTkFrame(master=self)
        self.frame_encabezado.pack(fill="x", padx=10, pady=10)

        # Label para seleccionar el tipo de cálculo
        self.label_seleccion = CTkLabel(
            master=self.frame_encabezado,
            text="Seleccione el tipo de calculadora:",
            font=CTkFont(family="Consolas", size=14)
        )
        self.label_seleccion.pack(side="left", padx=(0, 10), anchor="w")

        # Menú de selección del tipo de calculadora
        self.btn_menu_tipo_calculadora = CTkOptionMenu(
            master=self.frame_encabezado,
            values=['Resolver Ecuaciones Lineales', 'Multiplicar Matriz x Vector', 'Multiplicar Matriz x Vectores',
                    'Multiplicar Vector Fila x Columna', 'Operaciones de Vectores'],
            anchor="w",
            width=250,
            hover=True,
            command=self.cambiar_frame  # Cambia al método que selecciona el frame
        )
        self.btn_menu_tipo_calculadora.pack(side="right", padx=(0, 10))

        # Frame principal de la calculadora
        self.frame_calculadora = CTkFrame(master=self)
        self.frame_calculadora.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame interno que será cambiable dentro del frame principal
        self.frame_cambiable = CTkFrame(master=self.frame_calculadora)
        self.frame_cambiable.pack(fill="both", expand=True)

        # Inicializa los frames diferentes para las opciones
        self.frames = {
            'Resolver Ecuaciones Lineales': GaussJordanFrame(self.frame_cambiable),
            'Multiplicar Matriz x Vector': MultiplicacionMatricesFrame(self.frame_cambiable),
            'Multiplicar Matriz x Vectores': CalculadoraDeMatrizxVectoresFrame(self.frame_cambiable),
            'Multiplicar Vector Fila x Columna': VectorMultiplicacionFrame(self.frame_cambiable),
            'Operaciones de Vectores': VectorOperacionesFrame(self.frame_cambiable, self)
            # Agrega el argumento main_app
        }

        # Muestra el frame por defecto
        self.cambiar_frame('Resolver Ecuaciones Lineales')

    def cambiar_frame(self, opcion_seleccionada):
        """Cambia el frame según la opción seleccionada en el menú."""
        # Elimina el contenido anterior del frame cambiable
        for widget in self.frame_cambiable.winfo_children():
            widget.pack_forget()

        # Añade el nuevo frame según la opción seleccionada
        nuevo_frame = self.frames.get(opcion_seleccionada)
        if nuevo_frame:
            nuevo_frame.pack(expand=True, fill="both")

    def cambiar_frame_vector(self, frame_class, *args):
        """Cambia el frame actual a una nueva instancia del frame_class proporcionado."""
        # Elimina el contenido anterior del frame cambiable
        for widget in self.frame_cambiable.winfo_children():
            widget.pack_forget()

        # Crea una nueva instancia del frame_class proporcionado
        nuevo_frame = frame_class(self.frame_cambiable, self, *args)
        nuevo_frame.pack(padx=20, pady=20, fill="both", expand=True)


# Configuraciones de la ventana principal
set_default_color_theme("green")

if __name__ == "__main__":
    # Inicializa la aplicación
    root = App()
    root.geometry("1000x800")
    root.title("Calculadora Algebra Lineal")
    root.configure(fg_color=['gray92', 'gray14'])
    root.mainloop()
