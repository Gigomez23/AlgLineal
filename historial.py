"""
Archivo: historial 1.3
Descripcion: archivo que gestiona la creacion de los objetos matriz.
Los agrega a la lista que sirve de historial.
"""
from clase_matriz import *
from funciones import *

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

def resolver_sistema_de_ecuaciones():
    """
    Funcion del menu para resolver un sistema de ecuaciones.
    """
    #funcion es un prototipo
    # historial_de_matrices.append(CreadorDeEcuaciones())
    # historial_de_matrices[-1].obtener_matriz()
    # historial_de_matrices[-1].jauss_jordan_elimination()
    # historial_de_matrices[-1].imprimir_resultado_final()
    # Ejemplo de uso
    matriz_aumentada = obtener_matriz()

    # Resolvemos el sistema con el método de Gauss-Jordan
    matriz_reducida = gauss_jordan_elimination(matriz_aumentada)

    # Imprimimos la matriz escalonada reducida
    print("\nMatriz escalonada reducida:")
    for fila in matriz_reducida:
        print([str(elemento) for elemento in fila])

    # Obtenemos la solución
    soluciones, variables_libres = resolver_sistema(matriz_reducida)

    # Imprimimos la solución
    if isinstance(soluciones, str):
        print("\nSolución:")
        print(soluciones)
    else:
        print("\nSoluciones:")
        for i, solucion in enumerate(soluciones):
            if solucion:
                print(f"x{i + 1} = {solucion}")
            else:
                print(f"x{i + 1} es libre")


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
