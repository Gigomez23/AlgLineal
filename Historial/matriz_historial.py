"""
Archivo: operaciones_calc.py 1.5.0
Descripción: Este archivo contiene la interfáz gráfica de la calculadora de operaciones de matrices.
"""


class Historial:
    def __init__(self):
        self.problemas = []

    def agregar_problema(self, matriz1=None, matriz2=None, matriz3=None, matriz4=None, solucion=None, tipo=None,
                         clasificacion=None):
        problema = {
            "nombre": f"Problema {len(self.problemas) + 1}",
            "matriz entrada 1": matriz1,
            "matriz entrada 2": matriz2,
            "matriz entrada 3": matriz3,
            "matriz entrada 4": matriz4,
            "solucion": solucion,
            "tipo": tipo,  # uno, dos, tres, cuatro
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

