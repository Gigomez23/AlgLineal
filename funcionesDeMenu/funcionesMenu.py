import os
from funciones import *


def matriz_aleatoria():
    """
        Funcion que crea una matriz de forma aleatoria.
        Calcula la matriz identidad.
        Imprime la matriz identidad.
    """
    dimension = int(input("Ingrese el tamaño de la matriz cuadrada: "))
    matriz = crear_matriz_aleatoria(dimension)

    print("Matriz Inicial:")
    imprimir_matriz(matriz)

    if escalonar_matriz(matriz, dimension):
        print("La matriz ha sido transformada a una matriz identidad:")
        identidad = matriz_identidad(dimension)
        imprimir_matriz(identidad)
    else:
        print("No se pudo resolver la matriz ya que es inconsistente.")

    os.system("pause")


def matriz_manul():
    """
            Funcion que crea una matriz pidiendo al usuario los valores
            Calcula la matriz identidad.
            Imprime la matriz identidad.
        """
    dimension = int(input("Ingrese el tamaño de la matriz cuadrada: "))
    matriz = ingresar_matriz_usuario(dimension)

    print("Matriz Inicial:")
    imprimir_matriz(matriz)

    if escalonar_matriz(matriz, dimension):
        print("La matriz ha sido transformada a una matriz identidad:")
        identidad = matriz_identidad(dimension)
        imprimir_matriz(identidad)
    else:
        print("No se pudo resolver la matriz ya que es inconsistente.")

    os.system("pause")
