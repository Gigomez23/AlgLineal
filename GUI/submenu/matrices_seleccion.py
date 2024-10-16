from customtkinter import *  # Importa CustomTkinter para los componentes de la UI
from GUI.calculadoras.gauss_jordan_calc import GaussJordanFrame
from GUI.calculadoras.operaciones_calc import OperacionesAritmeticasMatrizFrame
from GUI.calculadoras.transpuesta_inversa_calc import MatrizCalculatorInvTranFrame
from GUI.calculadoras.determinante_frame import DeterminanteFrame


# Clase principal convertida a Frame
class CalculadoraMatricesFrame(CTkFrame):
    def __init__(self, parent, historial, *args, **kwargs):
        """Inicializa la calculadora en un frame."""
        super().__init__(parent, *args, **kwargs)

        # Se inicializa el historial
        self.historial = historial

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
            values=['Resolver Ecuaciones Lineales', 'Operaciones de Matrices', "Inversa/Transpuesta Matriz", "Determinante"],
            anchor="w",
            width=250,
            hover=True,
            command=self.cambiar_frame  # Cambia al método que selecciona el frame
        )
        self.btn_menu_tipo_calculadora.pack(side="right", padx=(0, 10))

        # Frame principal de la calculadora (scrollable)
        self.frame_calculadora = CTkScrollableFrame(master=self)  # Cambiado a CTkScrollableFrame
        self.frame_calculadora.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame interno que será cambiable dentro del frame principal
        self.frame_cambiable = CTkFrame(master=self.frame_calculadora)
        self.frame_cambiable.pack(fill="both", expand=True)

        # Inicializa los frames diferentes para las opciones
        self.frames = {
            'Resolver Ecuaciones Lineales': GaussJordanFrame(self.frame_cambiable, self.historial),
            'Operaciones de Matrices': OperacionesAritmeticasMatrizFrame(self.frame_cambiable, self.historial),
            'Inversa/Transpuesta Matriz': MatrizCalculatorInvTranFrame(self.frame_cambiable, self.historial),
            'Determinante': DeterminanteFrame(self.frame_cambiable, self.historial)
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