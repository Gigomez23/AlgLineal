"""
Archivo: falsa_possicion_bissecio_resolve.py 2.0.0
Descripción: Diseño de módulo que contiene la propagación de las tablas.
"""
import sympy as sp
import customtkinter as ctk
from tkinter import Text, END
from CTkTable import CTkTable


def mostrar_resultados(iteraciones, xr, converged, metodo, tolerancia_error):
    """
    Muestra los resultados del cálculo en una ventana emergente usando CTkTable.

    Args:
        iteraciones (list): Lista de tuplas con los detalles de las iteraciones.
        xr (float): La raíz aproximada calculada.
        converged (bool): Indica si el método convergió o no.
        metodo (str): El nombre del método utilizado para el cálculo.
        tolerancia_error (float): La tolerancia de error alcanzada en la última iteración.
    """
    # Crear ventana emergente
    resultados_ventana = ctk.CTkToplevel()
    resultados_ventana.title(f"Resultados - Método de {metodo}")
    resultados_ventana.geometry("700x500")

    # Encabezados para la tabla
    encabezados = ["Iteración", "Xi", "Xu", "Xr", "Ea"]

    # Datos formateados para la tabla
    datos = [[iteracion[0],
              f"{iteracion[1]:.5f}",
              f"{iteracion[2]:.5f}",
              f"{iteracion[3]:.5f}",
              f"{iteracion[4]:.4f}"]
             for iteracion in iteraciones]

    # Agregar la última fila con los resultados finales
    if converged:
        datos.append([f"Final", f"{iteraciones[-1][1]:.5f}", f"{iteraciones[-1][2]:.5f}", f"{xr:.5f}", f"{tolerancia_error:.4f}"])
    else:
        datos.append([f"Final", f"{iteraciones[-1][1]:.5f}", f"{iteraciones[-1][2]:.5f}", f"{xr:.5f}", f"{tolerancia_error:.4f}"])

    # Crear tabla
    tabla = CTkTable(
        resultados_ventana,
        row=len(datos),  # Aseguramos que el número de filas sea el correcto
        column=len(encabezados),
        values=[encabezados] + datos,  # Agregar encabezados como primera fila
        justify="center"
    )
    tabla.pack(expand=True, fill="both", padx=10, pady=10)

    # Crear un marco para organizar la información adicional
    info_frame = ctk.CTkFrame(resultados_ventana)
    info_frame.pack(pady=10, padx=10, fill="x", expand=True)

    # Mensaje sobre la raíz aproximada
    raiz_label = ctk.CTkLabel(info_frame, text=f"La raíz aproximada es: {xr:.10f}", font=("Arial", 14, "bold"))
    raiz_label.pack(pady=5, anchor="w")

    # Mensaje sobre la convergencia
    convergencia_label = ctk.CTkLabel(info_frame, text=f"{'El método converge' if converged else 'El método no converge dentro del número máximo de iteraciones.'}",
                                      font=("Arial", 12), text_color="green" if converged else "red")
    convergencia_label.pack(pady=5, anchor="w")

    # Mensaje sobre la tolerancia de error alcanzada
    tolerancia_label = ctk.CTkLabel(info_frame, text=f"Tolerancia de error alcanzada: {tolerancia_error:.4f}", font=("Arial", 12))
    tolerancia_label.pack(pady=5, anchor="w")

    # Separador entre información y tabla
    separator = ctk.CTkFrame(resultados_ventana, height=2, width=600, fg_color="gray")
    separator.pack(pady=10, padx=10, fill="x")


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
        float: La última tolerancia de error calculada.
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

    # Aseguramos que la última iteración con su error se añada
    if not converged:  # Si no ha convergido, agregamos la última iteración
        ea = abs((xr - xr_old) / xr)  # Calculamos el error de la última iteración
        iteraciones.append((max_iter, xi, xu, xr, ea))

    return iteraciones, xr, converged, ea


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
        float: La última tolerancia de error calculada.
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

    # Aseguramos que la última iteración con su error se añada
    if not converged:  # Si no ha convergido, agregamos la última iteración
        ea = abs((xr - xr_old) / xr)  # Calculamos el error de la última iteración
        iteraciones.append((max_iter, xi, xu, xr, ea))

    return iteraciones, xr, converged, ea


