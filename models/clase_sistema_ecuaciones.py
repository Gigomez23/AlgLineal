"""
Archivo: clase_sistema_ecuaciones.py 3.0.8
Descripcion: archivo que contiene los atributos y metodos de la clase GaussJordan.
contiene CreadorDeEcuaciones() que funciona como constructor de la clase.
"""
from fractions import Fraction

def CreadorDeEcuaciones():
    class GaussJordan:
        def __init__(self):
            self.nombre = ""
            self.matriz = []
            self.filas = 0
            self.columnas = 0
            self.pasos = 0

        def pivotea(self, fila, columna, mostrar_paso):
            if self.matriz[fila][columna] == 0:
                for i in range(fila + 1, self.filas):
                    if self.matriz[i][columna] != 0:
                        self.matriz[fila], self.matriz[i] = self.matriz[i], self.matriz[fila]
                        mostrar_paso(f"(f{fila + 1} <-> f{i + 1})")
                        break

        def normaliza_fila(self, fila, columna, mostrar_paso):
            pivote = self.matriz[fila][columna]
            if pivote != 0:
                for j in range(len(self.matriz[0])):
                    self.matriz[fila][j] /= pivote
                mostrar_paso(f"(f{fila + 1} -> f{fila + 1} / {str(Fraction(pivote))})")

        def hacer_ceros_columna(self, fila, columna, mostrar_paso):
            for i in range(self.filas):
                if i != fila:
                    factor = self.matriz[i][columna]
                    if factor != 0:
                        for j in range(len(self.matriz[0])):
                            self.matriz[i][j] -= factor * self.matriz[fila][j]
                        mostrar_paso(f"(f{i + 1} -> f{i + 1} - {str(Fraction(factor))} * f{fila + 1})")

        def reducir(self, mostrar_paso):
            fila_actual = 0
            for columna_actual in range(self.columnas):
                self.pivotea(fila_actual, columna_actual, mostrar_paso)

                mostrar_paso(f"Matriz después de verificar pivote en la columna {columna_actual + 1}:\n")
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

                mostrar_paso(f"Matriz después de modificar la columna {columna_actual + 1}:\n")
                mostrar_paso(self.formato_matriz())
                self.pasos += 1

            if fila_actual < self.columnas:
                return "infinitas"
            return "unica"

        def formato_matriz(self):
            return "\n".join([" ".join([str(Fraction(x)) for x in fila]) for fila in self.matriz]) + "\n"

        def mostrar_solucion(self, mostrar_paso):
            """
            Determina el tipo de solución y muestra la solución correspondiente.
            """
            resultado = self.reducir(mostrar_paso)

            if resultado == "inconsistente":
                mostrar_paso("El sistema es inconsistente y no tiene solución.\n")
            elif resultado == "infinitas":
                self.mostrar_variables_libres(mostrar_paso)
            elif resultado == "unica":
                self.mostrar_variables(mostrar_paso)

        def mostrar_variables(self, mostrar_paso):
            """
            Muestra la solución única del sistema.
            """
            variables = ["x" + str(i + 1) for i in range(self.columnas)]
            soluciones = [fila[-1] for fila in self.matriz]
            mostrar_paso("Solución única:\n")
            for i, sol in enumerate(soluciones):
                mostrar_paso(f"{variables[i]} = {str(Fraction(sol))}\n")

        def mostrar_variables_libres(self, mostrar_paso):
            """
            Muestra las soluciones cuando hay variables libres en el sistema,
            incluyendo la expresión de las variables dependientes.
            """
            variables = ["x" + str(i + 1) for i in range(self.columnas)]
            libres = []
            dependientes = {}

            for j in range(self.filas):
                pivote = -1
                for i in range(self.columnas):
                    if self.matriz[j][i] != 0:
                        pivote = i
                        break
                if pivote == -1:
                    continue  # Esta fila no tiene pivote, así que no afecta las soluciones
                dependencia = f"{variables[pivote]} = {str(Fraction(self.matriz[j][-1]))}"
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
                dependientes[variables[pivote]] = dependencia

            # Identificar las variables libres (aquellas que no tienen pivote)
            todos_pivotes = set(dependientes.keys())
            libres = [var for var in variables if var not in todos_pivotes]

            mostrar_paso("Soluciones:\n")
            # Mostrar las soluciones de las variables dependientes
            for var in sorted(dependientes.keys(), key=lambda v: int(v[1:])):
                mostrar_paso(f"{dependientes[var]}\n")
            # Mostrar las variables libres
            for var in sorted(libres, key=lambda v: int(v[1:])):
                mostrar_paso(f"{var} es libre\n")

    return GaussJordan()

