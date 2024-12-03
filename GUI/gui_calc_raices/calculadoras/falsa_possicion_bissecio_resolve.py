import sympy as sp
import customtkinter as ctk
from tkinter import Text, END


def mostrar_resultados(iteraciones, xr, converged, metodo):
    """
    Muestra los resultados del cálculo en una ventana emergente.

    Args:
        iteraciones (list): Lista de tuplas con los detalles de las iteraciones.
        xr (float): La raíz aproximada calculada.
        converged (bool): Indica si el método convergió o no.
        metodo (str): El nombre del método utilizado para el cálculo.
        frame (object): El frame donde se deben mostrar los resultados.
    """
    resultados_ventana = ctk.CTkToplevel()
    resultados_ventana.title(f"Resultados - Método de {metodo}")

    texto_resultados = Text(resultados_ventana, wrap='none', font=('Courier', 10))
    texto_resultados.insert(END, f"{'Iteración':<19}{'Xi':<8}{'Xu':<7}{'Xr':<8}{'Ea':<3}\n")
    texto_resultados.insert(END, "-" * 60 + "\n")

    for iteracion in iteraciones:
        texto_resultados.insert(END,
                                f"{iteracion[0]}\t\t{iteracion[1]:.5f}\t{iteracion[2]:.5f}\t{iteracion[3]:.5f}\t{iteracion[4]:.4f}\n")

    texto_resultados.insert(END, f"\nLa raíz aproximada es: {xr:.10f}")
    if converged:
        texto_resultados.insert(END, f"\nEl método converge en {len(iteraciones)} iteraciones.")
    else:
        texto_resultados.insert(END, "\nEl método no converge dentro del número máximo de iteraciones.")

    texto_resultados.config(state='disabled')
    texto_resultados.pack(expand=True, fill='both')


def calcular_falsa_posicion(funcion_str, xi, xu, error_tol, max_iter):
    """
    Calcula la raíz de una función usando el método de Falsa Posición.

    Args:
        funcion_str (str): La función como cadena de texto.
        xi (float): El valor inicial del intervalo inferior.
        xu (float): El valor inicial del intervalo superior.
        error_tol (float): La tolerancia de error para el cálculo.
        max_iter (int): El número máximo de iteraciones.

    Returns:
        list: Una lista de iteraciones con sus valores correspondientes.
        float: La raíz aproximada calculada.
        bool: Indica si el método convergió.
    """
    x = sp.symbols('x')
    funcion = sp.sympify(funcion_str)

    iteraciones = []
    ea = float('inf')
    xr_old = xi
    converged = False

    for i in range(max_iter):
        xr = xu - (funcion.subs(x, xu) * (xi - xu)) / (funcion.subs(x, xi) - funcion.subs(x, xu))

        if i > 0:
            ea = abs((xr - xr_old) / xr)

        iteraciones.append((i + 1, xi, xu, xr, ea))

        if ea < error_tol:
            converged = True
            break

        if funcion.subs(x, xi) * funcion.subs(x, xr) < 0:
            xu = xr
        else:
            xi = xr

        xr_old = xr

    return iteraciones, xr, converged


def calcular_biseccion(funcion_str, xi, xu, error_tol, max_iter):
    """
    Calcula la raíz de una función usando el método de Bisección.

    Args:
        funcion_str (str): La función como cadena de texto.
        xi (float): El valor inicial del intervalo inferior.
        xu (float): El valor inicial del intervalo superior.
        error_tol (float): La tolerancia de error para el cálculo.
        max_iter (int): El número máximo de iteraciones.

    Returns:
        list: Una lista de iteraciones con sus valores correspondientes.
        float: La raíz aproximada calculada.
        bool: Indica si el método convergió.
    """
    x = sp.symbols('x')
    funcion = sp.sympify(funcion_str)

    iteraciones = []
    ea = float('inf')
    xr_old = xi
    converged = False

    for i in range(max_iter):
        xr = (xi + xu) / 2

        if i > 0:
            ea = abs((xr - xr_old) / xr)

        iteraciones.append((i + 1, xi, xu, xr, ea))

        if ea < error_tol:
            converged = True
            break

        if funcion.subs(x, xi) * funcion.subs(x, xr) < 0:
            xu = xr
        else:
            xi = xr

        xr_old = xr

    return iteraciones, xr, converged
