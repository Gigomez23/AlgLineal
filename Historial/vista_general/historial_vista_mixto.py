"""
Archivo: historial_vista_mixto.py 1.0.5
Descripción: Este archivo contiene el frame interno para mostrar problemas mixtos en el historial general.
"""
from customtkinter import *
from Historial.matriz_historial import *
from Historial.visualizador.historial_visualizar_popup1 import HistorialVisualizacionPopup1
from Historial.visualizador.historial_visualizar_popup2 import HistorialVisualizacionPopup2
from Historial.visualizador.historial_visualizar_popup3 import HistorialVisualizacionPopup3


class HistorialMixtoFrame(CTkFrame):
    def __init__(self, parent, historial):
        """
        Frame que muestra todos los problemas con clasificación 'matriz' del historial.

        Args:
            parent: El widget padre para este frame.
            historial: La instancia de la clase Historial que contiene todos los problemas.
        """
        super().__init__(parent)
        self.historial = historial

        self.frame_historial = CTkScrollableFrame(master=self)  # Cambiado a CTkScrollableFrame
        self.frame_historial.pack(fill="both", expand=True, padx=10, pady=10)

        self.mostrar_historial_matriz()

    def mostrar_historial_matriz(self):
        """
        Muestra los problemas de tipo 'matriz' y agrega un botón para visualizar cada uno.
        """
        problemas_matriz = self.historial.obtener_historial_mixtos()

        for i, problema in enumerate(problemas_matriz):
            # Mostrar el nombre del problema
            nombre_label = CTkLabel(self.frame_historial, text=f"{problema['nombre']}:")
            nombre_label.grid(row=i, column=0, padx=10, pady=5)

            # Agregar un botón para visualizar más detalles del problema y pasar el nombre
            visualizar_btn = CTkButton(self.frame_historial, text="Visualizar",
                                       command=lambda nombre=problema["nombre"]: self.visualizar_problema(nombre))
            visualizar_btn.grid(row=i, column=1, padx=10, pady=5)

    def visualizar_problema(self, nombre_problema):
        """
        Muestra una ventana emergente con los detalles del problema seleccionado,
        buscando el problema por su nombre.

        Args:
            nombre_problema: El nombre del problema a visualizar.
        """
        # Encontrar el índice del problema basado en el nombre
        indice = next(
            (i for i, problema in enumerate(self.historial.problemas) if problema["nombre"] == nombre_problema), None)

        if indice is not None:
            if self.historial.problemas[indice]["tipo"] == "uno":
                popup_visualizacion = HistorialVisualizacionPopup1(self, self.historial, indice)
                popup_visualizacion.grab_set()
            elif self.historial.problemas[indice]["tipo"] == "dos":
                popup_visualizacion = HistorialVisualizacionPopup2(self, self.historial, indice)
                popup_visualizacion.grab_set()
            elif self.historial.problemas[indice]["tipo"] == "tres":
                popup_visualizacion = HistorialVisualizacionPopup3(self, self.historial, indice)
                popup_visualizacion.grab_set()
        else:
            print("Problema no encontrado.")

    # Ejemplo de cómo usar el frame con la función de visualización


if __name__ == "__main__":
    app = CTk()
    app.geometry("600x400")

    historial = Historial()
    # Agregar algunos problemas de ejemplo
    historial.agregar_problema([[1, 2], [3, 4]], None, None, [[5, 6], [7, 8]], "uno", "matriz")
    historial.agregar_problema([[1, 0], [0, 1]], None, None, [[0, 0], [0, 0]], "dos", "vector")
    historial.agregar_problema([[2, 3], [4, 5]], None, None, [[6, 7], [8, 9]], "tres", "matriz")

    # Crear el frame con la lista de problemas de matrices
    historial_frame = HistorialMixtoFrame(app, historial)
    historial_frame.pack(padx=20, pady=20)

    app.mainloop()
