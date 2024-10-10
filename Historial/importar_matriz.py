"""
Archivo: importar_matriz.py 1.0.0
Descripción: Este archivo contiene la clase para manejar datos a importar desde el historial.
"""


class Importar:
    def __init__(self):
        self.matriz_importada = []

    def establecer_dato(self, matriz):
        self.matriz_importada = matriz

    def obtener_dato(self):
        return self.matriz_importada

