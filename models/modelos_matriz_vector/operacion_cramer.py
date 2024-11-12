# Archivo: operacion_cramer.py
from models.modelos_matriz_vector.operaciones_determinante import CreadorDeOperacionDeterminantes


def CreadorDeCramer():
    class OperacionCramer:
        def __init__(self):
            # Crear una instancia de OperacionesDeterminante
            self.operacion_determinante = CreadorDeOperacionDeterminantes()
            self.matriz_coeficientes = []
            self.vector_independiente = []
            self.matriz_original = []
            self.solucion = []
            self.determinante = []

        def ingresar_datos_cramer(self, matriz_aumentada):
            """
            Recibe una matriz aumentada y la separa en la matriz de coeficientes y el vector de términos independientes.
            """
            # Verifica que la matriz aumentada tenga al menos una columna para el vector independiente
            if len(matriz_aumentada) == 0 or len(matriz_aumentada[0]) < 2:
                raise ValueError("La matriz aumentada debe tener al menos dos columnas.")

            self.matriz_original = matriz_aumentada
            print(self.matriz_original)
            # Separar la matriz aumentada en matriz de coeficientes y vector independiente
            self.matriz_coeficientes = [fila[:-1] for fila in matriz_aumentada]
            self.vector_independiente = [fila[-1] for fila in matriz_aumentada]

            # Verificar que la matriz de coeficientes sea cuadrada
            if len(self.matriz_coeficientes) != len(self.matriz_coeficientes[0]):
                raise ValueError("La matriz de coeficientes debe ser cuadrada.")

            # Utilizar el metodo de OperacionesDeterminante para ingresar los datos
            self.operacion_determinante.ingresar_datos(self.matriz_coeficientes)

        def resolver_cramer(self):
            """Se aplica la regla de Cramer para resolver el sistema de ecuaciones."""
            det_principal = self.operacion_determinante.calcular_determinante()
            self.determinante = [['Det de A:'], [det_principal]]
            if det_principal == 0:
                self.solucion = [['Determinante del coeficiente es 0, no tiene solución']]
                raise ValueError("El sistema no se puede resolver por Cramer "
                                 "porque el determinante del coeficiente es 0.")

            n = len(self.matriz_coeficientes)
            soluciones = []
            procedimiento = []  # Para almacenar los pasos detallados

            procedimiento.append(f"Determinante principal:\n det A = {det_principal}")

            for i in range(n):
                matriz_modificada = self._crear_matriz_modificada(i)
                matriz_modificada_str = self._formatear_matriz_como_matriz(matriz_modificada)
                procedimiento.append(f"\nMatriz modificada al reemplazar la columna {i + 1}:\n{matriz_modificada_str}")

                self.operacion_determinante.ingresar_datos(matriz_modificada)
                det_modificado = self.operacion_determinante.calcular_determinante()
                solucion = det_modificado / det_principal
                soluciones.append(solucion)

                procedimiento.append(f"Determinante de la matriz modificada: det A_{i + 1} = {det_modificado}")
                procedimiento.append(
                    f"Solución para x{i + 1}: x{i + 1} = {det_modificado}/{det_principal} = {solucion}\n")

            procedimiento.append("\nSoluciones finales:")
            for i, solucion in enumerate(soluciones):
                procedimiento.append(f"x{i + 1} = {solucion}")


            self.solucion = soluciones
            return soluciones, procedimiento  # Devuelve las soluciones y el procedimiento

        def _formatear_matriz_como_matriz(self, matriz):
            """Formatea una matriz para que se muestre como una matriz tradicional usando fracciones."""
            filas = ["|" + " ".join([f"{str(x):>4}" for x in fila]) + "|" for fila in matriz]
            return "\n".join(filas)

        def _crear_matriz_modificada(self, columna_reemplazar):
            """Crea una nueva matriz reemplazando la columna indicada con el vector de términos independientes."""
            matriz_modificada = [fila[:] for fila in self.matriz_coeficientes]  # Copia la matriz original
            for fila in range(len(matriz_modificada)):
                matriz_modificada[fila][columna_reemplazar] = self.vector_independiente[fila]
            return matriz_modificada

    return OperacionCramer()