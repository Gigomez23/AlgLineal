import sympy as sp
import customtkinter as ctk
from tkinter import messagebox, Text, END
from models.modelos_func.clase_secante import Secante  # Asegúrate de que la clase Secante esté importada


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
        raiz, iteraciones, convergencia = secante.calcular_raiz(x0, x1, tolerancia, max_iter)

        return iteraciones, raiz, convergencia

    except ValueError as ve:
        messagebox.showerror("Error de entrada", f"{str(ve)}")
    except Exception as e:
        messagebox.showerror("Error inesperado", f"Ha ocurrido un error inesperado: {str(e)}")


def mostrar_resultados_secante(iteraciones, raiz, convergencia):
    resultados_ventana = ctk.CTkToplevel()
    resultados_ventana.title("Resultados - Método de la Secante")

    texto_resultados = Text(resultados_ventana, wrap='none', font=('Courier', 10))
    texto_resultados.insert(END,
                            f"{'Iteración':<10}{'X0':<10}{'X1':<10}{'Xn':<10}{'f(X0)':<15}{'f(X1)':<15}{'Error Aproximado':<15}\n")
    texto_resultados.insert(END, "-" * 90 + "\n")

    for iteracion in iteraciones:
        texto_resultados.insert(END,
                                f"{iteracion[0]:<10}{iteracion[1]:<10.5f}{iteracion[2]:<10.5f}{iteracion[3]:<10.5f}{iteracion[4]:<15.5f}{iteracion[5]:<15.5f}{iteracion[6]:<15.5f}\n")

    texto_resultados.insert(END, f"\nLa raíz aproximada es: {raiz:.10f}")
    if convergencia:
        texto_resultados.insert(END, f"\nEl método converge en {len(iteraciones)} iteraciones.")
    else:
        texto_resultados.insert(END, "\nEl método no converge dentro del número máximo de iteraciones.")

    texto_resultados.config(state='disabled')
    texto_resultados.pack(expand=True, fill='both')
