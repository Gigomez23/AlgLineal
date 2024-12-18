"""
Archivo: clase_matriz_operaciones.py 2.0.5
Descripción: Archivo que resuelve segun la leyes de las matrices la multiplicacion de una matriz con
un vector.
"""
from fractions import Fraction


def CreadorDeOperaciones():
    class MatrizOperaciones:
        def __init__(self):
            self.nombre = ""
            self.A = []
            self.b = []
            self.solucion = []
            self.filas_A = 0
            self.columnas_A = 0
            self.filas_b = 0

        def multiplicar_con_pasos(self, text_salida, mostrar_pasos=False):
            resultado = [0] * self.filas_A
            if mostrar_pasos:
                text_salida.insert("end", "\nMultiplicación paso a paso:\n")
            for i in range(self.filas_A):
                suma = 0
                for j in range(self.columnas_A):
                    # Desempaqueta el valor de b si es una lista de listas
                    valor_b = self.b[j][0] if isinstance(self.b[j], list) else self.b[j]
                    multiplicacion = self.A[i][j] * valor_b
                    suma += multiplicacion
                    if mostrar_pasos:
                        text_salida.insert("end",
                                           f"A[{i + 1}][{j + 1}] * b[{j + 1}] = {self.A[i][j]} * {valor_b} = {multiplicacion}\n")
                resultado[i] = suma
                if mostrar_pasos:
                    text_salida.insert("end", f"Suma fila {i + 1}: {suma}\n")
            return resultado

        def imprimir_matrices(self, text_salida):
            text_salida.insert("end", "\nMatriz A:\n")
            for fila in self.A:
                text_salida.insert("end", f"{[str(Fraction(x)) for x in fila]}\n")

            text_salida.insert("end", "\nVector/matriz b:\n")
            for valor in self.b:
                text_salida.insert("end", f"{str(valor)}\n")
                # text_salida.insert("end", f"{valor}\n")

        def imprimir_solucion(self, text_salida, mostrar_pasos=False):
            resultado = self.multiplicar_con_pasos(text_salida, mostrar_pasos)
            text_salida.insert("end", "\nResultado de Ax = b:\n")
            for i, valor in enumerate(resultado):
                text_salida.insert("end", f"Fila {i + 1}: {valor}\n")
                self.solucion.insert(i, valor)

    return MatrizOperaciones()