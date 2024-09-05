"""
Archivo: clase_matriz 2.2
Descripcion: archivo que contiene los atributos y metodos de la clase Matriz.
contiene CreadorDeMatriz que funciona como constructor de la clase.
"""
import random
from fractions import Fraction
import copy

def CreadorDeMatriz():
    """
    Funcion que inicializa una instancia del objeto de matriz.

    Returns:
         (obj): clase Matriz
    """
    class Matriz:
        """
        Esta clase contiene varios objetos de matrices aumentadas cuadradas.

        Args:
            nombre (str): cadena de caracteres que conforman el nombre para identificar el objeto.
            dimensiones (int): dato que representa la dimension de la matriz cuadrada
            matriz (list): lista que representa la matriz
            matriz_original (list): lista que donde se guarda la matriz original

        A
        """
        def __init__(self):
            self.nombre = ""
            self.dimensiones = 0
            self.matriz = []
            self.matriz_original = []

        def crear_matriz_aleatoria(self, dimensiones, name):
            """
            Función para crear una matriz con valores aleatorios, incluyendo la columna del vector solución.

            Args:
                dimensiones (int): dimensión de la matriz (sin contar la columna del vector solución).
            """
            self.nombre = name
            self.dimensiones = dimensiones
            self.matriz = [[Fraction(random.randint(1, 10)) for _ in range(dimensiones + 1)] for _ in
                           range(dimensiones)]

            # Guardar copia original de la matriz
            self.matriz_original = copy.deepcopy(self.matriz)

        def ingresar_matriz_usuario(self, dimensiones, name):
            """
            Función que pide al usuario ingresar los datos para crear una matriz
            extendida (incluyendo la columna del vector solución).

            Args:
                dimensiones (int): dimensión de la matriz (sin contar la columna del vector solución).
            """
            self.nombre = name
            self.dimensiones = dimensiones
            matriz = []
            print("Por favor, ingrese los elementos de la matriz (incluyendo la columna del vector solución).")
            for i in range(self.dimensiones):
                fila = list(map(Fraction, input(
                    f"Ingrese los elementos de la fila {i + 1} separados por espacio "
                    f"(incluya el valor de la columna del vector solución): ").split()))
                if len(fila) != self.dimensiones + 1:
                    print(
                        f"Error: La fila debe tener {self.dimensiones + 1} elementos (la última "
                        f"columna es el vector solución).")
                    return
                matriz.append(fila)

            self.matriz = matriz

            # Guardar copia original de la matriz
            self.matriz_original = copy.deepcopy(self.matriz)

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

        def escalonar_matriz(self):
            """
            Función para escalonar la matriz. Imprime cada paso del proceso de escalonamiento.
            """
            dimensiones = self.dimensiones
            matriz_local = self.matriz

            for i in range(dimensiones):
                pivote = matriz_local[i][i]
                if pivote == 0:
                    for j in range(i + 1, dimensiones):
                        if matriz_local[j][i] != 0:
                            # Intercambiar filas en la matriz
                            matriz_local[i], matriz_local[j] = matriz_local[j], matriz_local[i]
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
                    pivote_fraction = Fraction(pivote)
                    print(f"F{i + 1} --> (1/{pivote_fraction.limit_denominator()}) * F{i + 1}")
                    self.imprimir_matriz(matriz_local)

                # Eliminar los elementos en las otras filas
                for j in range(dimensiones):
                    if j != i:
                        factor = matriz_local[j][i]
                        factor_fraction = Fraction(factor)
                        matriz_local[j] = [matriz_local[j][k] - factor * matriz_local[i][k] for k in
                                           range(dimensiones + 1)]
                        print(f"F{j + 1} --> F{j + 1} - ({factor_fraction.limit_denominator()}) * F{i + 1}")
                        self.imprimir_matriz(matriz_local)
            return True

        def resolver_matriz(self, imprimir_solucion=True):
            """
            Función para resolver la matriz extendida utilizando escalonamiento.
            Args:
                imprimir_solucion (bool): Si es True, imprime el vector solución después de resolver la matriz.
            """
            # Trabajar en una copia de la matriz original
            self.matriz = copy.deepcopy(self.matriz_original)

            print("Matriz inicial (incluyendo la columna del vector solución):")
            self.imprimir_matriz(self.matriz)

            if self.escalonar_matriz():
                print("La matriz ha sido escalonada:")
                self.imprimir_matriz(self.matriz)

                if imprimir_solucion:
                    print("Solución del sistema (Vector Solución Final):")
                    vector_solucion = [self.matriz[i][-1] for i in range(self.dimensiones)]
                    self.imprimir_matriz([[x] for x in vector_solucion])
                    self.imprimir_soluciones_formateadas(vector_solucion)
            else:
                print("La matriz es inconsistente.")
                print("No se pudo obtener una solución.")

        def imprimir_soluciones_formateadas(self, vector_solucion):
            """
            Función para imprimir el resultado del sistema en forma de ecuaciones como 'x1 = valor'.
            """
            print("\nSoluciones del sistema:")
            for i, valor in enumerate(vector_solucion):
                if all(elemento == 0 for elemento in self.matriz[i][:-1]):  # Verificar si la fila es 0
                    print(f"x{i + 1} es libre")
                else:
                    print(f"x{i + 1} = {valor}")

        def imprimir_matrices_para_historial(self):
            """
            Función que imprime la matriz original y la matriz escalonada.
            """
            print("Matriz Inicial (incluyendo la columna del vector solución): ")
            self.imprimir_matriz(self.matriz_original)

            print("")

            print("Matriz Escalonada: ")
            self.imprimir_matriz(self.matriz)

    return Matriz()

