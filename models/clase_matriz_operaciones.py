"""
Archivo: clase_matriz_operaciones.py 1.2.1
Descripción: Archivo que resuelve segun la leyes de las matrices la multiplicacion de una matriz con
un vector.
"""
from fractions import Fraction


def CreadorDeOperaciones():
    """
    Función que inicializa una instancia del objeto MultiplicacionMatrices.
    :return (obj): clase
    """

    class MatrizOperaciones:
        """
        Esta clase contiene métodos para realizar la multiplicación Ax = b.

        Args:
            A (list): matriz de coeficientes A
            b (list): vector/matriz de soluciones b
            filas_A (int): número de filas de A
            columnas_A (int): número de columnas de A
            filas_b (int): número de filas de b
        """

        def __init__(self):
            self.nombre = ""
            self.A = []
            self.b = []
            self.filas_A = 0
            self.columnas_A = 0
            self.filas_b = 0

        def ingresar_datos(self):
            """
            Permite al usuario ingresar los valores de las matrices A y b desde la consola.
            """
            # Ingresar la matriz A
            self.nombre = input("Ingrese el nombre del problema: ")
            self.filas_A = int(input("Ingrese el número de filas de la matriz A: "))
            self.columnas_A = int(input("Ingrese el número de columnas de la matriz A: "))
            print("Ingrese los elementos de la matriz A fila por fila (separados por espacios):")
            self.A = []
            for i in range(self.filas_A):
                fila = input(f"Fila {i + 1}: ").split()
                self.A.append([Fraction(x) for x in fila])

            # Ingresar el vector/matriz b
            self.filas_b = int(input("Introduce el número de filas del vector/matriz b: "))
            if self.filas_b != self.columnas_A:
                print("Error: El número de filas de b debe ser igual al número de columnas de A.")
                return

            print("Introduce los elementos del vector/matriz b:")
            self.b = []
            for i in range(self.filas_b):
                valor = Fraction(input(f"b[{i + 1}]: "))
                self.b.append(valor)

        def multiplicar_con_pasos(self):
            """
            Realiza la multiplicación Ax = b mostrando cada paso del cálculo.
            :return (list): resultado de la multiplicación.
            """
            resultado = [0] * self.filas_A
            print("\nPasos de la multiplicación Ax = b:\n")

            for i in range(self.filas_A):
                suma = 0
                print(f"Calculando fila {i + 1} del resultado:")

                for j in range(self.columnas_A):
                    multiplicacion = self.A[i][j] * self.b[j]
                    suma += multiplicacion
                    print(f"A[{i + 1}][{j + 1}] * b[{j + 1}] = {self.A[i][j]} * {self.b[j]} = {multiplicacion}")

                resultado[i] = suma
                print(f"Suma fila {i + 1}: {resultado[i]}\n")

            return resultado

        def mostrar_resultado_con_pasos(self):
            """
            Muestra el resultado de la multiplicación Ax = b y cada paso realizado.
            """
            resultado = self.multiplicar_con_pasos()
            print("Resultado final de Ax = b:")
            for i, valor in enumerate(resultado):
                print(f"Fila {i + 1}: {valor}")

        def imprimir_matrices_y_solucion(self):
            """
            Imprime las matrices A, b y el resultado Ax = b, mostrando los pasos.
            """
            # Imprimir la matriz A
            print("\nMatriz A:")
            for fila in self.A:
                print([str(Fraction(x)) for x in fila])

            # Imprimir el vector/matriz b
            print("\nVector/matriz b:")
            for valor in self.b:
                print(str(Fraction(valor)))

            # Imprimir el resultado con pasos
            print("\nResultado y pasos para Ax = b:")
            self.mostrar_resultado_con_pasos()

        def imprimir_matrices_para_historial(self):
            self.imprimir_matrices_y_solucion()

    return MatrizOperaciones()
