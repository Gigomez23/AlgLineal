"""
Archivo: operaciones_determinante.py 1.2.0
Descripción: Este archivo contiene la clase para encontrar la determinante
"""
from fractions import Fraction


def CreadorDeOperacionDeterminantes():
    class OperacionesDeterminante:
        def __init__(self):
            self.matriz = []
            self.procedimiento = ""
            self.determinantes = []

        def ingresar_datos(self, matriz):
            """Recibe una matriz ya validada y la almacena."""
            self.matriz = matriz

        def calcular_determinante(self):
            """Calcula el determinante de la matriz utilizando el método de Laplace."""
            self.procedimiento = ""
            resultado = self._determinante(self.matriz, 0)
            self.procedimiento += f"\ndet A = {resultado}\n"

            # Guardar solo el determinante en la lista de determinantes
            self.determinantes.append(resultado)

            return resultado

        def _determinante(self, matriz, nivel):
            """Función recursiva para calcular el determinante utilizando el método de Laplace."""
            if len(matriz) == 2:  # Caso base para matriz 2x2
                return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]

            det = Fraction(0)  # Inicializa el determinante
            for col in range(len(matriz)):
                submatriz = self._crear_submatriz(matriz, 0, col)
                cofactor = ((-1) ** col) * matriz[0][col]
                det_submatriz = self._determinante(submatriz, nivel + 1)
                det += cofactor * det_submatriz

                if nivel == 0:  # Solo formatear la primera expansión
                    submatriz_str = self._formatear_matriz_como_matriz(submatriz)
                    self.procedimiento += (
                        f"\n{'  ' * nivel}{cofactor} * \n{submatriz_str} = {cofactor * det_submatriz}\n"
                    )

            return det


        def _crear_submatriz(self, matriz, fila_eliminar, col_eliminar):
            """Genera una submatriz eliminando una fila y una columna específicas."""
            return [
                [matriz[i][j] for j in range(len(matriz)) if j != col_eliminar]
                for i in range(len(matriz)) if i != fila_eliminar
            ]

        def _formatear_matriz_como_matriz(self, matriz):
            """Formatea una matriz para que se muestre como una matriz tradicional."""
            filas = ["|" + " ".join([f"{str(x):>4}" for x in fila]) + "|" for fila in matriz]
            return "\n".join(filas)

        def obtener_procedimiento(self):
            """Devuelve el procedimiento paso a paso."""
            return self.procedimiento

    return OperacionesDeterminante()
