"""
Archivo: clase_sistema_ecuaciones.py 3.5.8
Descripcion: archivo que contiene los atributos y metodos de la clase GaussJordan.
contiene CreadorDeEcuaciones() que funciona como constructor de la clase.
"""
from fractions import Fraction


def CreadorDeEcuaciones():
    class GaussJordan:
        def __init__(self):
            """Inicializa una instancia de la clase GaussJordan."""
            self.nombre = ""
            self.matriz = []
            self.matriz_original = []  # Atributo para guardar la matriz original
            self.filas = 0
            self.columnas = 0
            self.pasos = 0
            self.solucion = []  # Soluciones en formato ordenado

        def pivotea(self, fila, columna, mostrar_paso):
            """Realiza el pivoteo en la matriz si el elemento en la posición dada es cero."""
            if self.matriz[fila][columna] == 0:
                for i in range(fila + 1, self.filas):
                    if self.matriz[i][columna] != 0:
                        self.matriz[fila], self.matriz[i] = self.matriz[i], self.matriz[fila]
                        mostrar_paso(f"Paso {self.pasos + 1}:\nIntercambio: (f{fila + 1} <-> f{i + 1})\n")
                        break

        def normaliza_fila(self, fila, columna, mostrar_paso):
            """Normaliza la fila dada dividiendo por el pivote."""
            pivote = self.matriz[fila][columna]
            if pivote != 0:
                for j in range(len(self.matriz[0])):
                    self.matriz[fila][j] /= pivote
                mostrar_paso(f"Paso {self.pasos + 1}:\nNormalización: (f{fila + 1} -> f{fila + 1} / {str(Fraction(pivote))})\n")

        def hacer_ceros_columna(self, fila, columna, mostrar_paso):
            """Elimina los valores no nulos en una columna, haciendo ceros por debajo y por encima del pivote."""
            for i in range(self.filas):
                if i != fila:
                    factor = self.matriz[i][columna]
                    if factor != 0:
                        for j in range(len(self.matriz[0])):
                            self.matriz[i][j] -= factor * self.matriz[fila][j]
                        mostrar_paso(f"Paso {self.pasos + 1}:\nEliminación: (f{i + 1} -> f{i + 1} - {str(Fraction(factor))} * f{fila + 1})\n")

        def reducir(self, mostrar_paso):
            """Reduce la matriz a su forma escalonada utilizando el método de Gauss-Jordan."""
            fila_actual = 0
            for columna_actual in range(self.columnas):
                self.pivotea(fila_actual, columna_actual, mostrar_paso)
                mostrar_paso(self.formato_matriz())
                if (all(self.matriz[fila_actual][j] == 0 for j in range(self.columnas))
                        and self.matriz[fila_actual][-1] != 0):
                    return "inconsistente"

                if self.matriz[fila_actual][columna_actual] != 0:
                    self.normaliza_fila(fila_actual, columna_actual, mostrar_paso)
                    self.hacer_ceros_columna(fila_actual, columna_actual, mostrar_paso)
                    fila_actual += 1

                if fila_actual >= self.filas:
                    break

            if fila_actual < self.columnas:
                return "infinitas"
            return "unica"

        def formato_matriz(self):
            """Devuelve la matriz en formato de texto legible."""
            return "\n".join([" ".join([str(Fraction(x)) for x in fila]) for fila in self.matriz]) + "\n"

        def mostrar_solucion(self, mostrar_paso):
            """Determina el tipo de solución y muestra la solución correspondiente."""
            resultado = self.reducir(mostrar_paso)
            if resultado == "inconsistente":
                mostrar_paso("El sistema es inconsistente y no tiene solución.\n")
            elif resultado == "infinitas":
                self.mostrar_variables_libres(mostrar_paso)
            elif resultado == "unica":
                self.mostrar_variables(mostrar_paso)

        def mostrar_variables(self, mostrar_paso):
            """Muestra la solución única del sistema."""
            variables = ["x" + str(i + 1) for i in range(self.columnas)]
            soluciones = [fila[-1] for fila in self.matriz]
            self.solucion = []  # Limpiamos el arreglo de soluciones
            mostrar_paso("Solución única:\n")
            for i, sol in enumerate(soluciones):
                self.solucion.append((variables[i], sol))  # Guardamos la solución en el formato correcto
                mostrar_paso(f"{str(Fraction(sol))}\n")  # Sin el prefijo "x="

        def mostrar_variables_libres(self, mostrar_paso):
            """Muestra las soluciones cuando hay variables libres, en orden de x1, x2, ..., sin separación."""
            variables = ["x" + str(i + 1) for i in range(self.columnas)]
            soluciones = [None] * self.columnas  # Creamos una lista de None para las soluciones

            for j in range(self.filas):
                pivote = -1
                for i in range(self.columnas):
                    if self.matriz[j][i] != 0:
                        pivote = i
                        break
                if pivote == -1:
                    continue

                dependencia = f"{str(Fraction(self.matriz[j][-1]))}"
                for k in range(pivote + 1, self.columnas):
                    coeficiente = Fraction(-self.matriz[j][k])
                    if coeficiente != 0:
                        if coeficiente == 1:
                            dependencia += f" + {variables[k]}"
                        elif coeficiente == -1:
                            dependencia += f" - {variables[k]}"
                        else:
                            signo = " + " if coeficiente > 0 else " - "
                            dependencia += f"{signo}{abs(coeficiente)} * {variables[k]}"

                soluciones[pivote] = dependencia

            # Las variables libres se quedan como "libre"
            for i, solucion in enumerate(soluciones):
                if solucion is None:
                    soluciones[i] = "libre"

            # Mostrar las soluciones
            self.solucion = []  # Limpiamos el arreglo de soluciones
            mostrar_paso("Soluciones:\n")
            for i, sol in enumerate(soluciones):
                self.solucion.append((variables[i], sol))  # Guardamos la solución en el formato correcto
                mostrar_paso(f"{variables[i]} = {sol}\n")  # Mostrar cada variable con su solución o "libre"

    return GaussJordan()

