import sympy as sp
import customtkinter as ctk
from tkinter import messagebox, Text, END
from models.modelos_func.clase_secante import Secante
from CTkTable import CTkTable
from CTkMessagebox import CTkMessagebox

#todo: fix this

def calcular_secante(funcion_str, x0, x1, tolerancia, max_iter=100):
    try:
        # Validar que los campos no estén vacíos
        if not funcion_str:
            raise ValueError("La función f(x) no puede estar vacía.")

        # Validar la función
        try:
            funcion = sp.sympify(funcion_str)
        except Exception:
            raise ValueError("La función ingresada no es válida. Por favor, verifica su sintaxis.")

        # Validar entradas numéricas
        try:
            x0 = float(x0)
            x1 = float(x1)
            tolerancia = float(tolerancia)
        except ValueError:
            raise ValueError("X0, X1 y la tolerancia deben ser números reales.")

        # Verificar que x0 y x1 sean mayores que cero si la función es logaritmo
        if 'log' in funcion_str and (x0 <= 0 or x1 <= 0):
            raise ValueError("Los valores iniciales deben ser mayores que cero para funciones logaritmo.")

        # Validar máximo de iteraciones (opcional)
        if not max_iter:
            max_iter = 100  # Valor predeterminado si no se ingresa nada
        else:
            try:
                max_iter = int(max_iter)
                if max_iter <= 0:
                    raise ValueError("El máximo de iteraciones debe ser un número entero positivo.")
            except ValueError:
                raise ValueError("El máximo de iteraciones debe ser un número entero válido.")

        # Variable simbólica
        x = sp.symbols('x')

        # Inicializar la clase Secante
        secante = Secante(funcion, x)
        raiz, iteraciones, convergencia, error_final = secante.calcular_raiz(x0, x1, tolerancia, max_iter)

        return iteraciones, raiz, convergencia, error_final

    except ValueError as ve:
        CTkMessagebox(title="Error", message=f"Dimensiones de entrada: {str(ve)}", icon="warning", fade_in_duration=2)
    except Exception as e:
        CTkMessagebox(title="Error", message=f"Ha ocurrido un error inesperado: {e}", icon="warning",
                      fade_in_duration=2)


def mostrar_resultados_secante(iteraciones, raiz, convergencia, parent_frame, tolerancia_error):
    """
    Muestra los resultados del cálculo en una ventana emergente usando un diseño elegante para el método de la Secante.

    Args:
        iteraciones (list): Lista de iteraciones con los resultados.
        raiz (float): La raíz aproximada.
        convergencia (bool): Si el método convergió.
        parent_frame (tkinter.Frame): El frame donde se muestra la ventana emergente.
        tolerancia_error (float): El error alcanzado en la última iteración.
    """
    # Crear ventana emergente
    resultados_ventana = ctk.CTkToplevel(parent_frame)
    resultados_ventana.title("Resultados - Método de la Secante")
    resultados_ventana.geometry("700x500")

    # Crear tabla con los resultados de las iteraciones
    encabezados = ["Iteración", "X0", "X1", "Xn", "f(X0)", "f(X1)", "Error Aproximado"]
    datos = [[iteracion[0], f"{iteracion[1]:.5f}", f"{iteracion[2]:.5f}", f"{iteracion[3]:.5f}",
              f"{iteracion[4]:.5f}", f"{iteracion[5]:.5f}", f"{iteracion[6]:.5f}"] for iteracion in iteraciones]

    # Agregar la última fila con la raíz y el error alcanzado
    datos.append([f"{len(iteraciones) + 1}", f"{raiz:.5f}", "N/A", f"{raiz:.5f}", "N/A", "N/A", f"{tolerancia_error:.5f}"])

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
    raiz_label = ctk.CTkLabel(info_frame, text=f"La raíz aproximada es: {raiz:.10f}", font=("Arial", 14, "bold"))
    raiz_label.pack(pady=5, anchor="w")

    # Mensaje sobre la convergencia
    convergencia_label = ctk.CTkLabel(info_frame, text=f"{'El método converge' if convergencia else 'El método no converge dentro del número máximo de iteraciones.'}",
                                      font=("Arial", 12), text_color="green" if convergencia else "red")
    convergencia_label.pack(pady=5, anchor="w")

    # Mensaje sobre la tolerancia de error alcanzada
    tolerancia_label = ctk.CTkLabel(info_frame, text=f"Tolerancia de error alcanzada: {tolerancia_error:.5f}", font=("Arial", 12))
    tolerancia_label.pack(pady=5, anchor="w")

    # Separador entre información y tabla
    separator = ctk.CTkFrame(resultados_ventana, height=2, width=600, fg_color="gray")
    separator.pack(pady=10, padx=10, fill="x")



