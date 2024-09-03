import random
from fractions import Fraction


def CreadorDeMatriz():
    class Matriz:
        def __init__(self):
            self.nombre = ""
            self.dimensiones = 0
            self.matriz = []
            self.matriz_identidad = []
            self.vector_solucion = []

        def crear_matriz_aleatoria(self, dimensiones, name):
            """
            Funcion para crear una matriz con valores aleatorios

            Args:
                dimensiones (int): dimension de la matriz
            """
            self.nombre = name
            self.dimensiones = dimensiones
            self.matriz = [[random.randint(1, 10) for _ in range(dimensiones)] for _ in range(dimensiones)]

        def ingresar_matriz_usuario(self, dimensiones, name):
            """
             Funcion que pide al usuario ingresar los datos.
             para crear una matriz de forma manual.

             Args:
                 dimensiones (int): dimensione de la matriz
             """
            self.nombre = name
            self.dimensiones = dimensiones
            matriz = []
            print("Por favor, ingrese los elementos de la matriz fila por fila.")
            for i in range(self.dimensiones):
                fila = list(map(int, input(
                    f"Ingrese los elementos de la fila {i + 1} separados por espacio (solo números positivos): ").split()))
                if len(fila) != self.dimensiones:
                    print(f"Error: La fila debe tener {self.dimensiones} elementos.")
                matriz.append(fila)
            self.matriz = matriz

        def imprimir_matriz(self, matriz):
            """
             Funcion para imprimir una matriz.

             Args:
                 matriz (int): lista con los datos de la matriz.
             """
            ancho = 10
            for fila in matriz:
                print(" ".join(f"{str(Fraction(elem).limit_denominator()):^{ancho}}" if isinstance(elem, float)
                               else f"{str(elem):^{ancho}}" for elem in fila))
            print()

        def escalonar_matriz(self):
            """
                 Funcion para escalonar la matriz.
             """
            dimensiones = self.dimensiones
            matriz = self.matriz

            for i in range(dimensiones):
                pivote = matriz[i][i]
                if pivote == 0:
                    for j in range(i + 1, dimensiones):
                        if matriz[j][i] != 0:
                            matriz[i], matriz[j] = matriz[j], matriz[i]
                            print(f"Intercambio: F{i + 1} <--> F{j + 1}")
                            self.imprimir_matriz(self.matriz)
                            pivote = matriz[i][i]
                            break
                    else:
                        print(f"La matriz es inconsistente en la fila {i + 1}.")
                        return False

                if pivote != 1:
                    matriz[i] = [x / pivote for x in matriz[i]]
                    pivote_fraction = Fraction(pivote)
                    print(f"F{i + 1} --> (1/{pivote_fraction.limit_denominator()}) * F{i + 1}")
                    self.imprimir_matriz(self.matriz)

                for j in range(dimensiones):
                    if j != i:
                        factor = matriz[j][i]
                        factor_fraction = Fraction(factor)
                        matriz[j] = [matriz[j][k] - factor * matriz[i][k] for k in range(dimensiones)]
                        print(f"F{j + 1} --> F{j + 1} - ({factor_fraction.limit_denominator()}) * F{i + 1}")
                        self.imprimir_matriz(self.matriz)
            return True

        def crear_matriz_identidad(self):
            """
             Funcion para crear la matriz identidad.
             """
            self.matriz_identidad = [[1 if i == j else 0 for j in range(self.dimensiones)] for i in
                                     range(self.dimensiones)]

        def resolver_matriz(self):
            """
                 Funcion para resolver la matriz.
             """
            print("Matriz inicial:")
            self.imprimir_matriz(self.matriz)

            if self.escalonar_matriz():
                print("La matriz ha sido transformada a una matriz identidad:")
                self.imprimir_matriz(self.matriz_identidad)
            else:
                print("La matriz es inconsistente.")

    return Matriz()