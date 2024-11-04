import sympy as sp
import customtkinter as ctk
from tkinter import messagebox, Text, Tk, END

def mostrar_resultados(iteraciones, xr, converged, metodo):
    resultados_ventana = Tk()
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
    resultados_ventana.mainloop()

def falsa_posicion():
    try:
        expr_latex = entry_expr.get()
        xi = float(entry_xi.get())
        xu = float(entry_xu.get())
        error_tol = float(entry_error_tol.get())
        max_iter = int(entry_max_iter.get()) if entry_max_iter.get() else 100

        x = sp.symbols('x')
        funcion = sp.sympify(expr_latex)

        iteraciones = []
        ea = float('inf')
        xr_old = xi
        converged = False

        for i in range(max_iter):
            xr = xu - (funcion.subs(x, xu) * (xi - xu)) / (funcion.subs(x, xi) - funcion.subs(x, xu))

            if i > 0:
                ea = abs((xr - xr_old) / xr)

            iteraciones.append((i + 1, xi, xu, xr, ea, funcion.subs(x, xi), funcion.subs(x, xu), funcion.subs(x, xr)))

            if ea < error_tol:
                converged = True
                break

            if funcion.subs(x, xi) * funcion.subs(x, xr) < 0:
                xu = xr
            else:
                xi = xr

            xr_old = xr

        mostrar_resultados(iteraciones, xr, converged, "Falsa Posición")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def biseccion():
    try:
        expr_latex = entry_expr.get()
        xi = float(entry_xi.get())
        xu = float(entry_xu.get())
        error_tol = float(entry_error_tol.get())
        max_iter = int(entry_max_iter.get()) if entry_max_iter.get() else 100

        x = sp.symbols('x')
        funcion = sp.sympify(expr_latex)

        iteraciones = []
        ea = float('inf')
        xr_old = xi
        converged = False

        for i in range(max_iter):
            xr = (xi + xu) / 2

            if i > 0:
                ea = abs((xr - xr_old) / xr)

            iteraciones.append((i + 1, xi, xu, xr, ea, funcion.subs(x, xi), funcion.subs(x, xu), funcion.subs(x, xr)))

            if ea < error_tol:
                converged = True
                break

            if funcion.subs(x, xi) * funcion.subs(x, xr) < 0:
                xu = xr
            else:
                xi = xr

            xr_old = xr

        mostrar_resultados(iteraciones, xr, converged, "Bisección")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# Configuración de la interfaz de customTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Método de Falsa Posición")

# Etiquetas y entradas para la interfaz
ctk.CTkLabel(root, text="Función f(x):").grid(row=0, column=0, padx=10, pady=10)
entry_expr = ctk.CTkEntry(root, width=200)
entry_expr.grid(row=0, column=1, padx=10, pady=10)

ctk.CTkLabel(root, text="Intervalo inferior (Xi):").grid(row=1, column=0, padx=10, pady=10)
entry_xi = ctk.CTkEntry(root, width=200)
entry_xi.grid(row=1, column=1, padx=10, pady=10)

ctk.CTkLabel(root, text="Intervalo superior (Xu):").grid(row=2, column=0, padx=10, pady=10)
entry_xu = ctk.CTkEntry(root, width=200)
entry_xu.grid(row=2, column=1, padx=10, pady=10)

ctk.CTkLabel(root, text="Error de tolerancia:").grid(row=3, column=0, padx=10, pady=10)
entry_error_tol = ctk.CTkEntry(root, width=200)
entry_error_tol.grid(row=3, column=1, padx=10, pady=10)

ctk.CTkLabel(root, text="Máximo de iteraciones (opcional):").grid(row=4, column=0, padx=10, pady=10)
entry_max_iter = ctk.CTkEntry(root, width=200)
entry_max_iter.grid(row=4, column=1, padx=10, pady=10)

# Botones para calcular
btn_calcular_falsa = ctk.CTkButton(root, text="Calcular por Falsa Posición", command=falsa_posicion)
btn_calcular_falsa.grid(row=5, column=0, pady=20)

btn_calcular_biseccion = ctk.CTkButton(root, text="Calcular por Bisección", command=biseccion)
btn_calcular_biseccion.grid(row=5, column=1, pady=20)

root.mainloop()