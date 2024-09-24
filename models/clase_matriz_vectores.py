"""
Archivo: clase_matriz_vectores.py.py 1.0.0
Descripción: Archivo con la clase para resolver un problema de tipo Au + Av
"""
def CreadorDeOperacionMatrizVector():
    class MatrizVectores:
        def __init__(self):
            self.A = []
            self.u = []
            self.v = []
            self.filas_A = 0
            self.columnas_A = 0

        def multiplicar_con_pasos(self, vector, text_salida, mostrar_pasos=False):
            resultado = [0] * self.filas_A
            if mostrar_pasos:
                text_salida.insert("end", "\nMultiplicación paso a paso:\n")
            for i in range(self.filas_A):
                suma = 0
                for j in range(self.columnas_A):
                    multiplicacion = self.A[i][j] * vector[j]
                    suma += multiplicacion
                    if mostrar_pasos:
                        text_salida.insert("end",
                                           f"A[{i + 1}][{j + 1}] * vector[{j + 1}] = {self.A[i][j]} * {vector[j]} = {multiplicacion}\n")
                resultado[i] = suma
                if mostrar_pasos:
                    text_salida.insert("end", f"Suma fila {i + 1}: {suma}\n")
            return resultado

        def imprimir_solucion(self, metodo, text_salida, mostrar_pasos=False):
            if metodo == "directo" or metodo == "ambos":
                # Resolver A(u + v)
                vector_suma = [self.u[i] + self.v[i] for i in range(self.columnas_A)]
                text_salida.insert("end", "\nCalculando A(u + v):\n")
                resultado_directo = self.multiplicar_con_pasos(vector_suma, text_salida, mostrar_pasos)
                text_salida.insert("end", "\nResultado de A(u + v):\n")
                for i, valor in enumerate(resultado_directo):
                    text_salida.insert("end", f"Fila {i + 1}: {valor}\n")

            if metodo == "separado" or metodo == "ambos":
                # Resolver A(u) y A(v) por separado
                text_salida.insert("end", "\nCalculando A(u):\n")
                resultado_u = self.multiplicar_con_pasos(self.u, text_salida, mostrar_pasos)
                text_salida.insert("end", "\nCalculando A(v):\n")
                resultado_v = self.multiplicar_con_pasos(self.v, text_salida, mostrar_pasos)
                text_salida.insert("end", "\nResultado de A(u) + A(v):\n")
                resultado_separado = [resultado_u[i] + resultado_v[i] for i in range(self.filas_A)]
                for i, valor in enumerate(resultado_separado):
                    text_salida.insert("end", f"Fila {i + 1}: {valor}\n")

    return MatrizVectores()