"""
Archivo: operaciones_calc.py 1.0.0
Descripción: Este archivo contiene la interfáz gráfica de la calculadora de operaciones de matrices.
"""


class Historial:
    def __init__(self):
        self.problemas = []

    def agregar_problema(self, matriz1, matriz2, solucion):
        problema = {
            "nombre": f"Problema {len(self.problemas) + 1}",
            "matriz entrada 1": matriz1,
            "matriz entrada 2": matriz2,
            "solucion": solucion
        }
        self.problemas.append(problema)

    def obtener_problema(self, indice):
        if 0 <= indice < len(self.problemas):
            return self.problemas[indice]
        return None

    def obtener_historial(self):
        return self.problemas

