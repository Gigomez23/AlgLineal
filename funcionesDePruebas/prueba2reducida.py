from fractions import Fraction

class Gauss:
    def __init__(self, matrix):
        self.matrix = matrix
        self.filas = len(matrix)
        self.columnas = len(matrix[0]) - 1  # La última columna es el vector de soluciones
        self.pasos = 0  # Contador para mostrar pasos

    def mostrar_matriz(self):
        """Imprime la matriz actual."""
        print(f"\nPaso {self.pasos}:")
        for fila in self.matrix:
            print([str(Fraction(elemento)) for elemento in fila])
        self.pasos += 1


    def pivotea(self, fila, columna):
        """Asegura que el elemento en matrix[fila][columna] sea un pivote no nulo."""
        if self.matrix[fila][columna] == 0:
            for i in range(fila + 1, self.filas):
                if self.matrix[i][columna] != 0:
                    # Intercambiar filas
                    self.matrix[fila], self.matrix[i] = self.matrix[i], self.matrix[fila]
                    break

    def normaliza_fila(self, fila, columna):
        """Normaliza la fila para que el pivote sea 1."""
        pivote = self.matrix[fila][columna]
        if pivote != 0:
            for j in range(len(self.matrix[0])):
                self.matrix[fila][j] /= pivote

    def hacer_ceros_columna(self, fila, columna):
        """Hace ceros en la columna del pivote actual para las otras filas."""
        for i in range(self.filas):
            if i != fila:
                factor = self.matrix[i][columna]
                for j in range(len(self.matrix[0])):
                    self.matrix[i][j] -= factor * self.matrix[fila][j]

    def reducir(self):
        """Aplica el método de Gauss-Jordan completo a la matriz, mostrando cada paso."""
        fila_actual = 0
        for columna_actual in range(self.columnas):
            # Paso 1: Asegurar que el pivote no sea 0
            self.pivotea(fila_actual, columna_actual)

            # Mostrar el estado de la matriz tras pivoteo
            self.mostrar_matriz()

            # Paso 2: Normalizar la fila para que el pivote sea 1
            if self.matrix[fila_actual][columna_actual] != 0:
                self.normaliza_fila(fila_actual, columna_actual)
                # Mostrar el estado de la matriz tras normalización
                self.mostrar_matriz()

                # Paso 3: Hacer ceros en las demás filas en la columna del pivote
                self.hacer_ceros_columna(fila_actual, columna_actual)
                # Mostrar el estado de la matriz tras hacer ceros
                self.mostrar_matriz()

                # Pasar a la siguiente fila
                fila_actual += 1

            # Si hemos procesado todas las filas, terminamos
            if fila_actual >= self.filas:
                break

    def obtener_solucion(self):
        """Obtiene las soluciones del sistema, manejando las variables libres si es necesario."""
        soluciones = [None] * self.columnas
        variables_libres = []

        for i in range(self.filas):
            pivote_encontrado = False
            for j in range(self.columnas):
                if self.matrix[i][j] == 1:
                    pivote_encontrado = True
                    solucion = self.matrix[i][-1]

                    # Si la constante es 0, la omitimos en la solución
                    if solucion != 0:
                        expresion = f"{solucion}"
                    else:
                        expresion = ""

                    for k in range(j + 1, self.columnas):
                        coeficiente = self.matrix[i][k]
                        if coeficiente != 0:
                            signo = '+' if coeficiente < 0 else '-'
                            coeficiente = abs(coeficiente)
                            expresion += f" {signo} {coeficiente}x{k + 1}"
                    soluciones[j] = expresion.strip()
                    break
            if not pivote_encontrado:
                variables_libres.append(f"x{j + 1}")

        return soluciones, variables_libres

    def mostrar_solucion(self):
        """Muestra las soluciones del sistema."""
        soluciones, variables_libres = self.obtener_solucion()

        print("\nSoluciones:")
        for i, solucion in enumerate(soluciones):
            if solucion:
                print(f"x{i + 1} = {solucion}")
            else:
                print(f"x{i + 1} es libre")

        if variables_libres:
            print(f"\nVariables libres: {', '.join(variables_libres)}")

# Función para pedir al usuario los elementos de la matriz
def obtener_matriz():
    filas = int(input("Introduce el número de filas de la matriz: "))
    columnas_totales = int(input("Introduce el número de columnas de la matriz aumentada (incluyendo el vector solución): "))

    matriz = []
    print("Introduce los elementos de la matriz fila por fila (separados por espacios):")
    for i in range(filas):
        fila_matriz = input(f"Fila {i + 1}: ").split()
        matriz.append([Fraction(x) for x in fila_matriz])

    return matriz

# Ejemplo de uso
matriz_aumentada = obtener_matriz()

# Crear una instancia de la clase GaussJordan
sistema = Gauss(matriz_aumentada)

# Aplicar el método de Gauss-Jordan, mostrando pasos intermedios
sistema.reducir()

# Mostrar las soluciones del sistema
sistema.mostrar_solucion()