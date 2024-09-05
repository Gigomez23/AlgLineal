import random
from fractions import Fraction
import copy


def CreadorDeMatriz():
    class Matriz:
        def __init__(self):
            self.nombre = ""
            self.dimensiones = 0
            self.matriz = []
            self.vector_solucion = []
            self.matriz_original = []
            self.vector_solucion_original = []

        def crear_matriz_aleatoria(self, dimensiones, name):
            """
            Función para crear una matriz con valores aleatorios y un vector solución.

            Args:
                dimensiones (int): dimensión de la matriz.
            """
            self.nombre = name
            self.dimensiones = dimensiones
            self.matriz = [[Fraction(random.randint(1, 10)) for _ in range(dimensiones)] for _ in range(dimensiones)]
            self.vector_solucion = [Fraction(random.randint(1, 10)) for _ in range(dimensiones)]

            # Guardar copia original de la matriz y del vector solución
            self.matriz_original = copy.deepcopy(self.matriz)
            self.vector_solucion_original = copy.deepcopy(self.vector_solucion)

        def ingresar_matriz_usuario(self, dimensiones, name):
            """
            Función que pide al usuario ingresar los datos para crear una matriz y un vector solución de forma manual.

            Args:
                dimensiones (int): dimensión de la matriz.
            """
            self.nombre = name
            self.dimensiones = dimensiones
            matriz = []
            print("Por favor, ingrese los elementos de la matriz fila por fila.")
            for i in range(self.dimensiones):
                fila = list(
                    map(Fraction, input(f"Ingrese los elementos de la fila {i + 1} separados por espacio: ").split()))
                if len(fila) != self.dimensiones:
                    print(f"Error: La fila debe tener {self.dimensiones} elementos.")
                matriz.append(fila)

            self.vector_solucion = list(
                map(Fraction, input(f"Ingrese los elementos del vector solución, separados por espacio: ").split()))
            if len(self.vector_solucion) != self.dimensiones:
                print(f"Error: El vector solución debe tener {self.dimensiones} elementos.")

            self.matriz = matriz

            # Guardar copia original de la matriz y del vector solución
            self.matriz_original = copy.deepcopy(self.matriz)
            self.vector_solucion_original = copy.deepcopy(self.vector_solucion)

        def imprimir_matriz(self, matriz):
            """
            Función para imprimir una matriz.

            Args:
                matriz (list): lista con los datos de la matriz.
            """
            ancho = 10
            for fila in matriz:
                print(" ".join(f"{str(elem):^{ancho}}" for elem in fila))
            print()

        def imprimir_vector(self, vector):
            """
            Función para imprimir un vector.

            Args:
                vector (list): lista con los datos del vector.
            """
            for valor in vector:
                print(f"{str(valor):^10}")
            print()

        def escalonar_matriz(self):
            """
            Función para escalonar la matriz y aplicar las mismas operaciones al vector solución.
            """
            dimensiones = self.dimensiones
            matriz_local = self.matriz
            vector_local = self.vector_solucion

            for i in range(dimensiones):
                pivote = matriz_local[i][i]
                if pivote == 0:
                    for j in range(i + 1, dimensiones):
                        if matriz_local[j][i] != 0:
                            # Intercambiar filas en la matriz y en el vector solución
                            matriz_local[i], matriz_local[j] = matriz_local[j], matriz_local[i]
                            vector_local[i], vector_local[j] = vector_local[j], vector_local[i]
                            print(f"Intercambio: F{i + 1} <--> F{j + 1}")
                            self.imprimir_matriz(matriz_local)
                            pivote = matriz_local[i][i]
                            break
                    else:
                        print(f"La matriz es inconsistente en la fila {i + 1}.")
                        return False

                # Escalar fila para que el pivote sea 1
                if pivote != 1:
                    matriz_local[i] = [x / pivote for x in matriz_local[i]]
                    vector_local[i] /= pivote
                    pivote_fraction = Fraction(pivote)
                    print(f"F{i + 1} --> (1/{pivote_fraction.limit_denominator()}) * F{i + 1}")
                    self.imprimir_matriz(matriz_local)
                    self.imprimir_vector(vector_local)

                # Eliminar los elementos en las otras filas
                for j in range(dimensiones):
                    if j != i:
                        factor = matriz_local[j][i]
                        factor_fraction = Fraction(factor)
                        matriz_local[j] = [matriz_local[j][k] - factor * matriz_local[i][k] for k in range(dimensiones)]
                        vector_local[j] -= factor * vector_local[i]
                        print(f"F{j + 1} --> F{j + 1} - ({factor_fraction.limit_denominator()}) * F{i + 1}")
                        self.imprimir_matriz(matriz_local)
                        self.imprimir_vector(vector_local)
            return True

        def resolver_matriz(self, imprimir_solucion=False):
            """
            Función para resolver la matriz utilizando escalonamiento.
            Args:
                imprimir_solucion (bool): Si es True, imprime el vector solución después de resolver la matriz.
            """
            # Trabajar en una copia de la matriz original y del vector solución
            self.matriz = copy.deepcopy(self.matriz_original)
            self.vector_solucion = copy.deepcopy(self.vector_solucion_original)

            print("Matriz inicial:")
            self.imprimir_matriz(self.matriz)
            print("Vector solución inicial:")
            self.imprimir_vector(self.vector_solucion)

            if self.escalonar_matriz():
                print("La matriz ha sido escalonada y el vector solución ha sido actualizado:")
                self.imprimir_matriz(self.matriz)
                self.imprimir_vector(self.vector_solucion)

                if imprimir_solucion:
                    print("Solución del sistema:")
                    self.imprimir_vector(self.vector_solucion)
            else:
                print("La matriz es inconsistente.")

        def imprimir_matrices_para_historial(self):
            """
            Función que imprime la matriz original y el vector solución original.
            """
            print("Matriz Inicial: ")
            self.imprimir_matriz(self.matriz_original)

            print("Vector Solución Inicial: ")
            self.imprimir_vector(self.vector_solucion_original)

    return Matriz()
