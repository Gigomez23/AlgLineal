"""
Archivo: clase_sistema_ecuaciones.py 2.2.3
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
            pasos (int): dato que representa los pasos tomados para resolver.
        """
        def __init__(self):
            self.nombre = ""
            self.matriz = []
            self.pasos = 0

        def pivotea(self, fila, columna):
            """
            Asegura que el elemento en matriz[fila][columna] sea un pivote no nulo.
            """
            if self.matriz[fila][columna] == 0:
                for i in range(fila + 1, self.filas):
                    if self.matriz[i][columna] != 0:
                        # Intercambiar filas
                        self.matriz[fila], self.matriz[i] = self.matriz[i], self.matriz[fila]
                        print(f"F{fila + 1} <--> F{i + 1} (Intercambio de filas)")
                        self.mostrar_matriz_en_proceso()
                        break

        def normaliza_fila(self, fila, columna):
            """
            Normaliza la fila para que el pivote sea 1.
            """
            pivote = self.matriz[fila][columna]
            if pivote != 0:
                for j in range(len(self.matriz[0])):
                    self.matriz[fila][j] /= pivote
                # Mostrar el paso realizado
                print(f"F{fila + 1} --> (1/{Fraction(pivote).limit_denominator()}) * F{fila + 1}")
                self.mostrar_matriz_en_proceso()

        def hacer_ceros_columna(self, fila, columna):
            """
            Hace ceros en la columna del pivote actual para las otras filas.
            """
            for i in range(self.filas):
                if i != fila:
                    factor = self.matriz[i][columna]
                    for j in range(len(self.matriz[0])):
                        self.matriz[i][j] -= factor * self.matriz[fila][j]
                    # Mostrar el paso realizado
                    print(f"F{i + 1} --> F{i + 1} - ({Fraction(factor).limit_denominator()}) * F{fila + 1}")
                    self.mostrar_matriz_en_proceso()

        def reducir(self):
            """
            Aplica el método de Gauss-Jordan completo a la matriz, mostrando cada paso.
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
                        solucion = self.matriz[i][-1]

                        # Si la constante es 0, la omitimos en la solución
                        if solucion != 0:
                            expresion = f"{solucion}"
                        else:
                            expresion = ""

                        for k in range(j + 1, self.columnas):
                            coeficiente = self.matriz[i][k]
                            if coeficiente != 0:
                                signo = '+' if coeficiente < 0 else '-'
                                coeficiente = abs(coeficiente)
                                expresion += f" {signo} {coeficiente}x{k + 1}"
                        soluciones[j] = expresion.strip()
                        break
                if not pivote_encontrado:
                    variables_libres.append(f"x{j + 1}")

            return soluciones, variables_libres

        def mostrar_matriz(self):
            """Imprime la matriz actual."""
            print(f"\nPaso {self.pasos}:")
            for fila in self.matriz:
                print([str(Fraction(elemento)) for elemento in fila])
            self.pasos += 1

        def mostrar_matriz_en_proceso(self):
            pasos_local = self.pasos
            print(f"\nPaso {pasos_local}:")
            for fila in self.matriz:
                print([str(Fraction(elemento)) for elemento in fila])
            self.pasos += 1

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

            if variables_libres:
                print(f"\nVariables libres: {', '.join(variables_libres)}")

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