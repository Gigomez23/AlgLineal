"""
Archivo: clase_sistema_ecuaciones.py 2.0.2
Descripcion: archivo que contiene los atributos y metodos de la clase GaussJordan.
contiene CreadorDeEcuaciones() que funciona como constructor de la clase.
"""
from fractions import Fraction

def CreadorDeEcuaciones():
    """
    Funcion que inicializa una instancia del objeto GaussJordan
    :return (obj): clase GaussJordan
    """
    class GaussJordan:
        """
        Esta clase contiene varios objetos de matrices reducidas y metodos para resolver.

        Args:
            nombre (str): cadena de caracteres que conforman el nombre para identificar la matriz
            matriz (list): lista de datos que representan las matrices
            filas (int): dato que representa la cantidad de filas en la matriz
            columnas (int): dato que representa la cantidad de columnas en la matriz
        """
        def _init_(self):
            self.nombre = ""
            self.matriz = []

        def pivotea(self, fila, columna):
            """
            Asegura que el elemento en matriz[fila][columna] sea un pivote no nulo.
            """
            if self.matriz[fila][columna] == 0:
                for i in range(fila + 1, self.filas):
                    if self.matriz[i][columna] != 0:
                        # Intercambiar filas
                        self.matriz[fila], self.matriz[i] = self.matriz[i], self.matriz[fila]
                        break

        def normaliza_fila(self, fila, columna):
            """
            Normaliza la fila para que el pivote sea 1.
            """
            pivote = self.matriz[fila][columna]
            if pivote != 0:
                for j in range(len(self.matriz[0])):
                    self.matriz[fila][j] /= pivote

        def hacer_ceros_columna(self, fila, columna):
            """
            Hace ceros en la columna del pivote actual para las otras filas.
            """
            for i in range(self.filas):
                if i != fila:
                    factor = self.matriz[i][columna]
                    for j in range(len(self.matriz[0])):
                        self.matriz[i][j] -= factor * self.matriz[fila][j]

        def reducir(self):
            """
            Aplica el método de Gauss-Jordan completo a la matriz.
            """
            fila_actual = 0
            for columna_actual in range(self.columnas):
                # Paso 1: Asegurar que el pivote no sea 0
                self.pivotea(fila_actual, columna_actual)

                # Paso 2: Normalizar la fila para que el pivote sea 1
                if self.matriz[fila_actual][columna_actual] != 0:
                    self.normaliza_fila(fila_actual, columna_actual)

                    # Paso 3: Hacer ceros en las demás filas en la columna del pivote
                    self.hacer_ceros_columna(fila_actual, columna_actual)

                    # Pasar a la siguiente fila
                    fila_actual += 1

                # Si hemos procesado todas las filas, terminamos
                if fila_actual >= self.filas:
                    break

        def obtener_solucion(self):
            """
            Obtiene las soluciones del sistema, manejando las variables libres si es necesario.
            """
            soluciones = [None] * self.columnas
            variables_libres = []

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

        def mostrar_matriz(self):
            """
            Imprime la matriz actual.
            """
            print("\nMatriz escalonada reducida:")
            for fila in self.matriz:
                print([str(elemento) for elemento in fila])

        def mostrar_solucion(self):
            """
            Muestra las soluciones del sistema.
            """
            soluciones, variables_libres = self.obtener_solucion()

            print("\nSoluciones:")
            for i, solucion in enumerate(soluciones):
                if solucion:
                    print(f"x{i + 1} = {solucion}")
                else:
                    print(f"x{i + 1} es libre")


    # Función para pedir al usuario los elementos de la matriz
        def obtener_matriz(self, name, filas, columna):
            """
            Funcion que sirve para ingresar los datos para la matriz y la clase.
            """
            self.nombre = name

            matriz = []
            print("Introduce los elementos de la matriz fila por fila (separados por espacios):")
            for i in range(filas):
                fila_matriz = input(f"Fila {i + 1}: ").split()
                matriz.append([Fraction(x) for x in fila_matriz])
            self.matriz = matriz
            self.filas = len(self.matriz)
            self.columnas = len(self.matriz[0]) - 1  # La última columna es el vector de soluciones

        def imprimir_matrices_para_historial(self):
            """
            Funcion que digita la matriz y la solucion cuando sea seleccionado
            desde el gestor de historial.
            """
            self.mostrar_matriz()
            self.mostrar_solucion()


    return GaussJordan()