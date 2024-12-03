"""
Archivo: historial_popup_ui.py 2.2.1
Descripción: Archivo contiene la interfaz grafica para el manejo de historial como popup
contiene un listbox con el historial y opciones para visualizar o importar.
"""
import customtkinter as ctk
from CTkListbox import *
from CTkMessagebox import CTkMessagebox
from Historial.historial_matriz.historial_popup.historial_importar_popup import HistorialImportarPopup
from Historial.historial_matriz.historial_popup.historial_visualizar_popup import HistorialVisualizacionPopup


class HistorialPopup(ctk.CTkToplevel):
    def __init__(self, parent, historial, matriz_entrada, *args, **kwargs):
        """
        Ventana emergente que muestra el historial de matrices y permite importar una matriz seleccionada.

        Args:
            parent: El widget padre donde se inserta la ventana.
            historial: Lista de matrices guardadas en el historial.
            matriz_entrada: Referencia al array donde se guardará la matriz importada.
        """
        super().__init__(parent, *args, **kwargs)
        self.title("Historial de Matrices")

        self.historial = historial
        self.matriz_entrada = matriz_entrada  # Referencia a la matriz de entrada

        self.label_historial = ctk.CTkLabel(self, text="Historial de matrices")
        self.label_historial.grid(row=0, column=0, columnspan=2, pady=20)

        # Listbox para mostrar el historial de matrices
        self.listbox_matrices = CTkListbox(self, height=80, width=200)
        self.listbox_matrices.grid(row=1, column=0, columnspan=2, padx=50, pady=10)

        # Insertar matrices del historial en la lista
        for idx, matriz in enumerate(self.historial.problemas):
            self.listbox_matrices.insert(ctk.END, f"{matriz['nombre']}")

        # Botón para importar la matriz seleccionada
        self.btn_importar = ctk.CTkButton(self, text="Importar", command=self.importar_matriz)
        self.btn_importar.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Botón para visualizar la opción seleccionada
        self.btn_visualizar = ctk.CTkButton(self, text="Visualizar", command=self.abrir_visualizacion_problema)
        self.btn_visualizar.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Botón para cerrar la ventana emergente
        self.btn_cerrar = ctk.CTkButton(self, text="Cerrar", command=self.cerrar_popup)
        self.btn_cerrar.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

    def importar_matriz(self):
        """Función que importa la matriz seleccionada desde el historial."""
        seleccion = self.listbox_matrices.curselection()
        if seleccion is None:
            CTkMessagebox(
                title="Advertencia",
                message="No tiene nada seleccionado. Por favor seleccione un problema para importar.",
                icon="warning",
                option_1="Entendido",
                button_hover_color="green",
                fade_in_duration=2
            )
            return

        indice = seleccion
        tipo = self.historial.problemas[indice]["tipo"]
        popup_importar = HistorialImportarPopup(self, self.historial, indice)
        popup_importar.grab_set()

        self.wait_window(popup_importar)  # Espera hasta que se cierre el popup
        self.matriz_entrada = popup_importar.matriz_importar

    def cerrar_popup(self):
        """Cierra la ventana emergente."""
        self.destroy()

    def abrir_visualizacion_problema(self):
        """Muestra los valores del problema seleccionado según el tipo."""
        seleccion = self.listbox_matrices.curselection()
        if seleccion is None:
            CTkMessagebox(
                title="Advertencia",
                message="No tiene nada seleccionado. Por favor seleccione un problema.",
                icon="warning",
                option_1="Entendido",
                button_hover_color="green",
                fade_in_duration=2
            )
            return

        indice = seleccion

        popup_visualizacion = HistorialVisualizacionPopup(self, self.historial, indice)
        popup_visualizacion.grab_set()

    def retornar_matriz_importada(self):
        return self.matriz_entrada

