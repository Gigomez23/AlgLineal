import customtkinter as ctk
from CTkListbox import *
from Historial.historial_visualizar_popup import *
from Historial.escoger_matriz import HistorialImportarPopup


class HistorialPopup(ctk.CTkToplevel):
    def __init__(self, parent, historial, campo_entrada, *args, **kwargs):
        """
        Ventana emergente que muestra el historial de matrices y permite importar una matriz seleccionada.

        Args:
            parent: El widget padre donde se inserta la ventana.
            historial: Lista de matrices guardadas en el historial.
        """
        super().__init__(parent, *args, **kwargs)
        self.title("Historial de Matrices")  # Título de la ventana emergente

        self.historial = historial
        self.campo_entrada = campo_entrada  # Añadimos el campo de entrada
        self.matriz_importar = []


        self.label_historial = ctk.CTkLabel(self, text="Historial de matrices")
        self.label_historial.grid(row=0, column=0, columnspan=2, pady=20)

        # Listbox para mostrar el historial de matrices
        self.listbox_matrices = CTkListbox(self, height=30, width=200)
        self.listbox_matrices.grid(row=1, column=0, columnspan=2, padx=50, pady=10)

        # Insertar matrices del historial en la lista
        for idx, matriz in enumerate(self.historial.problemas):
            self.listbox_matrices.insert(ctk.END, f"{matriz['nombre']}")

        # todo: develop this function
        # Botón para importar la matriz seleccionada
        self.btn_importar = ctk.CTkButton(self, text="Importar", command=self.importar_matriz)
        self.btn_importar.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # botón para visualizar la opción seleccionada
        self.btn_visualizar = ctk.CTkButton(self, text="Visualizar",
                                            command=self.abrir_visualizacion_problema)
        self.btn_visualizar.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Botón para cerrar la ventana emergente
        self.btn_cerrar = ctk.CTkButton(self, text="Cerrar", command=self.cerrar_popup)
        self.btn_cerrar.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

    # todo: desarollar esta vaina
    def importar_matriz(self):
        """Función que importa la matriz seleccionada desde el frame HistorialImportarPopup"""
        seleccion = self.listbox_matrices.curselection()
        if seleccion:
            popup_importar = HistorialImportarPopup(self, self.historial, seleccion)
            popup_importar.grab_set()
            self.wait_window(popup_importar)  # Espera hasta que se cierre el popup

            # Verificar si se ha importado una matriz
            if popup_importar.matriz_importar is not None:
                matriz_importada = popup_importar.matriz_importar
                # Actualiza el campo de entrada con la matriz importada
                self.campo_entrada.delete(1.0, ctk.END)  # Borra el contenido actual del campo
                self.campo_entrada.insert(ctk.END, str(matriz_importada))  # Inserta la matriz importada

    def cerrar_popup(self):
        """Cierra la ventana emergente."""
        self.destroy()  # Cierra la ventana pop-up

    def abrir_visualizacion_problema(self):
        indice = self.listbox_matrices.curselection()
        popup_visualizacion = HistorialVisualizacionPopup(self, self.historial, indice)
        popup_visualizacion.grab_set()
