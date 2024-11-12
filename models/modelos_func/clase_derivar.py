"""
Archivo: clase_derivar.py 1.0.0
Descripción: archivo que contiene la clase para derivar.
"""
import sympy as sp


class Derivador:
    @staticmethod
    def derivada(funcion, variable):
        """
        Calcula la derivada de una función simbólica.
        :param funcion: Función simbólica de SymPy
        :param variable: Variable respecto a la cual derivar
        :return: Derivada de la función
        """
        return sp.diff(funcion, variable)
