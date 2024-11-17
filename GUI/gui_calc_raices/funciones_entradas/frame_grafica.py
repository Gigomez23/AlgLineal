# grafica_frame.py
# todo: implement this
import customtkinter as ctk
from sympy import symbols, sympify, sin, cos, tan, log, sqrt, pi, E, solve
from sympy import lambdify
import matplotlib.pyplot as plt
import numpy as np
from CTkMessagebox import CTkMessagebox

x = symbols('x')  # Definir símbolo para la gráfica


class GraficaFrame(ctk.CTkFrame):
    def __init__(self, parent, parent_textbox):
        super().__init__(parent)
        self.parent_textbox = parent_textbox

        # Botón para mostrar la gráfica
        self.boton_grafica = ctk.CTkButton(self, text="Mostrar gráfica", command=self.mostrar_grafica)
        self.boton_grafica.pack(pady=10)

    def obtener_funcion(self):
        """Devuelve la función ingresada en el textbox del parent en formato interpretable por Python."""
        funcion = self.parent_textbox.get()
        funcion_modificada = funcion.replace('sen', 'sin').replace('√', 'sqrt').replace('^', '**')

        import re
        funcion_modificada = re.sub(r'(\d)(x)', r'\1*\2', funcion_modificada)
        return funcion_modificada

    def mostrar_grafica(self):
        """Genera y muestra la gráfica de la función ingresada en el textbox del parent."""
        try:
            plt.style.use('dark_background')
            expresion = sympify(self.obtener_funcion(),
                                locals={"sin": sin, "cos": cos, "tan": tan, "ln": log, "log": log, "sqrt": sqrt,
                                        "pi": pi, "e": E})

            interceptos = solve(expresion, x)
            centro = 0 if not interceptos else float(interceptos[0])

            if 'sqrt' in str(expresion):
                x_vals = np.linspace(0, centro + 20, 400)
            else:
                x_vals = np.linspace(centro - 20, centro + 20, 400)

            f = lambdify(x, expresion, 'numpy')

            y_vals = []
            for x_val in x_vals:
                try:
                    y_val = f(x_val)
                    if np.iscomplex(y_val) or abs(y_val) > 1e6:
                        y_vals.append(np.nan)
                    else:
                        y_vals.append(y_val)
                except:
                    y_vals.append(np.nan)

            y_vals = np.array(y_vals, dtype=np.float64)

            plt.plot(x_vals, y_vals, label=str(expresion), color="cyan")
            plt.axhline(0, color='white', linewidth=0.7)
            plt.axvline(0, color='white', linewidth=0.7)
            plt.legend()
            plt.show()

        except Exception as e:
            CTkMessagebox(title="Error", message="Error al graficar: Verifique la función", icon="warning",
                          fade_in_duration=2)
