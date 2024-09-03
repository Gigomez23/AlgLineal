"""
Archivo: funcionesMenu.py 1.5.0
Descripcion: archivo con funciones para el menu
"""
import os
from historial import *


def matriz_aleatoria():
    """
    Funcion que pide al usuario digitar dimension y titulo de matriz.
    Crea una matriz aleatoria y la agrega a la lista de historial.
    """
    try:
        dimension = int(input("Ingrese el tamaño de la matriz cuadrada: "))
        titulo_matriz = input("Ingrese el nombre de la matriz: ")
        agregar_matriz_aleatoria(dimension, titulo_matriz)
    except ValueError:
        print("Por favor digite un valor numerico como dimensión. ")

    os.system("pause")


def matriz_manul():
    """
    Funcion que pide al usuario digitar dimension y titulo de matriz.
    Crea una matriz de forma manual y la agrega a la lista de historial.
    """
    try:
        dimension = int(input("Ingrese el tamaño de la matriz cuadrada: "))
        titulo_matriz = input("Ingrese el nombre de la matriz: ")
        agregar_matriz_manual(dimension, titulo_matriz)
    except ValueError:
        print("Por favor digite un valor numerico como dimension. ")

    os.system("pause")


def imprimir_historial():
    """
    Funcion de menu que ejecuta la seleccion de matrices del historial.
    """
    mostrar_matrices_y_seleccionar()
