import sympy as sp

class Secante:
    def __init__(self, funcion, variable):
        # Asegurarse de que la función y la variable sean expresiones simbólicas
        if isinstance(funcion, str):
            self.funcion = sp.sympify(funcion)  # Convierte la función de cadena a expresión simbólica
        else:
            self.funcion = funcion

        if isinstance(variable, str):
            self.variable = sp.Symbol(variable)  # Convierte la variable de cadena a símbolo
        else:
            self.variable = variable

    def calcular_raiz(self, x0, x1, tolerancia=1e-7, max_iter=100):
        # Validar que x0 y x1 sean números reales
        if not isinstance(x0, (int, float)):
            raise ValueError(f"x0 debe ser un número real, pero se recibió: {type(x0)._name_}")
        if not isinstance(x1, (int, float)):
            raise ValueError(f"x1 debe ser un número real, pero se recibió: {type(x1)._name_}")

        iteraciones = []
        x = self.variable

        for i in range(max_iter):
            try:
                # Evaluar la función en x0 y x1
                f_x0 = float(self.funcion.subs(x, x0).evalf())
                f_x1 = float(self.funcion.subs(x, x1).evalf())
            except Exception as e:
                raise ValueError(
                    f"No se pudo evaluar la función en x0={x0} o x1={x1}. "
                    f"Asegúrate de que la función y los valores sean válidos. Error: {e}"
                )

            if f_x1 - f_x0 == 0:
                raise ValueError(
                    f"La diferencia entre f(x1) y f(x0) es 0 (división por cero). "
                    f"Intenta con valores iniciales diferentes."
                )

            # Calcular xn usando la fórmula del método de la secante
            xn = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
            error_aprox = abs(xn - x1)

            # Guardar iteración (número, x0, x1, xn, f(x0), f(x1), error aproximado)
            iteraciones.append((i + 1, x0, x1, xn, f_x0, f_x1, error_aprox))

            # Comprobar si el error aproximado es menor que la tolerancia
            if error_aprox < tolerancia:
                return xn, iteraciones, True

            # Actualizar valores para la siguiente iteración
            x0, x1 = x1, xn

        return xn, iteraciones, False