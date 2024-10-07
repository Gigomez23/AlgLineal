"""
Archivo: clase_matriz_op_ari.py 1.10.0
Descripción: Este archivo contiene la interfáz gráfica de la calculadora de operaciones de matrices.
"""
from fractions import Fraction


def CreadorDeMatricesAritmeticas():
    class OperacionesMatricesAritmeticas:
        def __init__(self):
            self.matriz1 = []
            self.matriz2 = []
            self.resultado = []
            self.procedimiento = ""

        def suma_matrices(self):
            """Función que suma las matrices y muestra el procedimiento"""
            self.resultado = []
            self.procedimiento = "Procedimiento para la suma de matrices:\n"
            for i in range(len(self.matriz1)):
                fila_resultado = []
                for j in range(len(self.matriz1[0])):
                    suma = self.matriz1[i][j] + self.matriz2[i][j]
                    fila_resultado.append(suma)
                    self.procedimiento += f"Elemento [{i+1}, {j+1}] = {self.matriz1[i][j]} + {self.matriz2[i][j]} = {suma}\n"
                self.resultado.append(fila_resultado)

        def resta_matrices(self):
            """Función que resta las matrices y muestra el procedimiento"""
            self.resultado = []
            self.procedimiento = "Procedimiento para la resta de matrices:\n"
            for i in range(len(self.matriz1)):
                fila_resultado = []
                for j in range(len(self.matriz1[0])):
                    resta = self.matriz1[i][j] - self.matriz2[i][j]
                    fila_resultado.append(resta)
                    self.procedimiento += f"Elemento [{i+1}, {j+1}] = {self.matriz1[i][j]} - {self.matriz2[i][j]} = {resta}\n"
                self.resultado.append(fila_resultado)

        def multiplicar_matrices(self):
            """Función que multiplica las matrices"""
            filas_matriz1 = len(self.matriz1)
            columnas_matriz1 = len(self.matriz1[0])
            columnas_matriz2 = len(self.matriz2[0])

            self.resultado = [
                [sum(self.matriz1[i][k] * self.matriz2[k][j] for k in range(columnas_matriz1))
                 for j in range(columnas_matriz2)]
                for i in range(filas_matriz1)
            ]

            self.procedimiento = "Procedimiento para la multiplicación:\n"
            for i in range(filas_matriz1):
                for j in range(columnas_matriz2):
                    pasos = []
                    for k in range(columnas_matriz1):
                        multiplicacion = f"{self.matriz1[i][k]} * {self.matriz2[k][j]}"
                        pasos.append(multiplicacion)
                    suma_procedimiento = " + ".join(pasos)
                    self.procedimiento += f"Elemento [{i+1}, {j+1}] = {suma_procedimiento} = {self.resultado[i][j]}\n"

        def formato_matriz(self, matriz):
            """Función para aplicar el formato adecuado a la matriz ingresada"""
            return "\n".join([" ".join([str(Fraction(x)) for x in fila]) for fila in matriz]) + "\n"

    return OperacionesMatricesAritmeticas()
