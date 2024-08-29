from fractions import Fraction


def crear_matriz_aleatoria(dimension):
    """
    Funcion para crear una matriz con valores aleatorias

    Args:
        dimension (int): dimension de la matriz

    Returns: una matriz con la dimension especificada y numeros aleatorios
    """
    import random
    matriz = [[random.randint(1, 10) for _ in range(dimension)] for _ in range(dimension)]
    return matriz


def ingresar_matriz_usuario(dimension):
    """
     Funcion para crear una matriz con valores digitados por el usuario

     Args:
         dimension (int): dimension de la matriz

     Returns: una matriz con la dimension especificada y los numeros ingresados por el usuario
     """
    print("Por favor, ingrese los elementos de la matriz fila por fila.")
    matriz = []
    for i in range(dimension):
        fila = list(map(int, input(
            f"Ingrese los elementos de la fila {i + 1} separados por espacio (solo números positivos): ").split()))
        if len(fila) != dimension:
            print(f"Error: La fila debe tener {dimension}  de lo contrario es inconsistente.")
            return None
        matriz.append(fila)
    return matriz


def imprimir_matriz(matriz):
    """
     Funcion para imprimir una matriz.

     Args:
         matriz (int): lista con los datos de la matriz.
     """
    # Definir un ancho fijo para los elementos (ajustable según lo necesites)
    ancho = 10

    for fila in matriz:
        # Formatear cada elemento para que tenga el mismo ancho y esté centrado
        print(" ".join(f"{str(Fraction(elem).limit_denominator()):^{ancho}}" if isinstance(elem,
                                                                                           float) else f"{str(elem):^{ancho}}"
                       for elem in fila))
    print()


def escalonar_matriz(matriz, dimension):
    """
     Funcion para escalonar la matriz.

     Args:
         matriz (list): lista que contiene los datos de la matriz.
         dimension (int): dimension de la matriz.

     Returns: un valor verdadero si es posible resolver de lo contrario es falso.
     """
    # Algoritmo de eliminación gaussiana
    for i in range(dimension):
        # Hacer que el pivote sea 1 (dividiendo toda la fila por el valor del pivote)
        pivote = matriz[i][i]
        if pivote == 0:
            # Encontrar una fila que tenga un valor diferente de cero en la columna actual
            for j in range(i + 1, dimension):
                if matriz[j][i] != 0:
                    matriz[i], matriz[j] = matriz[j], matriz[i]
                    print(f"Intercambio: F{i + 1} <--> F{j + 1}")
                    imprimir_matriz(matriz)
                    pivote = matriz[i][i]
                    break
            else:
                print(f"La matriz es inconsistente en la fila {i + 1}.")
                return False  # No es posible convertir a una matriz identidad

        if pivote != 1:
            matriz[i] = [x / pivote for x in matriz[i]]
            print(f"F{i + 1} --> (1/{Fraction(pivote).limit_denominator()}) * F{i + 1}")
            imprimir_matriz(matriz)

        # Hacer ceros en las demás filas en la columna i
        for j in range(dimension):
            if j != i:
                factor = matriz[j][i]
                matriz[j] = [matriz[j][k] - factor * matriz[i][k] for k in range(dimension)]
                print(f"F{j + 1} --> F{j + 1} - ({Fraction(factor).limit_denominator()}) * F{i + 1}")
                imprimir_matriz(matriz)
    return True


def matriz_identidad(dimension):
    """
         Funcion crear la matriz identidad.

         Args:
             dimension (int): la dimension de la matriz

         Returns: la lista que contiene la matriz identidad.
         """
    identidad = [[1 if i == j else 0 for j in range(dimension)] for i in range(dimension)]
    return identidad

