# Archivo: operacion_cramer.py
from models.operaciones_determinante import CreadorDeOperacionDeterminantes
from fractions import Fraction


def CreadorDeCramer():
    class OperacionCramer:
        def _init_(self):
            # Crear una instancia de OperacionesDeterminante
            self.operacion_determinante = CreadorDeOperacionDeterminantes()()
            self.matriz_coeficientes = []
            self.vector_independiente = []

        def ingresar_datos_cramer(self, matriz_coeficientes, vector_independiente):
            """Recibe una matriz de coeficientes y un vector de términos independientes."""
            if len(matriz_coeficientes) != len(matriz_coeficientes[0]):
                raise ValueError("La matriz de coeficientes debe ser cuadrada.")
            if len(matriz_coeficientes) != len(vector_independiente):
                raise ValueError("El vector de términos independientes debe tener la misma longitud que la matriz.")

            self.matriz_coeficientes = matriz_coeficientes
            self.vector_independiente = vector_independiente
            # Utilizar el metodo de OperacionesDeterminante para ingresar los datos
            self.operacion_determinante.ingresar_datos(matriz_coeficientes)

        def resolver_cramer(self):
            """Se aplica la regla de Cramer para resolver el sistema de ecuaciones."""
            # Reutilizar el metodo de calcular determinante desde la instancia de OperacionesDeterminante
            det_principal = self.operacion_determinante.calcular_determinante()
            if det_principal == 0:
                raise ValueError("El sistema no tiene solución única porque el determinante es 0.")

            n = len(self.matriz_coeficientes)
            soluciones = []

            print(f"Determinante principal: {det_principal}")

            for i in range(n):
                matriz_modificada = self._crear_matriz_modificada(i)
                print(f"\nMatriz modificada al reemplazar la columna {i + 1}:\n")
                for fila in matriz_modificada:
                    print(fila)

                self.operacion_determinante.ingresar_datos(matriz_modificada)
                det_modificado = self.operacion_determinante.calcular_determinante()
                solucion = det_modificado / det_principal
                soluciones.append(solucion)

                print(f"Determinante modificado: {det_modificado}")
                print(f"Solución para x{i + 1}: {solucion}\n")

                print("Soluciones del sistema:")
                for i, solucion in enumerate(soluciones):
                    print(f"x{i + 1} = {solucion}")

            return soluciones

        def _crear_matriz_modificada(self, columna_reemplazar):
            """Crea una nueva matriz reemplazando la columna indicada con el vector de términos independientes."""
            matriz_modificada = [fila[:] for fila in self.matriz_coeficientes]  # Copia la matriz original
            for fila in range(len(matriz_modificada)):
                matriz_modificada[fila][columna_reemplazar] = self.vector_independiente[fila]
            return matriz_modificada

    return OperacionCramer