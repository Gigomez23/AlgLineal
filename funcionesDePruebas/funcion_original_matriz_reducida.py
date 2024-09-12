"""
Archivo: funcionesMenu.py 1.0.0
Descripcion: archivo con funciones para el menu
"""
from fractions import Fraction


# def mostrar_matriz(matrix, paso):
#     print(f"\nPaso {paso}:")
#     for fila in matrix:
#         print([str(elemento) for elemento in fila])


def gauss_jordan_elimination(matrix):
    filas = len(matrix)
    columnas = len(matrix[0]) - 1  # La última columna es el vector de soluciones
    paso = 1  # Contador de pasos

    # Paso 1: Aplicamos el proceso de eliminación Gaussiana
    for i in range(min(filas, columnas)):
        # Seleccionamos el pivote, intercambiando filas si el pivote es cero
        if matrix[i][i] == 0:
            for j in range(i + 1, filas):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    mostrar_matriz(matrix, paso)
                    paso += 1
                    break

        # Normalizamos la fila del pivote
        pivote = matrix[i][i]
        if pivote != 0:
            for j in range(columnas + 1):
                matrix[i][j] /= pivote
            mostrar_matriz(matrix, paso)
            paso += 1

        # Eliminamos los otros elementos en la columna del pivote
        for j in range(filas):
            if j != i:
                factor = matrix[j][i]
                for k in range(columnas + 1):
                    matrix[j][k] -= factor * matrix[i][k]
                mostrar_matriz(matrix, paso)
                paso += 1

    return matrix


def resolver_sistema(matrix):
    filas = len(matrix)
    columnas = len(matrix[0]) - 1
    soluciones = [None] * columnas
    variables_libres = []

    for i in range(filas):
        # Determinamos si una fila es inconsistente
        if all(matrix[i][j] == 0 for j in range(columnas)) and matrix[i][-1] != 0:
            return "El sistema no tiene solución"

    # Determinar las variables libres y las dependientes
    for i in range(filas):
        pivote_encontrado = False
        for j in range(columnas):
            if matrix[i][j] == 1:
                pivote_encontrado = True
                soluciones[j] = matrix[i][-1]
                for k in range(j + 1, columnas):
                    if matrix[i][k] != 0:
                        soluciones[j] = f"{matrix[i][-1]} - {matrix[i][k]}x{k + 1}"
                break
        if not pivote_encontrado:
            variables_libres.append(f"x{i + 1}")

    return soluciones, variables_libres


# Función para pedir al usuario los elementos de la matriz
def obtener_matriz():
    filas = int(input("Introduce el número de filas de la matriz: "))
    columnas_totales = int(
        input("Introduce el número de columnas de la matriz aumentada (incluyendo el vector solución): "))

    matriz = []
    print("Introduce los elementos de la matriz fila por fila (separados por espacios):")
    for i in range(filas):
        fila_matriz = input(f"Fila {i + 1}: ").split()
        matriz.append([Fraction(x) for x in fila_matriz])

    return matriz