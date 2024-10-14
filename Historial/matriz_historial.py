"""
Archivo: operaciones_calc.py 1.5.0
Descripción: Este archivo contiene la interfáz gráfica de la calculadora de operaciones de matrices.
"""


class Historial:
    def __init__(self):
        self.problemas = []

    def agregar_problema(self, matriz1, matriz2, matriz3, solucion, tipo, clasificacion):
        problema = {
            "nombre": f"Problema {len(self.problemas) + 1}",
            "matriz entrada 1": matriz1,
            "matriz entrada 2": matriz2,
            "matriz entrada 3": matriz3,
            "solucion": solucion,
            "tipo": tipo,  # uno, dos, tres
            "clasificacion": clasificacion  # matriz, vector, mixto
        }
        self.problemas.append(problema)

    def obtener_problema(self, indice):
        if 0 <= indice < len(self.problemas):
            return self.problemas[indice]
        return None

    def obtener_historial(self):
        return self.problemas

    def obtener_historial_matriz(self):
        return [problema for problema in self.problemas if problema["clasificacion"] == "matriz"]

    def obtener_historial_vector(self):
        return [problema for problema in self.problemas if problema["clasificacion"] == "vector"]

    def obtener_historial_mixtos(self):
        return [problema for problema in self.problemas if problema["clasificacion"] == "mixto"]

