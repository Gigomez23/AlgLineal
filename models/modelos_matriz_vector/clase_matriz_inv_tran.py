"""
Archivo: clase_matriz_inv_tran.py 1.10.1
Descripción: Este archivo contiene la interfáz gráfica de la calculadora de operaciones de matrices.
"""
from fractions import Fraction


class MatrizCalculadora:
    """
    Esta clase contiene métodos estáticos para realizar operaciones con matrices,
    como obtener una matriz de una cadena, calcular su transpuesta y su inversa.
    """

    @staticmethod
    def obtener_matriz(matriz_str):
        """
        Convierte una cadena de texto en una matriz (lista de listas) de Fracciones.

        Args:
            matriz_str (str): Cadena que representa la matriz, con filas separadas por saltos de línea
            y elementos de cada fila separados por espacios.

        Returns:
            list: Una matriz como lista de listas con valores fraccionarios.

        Raises:
            ValueError: Si el formato de la cadena es incorrecto o las filas tienen diferente número de columnas.
        """
        try:
            filas = matriz_str.split("\n")
            matriz = [list(map(lambda x: Fraction(x), fila.split())) for fila in filas]

            num_columnas = len(matriz[0])
            for fila in matriz:
                if len(fila) != num_columnas:
                    raise ValueError("Las filas tienen diferente número de columnas")
            return matriz
        except Exception as e:
            raise ValueError(f"La matriz ingresada no es válida: {str(e)}")

    @staticmethod
    def transponer_matriz(matriz):
        """
        Calcula la transpuesta de una matriz.

        Args:
            matriz (list): La matriz original como una lista de listas.

        Returns:
            list: La matriz transpuesta.
        """
        filas = len(matriz)
        columnas = len(matriz[0])
        return [[matriz[j][i] for j in range(filas)] for i in range(columnas)]

    @staticmethod
    def inversa_matriz_con_pasos(matriz):
        """
        Calcula la inversa de una matriz cuadrada utilizando el método de Gauss-Jordan.
        Devuelve tanto la matriz inversa como los pasos intermedios para el cálculo.

        Args:
            matriz (list): La matriz original como una lista de listas.

        Returns:
            tuple: Una tupla con dos elementos:
                - pasos (list): Lista de cadenas que describen los pasos del cálculo.
                - inversa (list): La matriz inversa.

        Raises:
            ValueError: Si la matriz no es cuadrada o no tiene inversa (determinante es 0).
        """
        pasos = []

        if len(matriz) != len(matriz[0]):
            raise ValueError("Solo se puede calcular la inversa de matrices cuadradas.")

        n = len(matriz)
        identidad = MatrizCalculadora.matriz_identidad(n)
        aumentada = [fila + identidad[i] for i, fila in enumerate(matriz)]

        pasos.append(f"Matriz aumentada inicial:\n{MatrizCalculadora.matriz_a_string(aumentada)}")

        for i in range(n):
            if aumentada[i][i] == 0:
                for k in range(i + 1, n):
                    if aumentada[k][i] != 0:
                        # Intercambiamos las filas
                        aumentada[i], aumentada[k] = aumentada[k], aumentada[i]
                        pasos.append(
                            f"Intercambiando fila {i + 1} con la fila {k + 1}:\n{MatrizCalculadora.matriz_a_string(aumentada)}")
                        break
                else:
                    raise ValueError("La matriz no tiene inversa (determinante es 0).")

            divisor = aumentada[i][i]
            aumentada[i] = [elemento / divisor for elemento in aumentada[i]]
            pasos.append(f"Dividiendo la fila {i + 1} por {divisor}:\n{MatrizCalculadora.matriz_a_string(aumentada)}")

            for j in range(n):
                if i != j:
                    factor = aumentada[j][i]
                    aumentada[j] = [aumentada[j][k] - factor * aumentada[i][k] for k in range(2 * n)]
                    pasos.append(
                        f"Restando {factor} veces la fila {i + 1} de la fila {j + 1}:\n{MatrizCalculadora.matriz_a_string(aumentada)}")

        inversa = [fila[n:] for fila in aumentada]
        return pasos, inversa

    @staticmethod
    def matriz_identidad(n):
        """
        Genera una matriz identidad de tamaño n.

        Args:
            n (int): Dimensión de la matriz identidad.

        Returns:
            list: Matriz identidad de tamaño n.
        """
        return [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]

    @staticmethod
    def matriz_a_string(matriz):
        """
        Convierte una matriz en una cadena de texto con formato para su visualización.

        Args:
            matriz (list): La matriz como lista de listas.

        Returns:
            str: Cadena de texto que representa la matriz.
        """
        return "\n".join(["\t".join(map(str, fila)) for fila in matriz])