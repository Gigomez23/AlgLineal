from fractions import Fraction

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