"""
Archivo: newton_raphston_resolve.py 2.0.0
Descripción: Archivo con funciones de calcular y mostrar resultados de método de raphston.
"""
import sympy as sp
from models.modelos_func.clase_newton_raphson import NewtonRaphson
import customtkinter as ctk
from tkinter import Text, END
from CTkTable import CTkTable


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
        error_final (float): El error alcanzado en la última iteración.
    """
    try:
        x = sp.symbols('x')
        funcion = sp.sympify(expr_texto)

        metodo_newton = NewtonRaphson(funcion, x)
        raiz, iteraciones, convergencia = metodo_newton.calcular_raiz(x0, tolerancia=error_tol, max_iter=max_iter)

        # Calcular el error de la última iteración
        if iteraciones:
            error_final = iteraciones[-1][5]  # Suponiendo que el error se guarda en la 6ª columna de la iteración
        else:
            error_final = 0.0  # En caso de que no haya iteraciones

        return iteraciones, raiz, convergencia, error_final
    except Exception as e:
        raise ValueError(f"Ocurrió un error al calcular la raíz: {str(e)}")



def mostrar_resultados_newton(iteraciones, xr, converged, parent_frame, tolerancia_error):
    """
    Muestra los resultados del cálculo en una ventana emergente usando un diseño elegante.

    Args:
        iteraciones (list): Lista de iteraciones con los resultados.
        xr (float): La raíz aproximada.
        converged (bool): Si el método convergió.
        parent_frame (tkinter.Frame): El frame donde se muestra la ventana emergente.
        tolerancia_error (float): El error alcanzado en la última iteración.
    """
    # Crear ventana emergente
    resultados_ventana = ctk.CTkToplevel(parent_frame)
    resultados_ventana.title("Resultados - Método de Newton-Raphson")
    resultados_ventana.geometry("700x500")

    # Crear tabla con los resultados de las iteraciones
    encabezados = ["Iteración", "Xi", "f(Xi)", "f'(Xi)", "Xi+1", "Error"]
    datos = [[iteracion[0], f"{iteracion[1]:.5f}", f"{iteracion[2]:.5f}", f"{iteracion[3]:.5f}",
              f"{iteracion[4]:.5f}", f"{iteracion[5]:.5f}"] for iteracion in iteraciones]

    # Agregar la última fila con la raíz y el error alcanzado
    datos.append([f"{len(iteraciones) + 1}", f"{xr:.5f}", "N/A", "N/A", f"{xr:.5f}", f"{tolerancia_error:.5f}"])

    # Crear la tabla con CTkTable
    tabla = CTkTable(
        resultados_ventana,
        row=len(datos),
        column=len(encabezados),
        values=[encabezados] + datos,
        justify="center"
    )
    tabla.pack(expand=True, fill="both", padx=10, pady=10)

    # Crear un marco para los mensajes adicionales
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
    tolerancia_label = ctk.CTkLabel(info_frame, text=f"Tolerancia de error alcanzada: {tolerancia_error:.5f}", font=("Arial", 12))
    tolerancia_label.pack(pady=5, anchor="w")

    # Separador entre información y tabla
    separator = ctk.CTkFrame(resultados_ventana, height=2, width=600, fg_color="gray")
    separator.pack(pady=10, padx=10, fill="x")

