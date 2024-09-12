"""
Archivo: historial 1.5.0
Descripcion: archivo que gestiona la creacion de los objetos matriz.
Los agrega a la lista que sirve de historial.
"""
from models.clase_matriz import *
from models.clase_sistema_ecuaciones import *
from models.clase_matriz_operaciones import *

historial_de_matrices = []


def agregar_matriz_aleatoria(dimension, nombre):
    """
    Funcion del menu para agregar una matriz de forma aleatoria.

    Args:
        dimension (int): dimension para la matriz a crear
        nombre (str): cadena que representa el nombre de la matriz a agregar
    """
    historial_de_matrices.append(CreadorDeMatriz())
    historial_de_matrices[-1].crear_matriz_aleatoria(dimension, nombre)
    historial_de_matrices[-1].resolver_matriz(imprimir_solucion=True)


def agregar_matriz_manual(dimension, nombre):
    """
    Funcion del menu para agregar una matriz de forma manual.

    Args:
        dimension (int): dimension para la matriz a crear
        nombre (str): cadena que representa el nombre de la matriz a agregar
    """
    historial_de_matrices.append(CreadorDeMatriz())
    historial_de_matrices[-1].ingresar_matriz_usuario(dimension, nombre)
    historial_de_matrices[-1].resolver_matriz(imprimir_solucion=True)

def resolver_sistema_de_ecuaciones(nombre, fila, columna):
    """
    Funcion del menu para resolver un sistema de ecuaciones.
    """
    historial_de_matrices.append(CreadorDeEcuaciones())
    historial_de_matrices[-1].obtener_matriz(nombre, fila, columna)
    historial_de_matrices[-1].reducir()
    historial_de_matrices[-1].mostrar_matriz()
    historial_de_matrices[-1].mostrar_solucion()

def resolver_operaciones_de_matriz():
    """Funcion del menu para inicializar una matriz en base a la operación deseada"""
    historial_de_matrices.append(CreadorDeOperaciones())
    historial_de_matrices[-1].ingresar_datos()
    historial_de_matrices[-1].imprimir_matrices_y_solucion()

def mostrar_matrices_y_seleccionar():
    """
    Muestra los nombres de todas las matrices disponibles y permite al usuario seleccionar una.
    """
    if not historial_de_matrices:
        print("No hay matrices disponibles.")
        return

    # Mostrar todos los nombres de las matrices
    print("Matrices disponibles:")
    for i, matriz in enumerate(historial_de_matrices, start=1):
        print(f"{i}. {matriz.nombre}")

    # Pedir al usuario que elija una matriz por número
    try:
        seleccion = int(input("Seleccione el número de la matriz que desea imprimir: "))
        if 1 <= seleccion <= len(historial_de_matrices):
            matriz_seleccionada = historial_de_matrices[seleccion - 1]
            print(f"\nMatriz seleccionada: {matriz_seleccionada.nombre}")

            # Imprimir la matriz principal
            matriz_seleccionada.imprimir_matrices_para_historial()
        else:
            print("Selección inválida. Intente de nuevo.")
    except ValueError:
        print("Por favor, ingrese un número válido.")
