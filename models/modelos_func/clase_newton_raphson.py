"""
Archivo: clase_newton_raphson.py 1.0.0
Descripción: archivo que contiene la clase para calcular por metodo de newton raphson y encontrar la raíz.
"""
from models.modelos_func.clase_derivar import Derivador
from fractions import Fraction
import sympy as sp


class NewtonRaphson:
    def __init__(self, funcion, variable):
        self.funcion = funcion
        self.variable = variable
        self.derivada = Derivador.derivada(self.funcion, self.variable)

    def calcular_raiz(self, x0, tolerancia=1e-7, max_iter=100):
        iteraciones = []
        xi = x0
        x = self.variable
        for i in range(max_iter):
            f_xi = float(self.funcion.subs(x, xi))
            derivada_f_x0 = float(self.derivada.subs(x, xi))

            # Para evitar división por 0
            if derivada_f_x0 == 0:
                raise ValueError("Derivada es 0, no se puede continuar con el método.")

            xi_n = xi - f_xi / derivada_f_x0
            error_aprox = abs(xi_n - xi)  # calcular error antes de actualizar xi
            iteraciones.append((i + 1, xi, f_xi, derivada_f_x0, xi_n, error_aprox))

            xi = xi_n  # de esta manera se actualiza xi después de calcular el error

            if error_aprox < tolerancia:
                return xi, iteraciones, True  # Retornar 'iteraciones' aquí también

        return xi, iteraciones, False

