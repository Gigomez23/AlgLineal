"""
Archivo: historial_general_ui.py 1.5.0
Descripción: Este archivo contiene el frame para el historial general divida en pestañas.
"""
from customtkinter import *
from Historial.historial_matriz.vista_general.historial_vista_matriz import HistorialMatrizFrame
from Historial.historial_matriz.vista_general.historial_vista_mixto import HistorialMixtoFrame
from Historial.historial_matriz.vista_general.historial_vista_vector import HistorialVectorFrame


class HistorialGeneralFrame(CTkFrame):
    def __init__(self, parent, historial, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # se inicializa el historial
        self.historial = historial

        # Crear el Tabview para las opciones del menú
        self.tabview = CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # Crear las pestañas (tab)
        self.tab_matrices = self.tabview.add("Historial de Operaciones de Matrices")
        self.tab_mixta = self.tabview.add("Historial de Operaciones Mixtas")
        self.tab_vectores = self.tabview.add("Historial de Operaciones de Vectores")

        # Inicializar directamente el frame correspondiente en cada pestaña
        self.frame_vectores = HistorialVectorFrame(self.tab_vectores, self.historial)
        self.frame_vectores.pack(fill="both", expand=True)

        self.frame_matrices = HistorialMatrizFrame(self.tab_matrices, self.historial)
        self.frame_matrices.pack(fill="both", expand=True)

        self.frame_mixta = HistorialMixtoFrame(self.tab_mixta, self.historial)
        self.frame_mixta.pack(fill="both", expand=True)


