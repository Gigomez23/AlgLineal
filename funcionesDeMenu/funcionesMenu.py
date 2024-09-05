"""
Archivo: funcionesMenu.py 1.5.0
Descripcion: archivo con funciones para el menu
"""
import os
from consolemenu import clear_terminal
from historial import *


def matriz_aleatoria():
    """
    Funcion que pide al usuario digitar dimension y titulo de matriz.
    Crea una matriz aleatoria y la agrega a la lista de historial.
    """
    clear_terminal()
    try:
        dimension = int(input("Ingrese el tamaño de la matriz cuadrada: "))
        titulo_matriz = input("Ingrese el nombre de la matriz: ")
        agregar_matriz_aleatoria(dimension, titulo_matriz)
    except ValueError:
        print("Por favor digite un valor numerico como dimensión. ")

    os.system("pause")
    os.system('cls' if os.name == 'nt' else 'clear')


def matriz_manul():
    """
    Funcion que pide al usuario digitar dimension y titulo de matriz.
    Crea una matriz de forma manual y la agrega a la lista de historial.
    """
    clear_terminal()
    try:
        dimension = int(input("Ingrese el tamaño de la matriz cuadrada: "))
        titulo_matriz = input("Ingrese el nombre de la matriz: ")
        agregar_matriz_manual(dimension, titulo_matriz)
    except ValueError:
        print("Por favor digite un valor numerico como dimension. ")

    os.system("pause")
    os.system('cls' if os.name == 'nt' else 'clear')


def imprimir_historial():
    """
    Funcion de menu que ejecuta la seleccion de matrices del historial.
    """
    clear_terminal()
    mostrar_matrices_y_seleccionar()

