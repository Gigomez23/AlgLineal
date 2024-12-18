from fractions import Fraction
import ast

def convertir_a_formato_lista(matriz_texto):
    """
    Convierte una matriz de texto en una lista de listas.
    Cada valor dentro de la matriz es convertido a entero o fracción si es posible.

    :param matriz_texto: Cadena de texto con las filas de la matriz separadas por líneas y los valores separados por espacios.
    :return: Lista de listas con los valores convertidos.
    """
    try:
        # Dividir la matriz de texto en filas
        filas = matriz_texto.split('\n')

        # Convertir cada fila a una lista de valores
        matriz = []
        for fila in filas:
            # Ignorar filas vacías
            if fila.strip():
                # Dividir la fila en valores y convertirlos a enteros o fracciones
                valores = [Fraction(valor) for valor in fila.split()]
                matriz.append(valores)

        return matriz
    except ValueError as e:
        # Manejar errores si no se pueden convertir los valores a fracción o entero
        raise ValueError(f"Error al convertir la matriz: {str(e)}")


def lista_a_array_strings(fraccion_lista):
    """
    Convierte una lista de fracciones en un array de strings que contienen los numeradores.

    Args:
        fraccion_lista (list): Lista con objetos Fraction.

    Returns:
        list: Lista de strings que contienen los numeradores de las fracciones.
    """
    # Extrae los numeradores de las fracciones y los convierte en strings
    resultado = [str(fr.numerator) for fr in fraccion_lista]

    return resultado


def convertir_a_array_columnas(lista):
    """
    Convierte una lista de fracciones en un array de listas con cada fracción en su propia lista.

    Args:
        lista (list of Fraction): Lista de fracciones.

    Returns:
        list of list of Fraction: Array en el formato deseado.
    """
    return [[elemento] for elemento in lista]


def convertir_a_formato_matriz(matriz_texto):
    """
    Convierte una cadena de texto en una matriz de Fracciones en el formato adecuado.

    Args:
        matriz_texto (str): Cadena de texto con las filas de la matriz separadas por líneas.

    Returns:
        list of list of Fraction: Matriz de Fracciones.
    """
    filas = matriz_texto.split('\n')
    matriz = []
    for fila in filas:
        if fila.strip():  # Ignorar filas vacías
            valores = [Fraction(valor) for valor in fila.split()]
            matriz.append(valores)
    return matriz



def lista_a_matriz(fraccion_lista):
    """
    Convierte una lista de fracciones en una matriz (lista de listas) donde cada fracción ocupa una fila.

    Args:
        fraccion_lista (list): Lista con objetos Fraction.

    Returns:
        list: Matriz donde cada fila contiene el valor de una fracción en formato str.
    """
    # Extrae los valores de las fracciones como números y crea una matriz
    resultado = [[str(fr)] for fr in
                 fraccion_lista]  # Cada fracción se convierte a flotante y se coloca en su propia fila

    return resultado


def convertir_a_matriz_de_fracciones(matriz_texto):
    """
    Convierte una matriz de listas de objetos Fraction en una lista de listas de fracciones.

    :param matriz_texto: Lista de listas con objetos Fraction.
    :return: Lista de listas con objetos Fraction.
    """
    matriz_fracciones = []

    for fila in matriz_texto:
        nueva_fila = []
        for elemento in fila:
            if isinstance(elemento, Fraction):
                nueva_fila.append(elemento)  # Solo agregar el objeto Fraction directamente
            else:
                raise TypeError(f"Se esperaba un objeto Fraction, pero se recibió: {type(elemento)}")
        matriz_fracciones.append(nueva_fila)  # Agregar la nueva fila a la matriz

    return matriz_fracciones


def a_lista_simple(vector):
    """
    Convierte una lista de listas con un solo elemento en una lista plana de elementos.

    Args:
        vector (lista de listas): Una lista donde cada elemento es una lista de un solo elemento.

    Returns:
        lista: Una lista plana con los elementos extraídos.
    """
    return [item[0] for item in vector]


def convertir_a_vector_columnar(matriz):
    """
    Convierte una matriz en un vector columnar, colocando cada elemento en una sublista.

    Args:
        matriz (list): Matriz de entrada en formato [[Fraction, Fraction, ...]].

    Returns:
        list: Matriz en formato [[Fraction], [Fraction], ...] con cada valor en una sublista.
    """
    return [[elemento] for elemento in matriz[0]]








