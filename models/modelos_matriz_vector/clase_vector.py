"""
Archivo: clase_vector_calc.py 1.0.0
Descripción: Archivo que contiene clase de vectores y funcion para mostrar vector de lado
a lado.
"""
from fractions import Fraction


class Vector:
    """
    Clase para representar un vector con componentes fraccionarias.
    """
    def __init__(self, *components):
        self.components = [Fraction(str(comp)) for comp in components]

    def __add__(self, other):
        if len(self.components) != len(other.components):
            raise ValueError("Los vectores deben tener la misma cantidad de dimensiones")
        return Vector(*(x + y for x, y in zip(self.components, other.components)))

    def __sub__(self, other):
        if len(self.components) != len(other.components):
            raise ValueError("Los vectores deben tener la misma cantidad de dimensiones")
        return Vector(*(x - y for x, y in zip(self.components, other.components)))

    def multiplicar_por_escalar(self, escalar):
        return Vector(*(comp * escalar for comp in self.components))

    def escalar(self):
        return ", ".join(str(comp) for comp in self.components)


def mostrar_vectores_lado_a_lado(vs, resultado, operacion):
    """
    Muestra los vectores y el resultado lado a lado en formato de texto.

    Args:
        vs (list): Lista de vectores.
        resultado (Vector): Resultado de la operación.
        operacion (str): Operación realizada ('suma' o 'resta').

    Returns:
        str: Representación textual de los vectores y el resultado.
    """
    max_len = max(
        max(len(str(comp)) for comp in v.components)
        for v in vs + [resultado]
    )

    operaciones = {
        'suma': '+',
        'resta': '-'
    }

    resultado_matriz = []
    for i in range(len(vs[0].components)):
        fila = "   ".join(f"→{i + 1}: [{str(v.components[i]).rjust(max_len)}]" for v in vs)
        fila += f"   {operaciones.get(operacion, '+')}   "
        fila += f"→R: [{str(resultado.components[i]).rjust(max_len)}]"
        fila += "   =   "
        resultado_matriz.append(fila)

    escalar_linea = "   ".join(
        f"→{i + 1}: {v.escalar().rjust(max_len * len(vs) + len(vs) * 5)}" for i, v in enumerate(vs))
    resultado_matriz.append(f"Escalar de cada vector: {escalar_linea}")

    return "\n".join(resultado_matriz)

