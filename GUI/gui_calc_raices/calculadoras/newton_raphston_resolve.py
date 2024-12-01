# newton_raphson_func.py

import sympy as sp
from models.modelos_func.clase_newton_raphson import NewtonRaphson
import customtkinter as ctk
from tkinter import Text, END


def calcular_newton_raphson(expr_texto, x0, error_tol, max_iter=100):
    """
    Realiza el cálculo utilizando el método de Newton-Raphson y devuelve los resultados.

    Args:
        expr_texto (str): La función f(x) a evaluar.
        x0 (float): El valor inicial para el cálculo.
        error_tol (float): El error de tolerancia.
        max_iter (int, opcional): Número máximo de iteraciones. Por defecto es 100.

    Returns:
        iteraciones (list): Lista con los resultados de cada iteración.
        raiz (float): La raíz aproximada.
        converged (bool): Si el método convergió o no.
    """
    try:
        x = sp.symbols('x')
        funcion = sp.sympify(expr_texto)

        metodo_newton = NewtonRaphson(funcion, x)
        raiz, iteraciones, convergencia = metodo_newton.calcular_raiz(x0, tolerancia=error_tol, max_iter=max_iter)

        return iteraciones, raiz, convergencia
    except Exception as e:
        raise ValueError(f"Ocurrió un error al calcular la raíz: {str(e)}")


def mostrar_resultados_newton(iteraciones, xr, converged, parent_frame):
    """
    Muestra los resultados del cálculo en una ventana emergente.

    Args:
        iteraciones (list): Lista de iteraciones con los resultados.
        xr (float): La raíz aproximada.
        converged (bool): Si el método convergió.
        parent_frame (tkinter.Frame): El frame donde se muestra la ventana emergente.
    """
    resultados_ventana = ctk.CTkToplevel(parent_frame)
    resultados_ventana.title("Resultados - Método de Newton-Raphson")

    texto_resultados = Text(resultados_ventana, wrap='none', font=('Courier', 10))
    texto_resultados.insert(END,
                            f"{'Iteración':<12}{'Xi':<12}{'f(Xi)':<12}{'f\'(Xi)':<12}{'Xi+1':<12}{'Error':<12}\n")
    texto_resultados.insert(END, "-" * 70 + "\n")

    for iteracion in iteraciones:
        texto_resultados.insert(
            END,
            f"{iteracion[0]:<12}{iteracion[1]:<12.5f}{iteracion[2]:<12.5f}{iteracion[3]:<12.5f}{iteracion[4]:<12.5f}{iteracion[5]:<12.5f}\n"
        )

    texto_resultados.insert(END, f"\nLa raíz aproximada es: {xr:.10f}")
    if converged:
        texto_resultados.insert(END, f"\nEl método converge en {len(iteraciones)} iteraciones.")
    else:
        texto_resultados.insert(END, "\nEl método no converge dentro del número máximo de iteraciones.")

    texto_resultados.insert(END,
                            f"\nTolerancia de error: {str(iteraciones[0][5])}")  # Mostrar el error de tolerancia de la última iteración.

    texto_resultados.config(state='disabled')
    texto_resultados.pack(expand=True, fill='both')
