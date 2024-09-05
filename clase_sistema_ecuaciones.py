"""
Archivo: clase_matriz 1.0
Descripcion: archivo que contiene los atributos y metodos de la clase Matriz.
contiene CreadorDeMatriz que funciona como constructor de la clase.
"""
from fractions import Fraction


def CreadorDeEcuaciones():
    class SistemaEcuaciones:
        def __init__(self):
            """
            Inicializa la clase con la matriz aumentada ingresada por el usuario.

            Args:
                matriz (list): Matriz aumentada del sistema de ecuaciones.
            """
            self.nombre = ""
            self.matriz = []
            self.matriz_original = [fila[:] for fila in self.matriz]  # Clonamos la matriz para guardarla como original
            self.filas = len(self.matriz)
            self.columnas = len(self.matriz[0]) - 1  # La última columna es el vector de soluciones
            self.paso = 1  # Contador de pasos

        def mostrar_matriz(self):
            """
            Imprime la matriz actual en cada paso del proceso de Gauss-Jordan.
            """
            print(f"\nPaso {self.paso}:")
            for fila in self.matriz:
                print([str(elemento) for elemento in fila])

        def mostrar_matriz_original(self):
            """
            Imprime la matriz original ingresada por el usuario.
            """
            print("\nMatriz original:")
            for fila in self.matriz_original:
                print([str(elemento) for elemento in fila])

        def gauss_jordan_elimination(self):
            """
            Aplica la eliminación Gauss-Jordan a la matriz aumentada.
            """
            for i in range(min(self.filas, self.columnas)):
                # Seleccionar el pivote, intercambiando filas si el pivote es cero
                if self.matriz[i][i] == 0:
                    for j in range(i + 1, self.filas):
                        if self.matriz[j][i] != 0:
                            self.matriz[i], self.matriz[j] = self.matriz[j], self.matriz[i]
                            self.mostrar_matriz()
                            self.paso += 1
                            break

                # Normalizar la fila del pivote
                pivote = self.matriz[i][i]
                if pivote != 0:
                    for j in range(self.columnas + 1):
                        self.matriz[i][j] /= pivote
                    self.mostrar_matriz()
                    self.paso += 1

                # Eliminar los otros elementos en la columna del pivote
                for j in range(self.filas):
                    if j != i:
                        factor = self.matriz[j][i]
                        for k in range(self.columnas + 1):
                            self.matriz[j][k] -= factor * self.matriz[i][k]
                        self.mostrar_matriz()
                        self.paso += 1

            return self.matriz

        def resolver_sistema(self):
            """
            Resuelve el sistema de ecuaciones lineales a partir de la matriz reducida.

            Returns:
                tuple: Un par que contiene las soluciones y las variables libres, o un mensaje de inconsistencia.
            """
            soluciones = [None] * self.columnas
            variables_libres = []

            # Verificar si el sistema es inconsistente
            for i in range(self.filas):
                if all(self.matriz[i][j] == 0 for j in range(self.columnas)) and self.matriz[i][-1] != 0:
                    return "El sistema no tiene solución"

            # Determinar las variables libres y las dependientes
            for i in range(self.filas):
                pivote_encontrado = False
                for j in range(self.columnas):
                    if self.matriz[i][j] == 1:
                        pivote_encontrado = True
                        soluciones[j] = self.matriz[i][-1]
                        for k in range(j + 1, self.columnas):
                            if self.matriz[i][k] != 0:
                                soluciones[j] = f"{self.matriz[i][-1]} - {self.matriz[i][k]}x{k + 1}"
                        break
                if not pivote_encontrado:
                    variables_libres.append(f"x{i + 1}")

            return soluciones, variables_libres


        def obtener_matriz(self):
            """
            Solicita al usuario los elementos de la matriz aumentada y los convierte en fracciones.

            Returns:
                list: La matriz ingresada por el usuario.
            """
            name = input("Ingrese el nombre e la matriz: . ")
            filas = int(input("Introduce el número de filas de la matriz: "))
            columnas_totales = int(
                input("Introduce el número de columnas de la matriz aumentada (incluyendo el vector solución): "))

            matriz = []
            print("Introduce los elementos de la matriz fila por fila (separados por espacios):")
            for i in range(filas):
                fila_matriz = input(f"Fila {i + 1}: ").split()
                matriz.append([Fraction(x) for x in fila_matriz])

            self.nombre = name
            self.matriz = matriz

        def imprimir_resultado_final(self):
            """
            Imprime la matriz original y las soluciones del sistema (si existen).
            """
            # Imprimir la matriz original
            self.mostrar_matriz_original()

            # Resolver el sistema
            soluciones, variables_libres = self.resolver_sistema()

            # Imprimir la solución
            if isinstance(soluciones, str):
                print("\nSolución:")
                print(soluciones)
            else:
                print("\nSoluciones:")
                for i, solucion in enumerate(soluciones):
                    if solucion:
                        print(f"x{i + 1} = {solucion}")
                    else:
                        print(f"x{i + 1} es libre")

    return SistemaEcuaciones()


# Ejemplo de uso

# # Obtener la matriz ingresada por el usuario
# matriz_aumentada = SistemaEcuaciones.obtener_matriz()
#
# # Crear una instancia del sistema de ecuaciones
# sistema = SistemaEcuaciones(matriz_aumentada)
#
# # Aplicar la eliminación Gauss-Jordan
# matriz_reducida = sistema.gauss_jordan_elimination()
#
# # Imprimir la matriz escalonada reducida
# print("\nMatriz escalonada reducida:")
# sistema.mostrar_matriz()
#
# # Imprimir la matriz original y la solución
# sistema.imprimir_resultado_final()
