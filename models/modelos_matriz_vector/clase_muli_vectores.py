"""
Archivo: multi_fila_x_columna_calc.py 1.0.0
Descripcion: Archivo que contiene la clase que gestiona la clase para multiplicar vectores.
"""
class VectorMultiplicacionCalculadora:
    """
    Clase que maneja el cálculo de la multiplicación de un vector fila por un vector columna.
    """

    def __init__(self):
        self.vector_fila = []
        self.vector_columna = []
        self.resultado = None
        self.proceso = []

    def set_vectores(self, fila, columna):
        """
        Configura los vectores para el cálculo.

        Args:
            fila (list): Lista de valores para el vector fila.
            columna (list): Lista de valores para el vector columna.
        """
        if len(fila) != len(columna):
            raise ValueError(
                "El número de elementos en el vector fila debe ser igual al número de elementos en el vector columna.")

        self.vector_fila = fila
        self.vector_columna = columna

    def calcular(self):
        """
        Realiza el cálculo de la multiplicación de vectores y guarda los resultados.

        Returns:
            str: Cadena con los pasos del cálculo y el resultado final.
        """
        self.proceso = [
            f"{self.vector_fila[i]} * {self.vector_columna[i]} = {self.vector_fila[i] * self.vector_columna[i]}" for i
            in range(len(self.vector_fila))]
        self.resultado = sum(self.vector_fila[i] * self.vector_columna[i] for i in range(len(self.vector_fila)))
        return "\n".join(self.proceso) + f"\n\nResultado de la multiplicación: {self.resultado}"