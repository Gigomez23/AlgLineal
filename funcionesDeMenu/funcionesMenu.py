"""
Archivo: funcionesMenu.py 1.7.0
Descripcion: archivo con funciones para el menu
todo: pass todo a metodo dentro de la clase
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
        titulo_matriz = input("Ingrese el nombre de la matriz: ")
        dimension = int(input("Ingrese el tamaño de la matriz cuadrada: "))
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
        titulo_matriz = input("Ingrese el nombre de la matriz: ")
        dimension = int(input("Ingrese el tamaño de la matriz cuadrada: "))
        agregar_matriz_manual(dimension, titulo_matriz)
    except ValueError:
        print("Por favor digite un valor numerico como dimension. ")

    os.system("pause")
    os.system('cls' if os.name == 'nt' else 'clear')

def matriz_reducida():
    """
    Funcion que pide al usuario digitar una matriz reducidad y resolver.
    :return:
    """
    try:
        nombre = input("Ingrese el nombre de la matriz: ")
        fila = int(input("Ingrese el numero de filas de la matriz: "))
        columnas = int(input("Ingrese el numero de columnas de la matriz aumentada (incluyendo el vector solucion): "))
        resolver_sistema_de_ecuaciones(nombre, fila, columnas)
    except ValueError:
        print("Por favor digite un valor numerico como dimension. ")

    os.system("pause")

def matriz_operacion():
    resolver_operaciones_de_matriz()
    os.system("pause")

def imprimir_historial():
    """
    Funcion de menu que ejecuta la seleccion de matrices del historial.
    """
    clear_terminal()
    mostrar_matrices_y_seleccionar()

