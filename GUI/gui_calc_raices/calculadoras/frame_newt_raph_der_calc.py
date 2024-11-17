"""
Archivo: frame_newt_raph_der_calc.py 1.2.0
Descripción: Archivo que contiene el frame como clase de la calculadora de metodo de newton raphston.
"""
import sympy as sp
import customtkinter as ctk
from tkinter import messagebox, Text, END
from models.modelos_func.clase_newton_raphson import NewtonRaphson
from GUI.gui_calc_raices.funciones_entradas.frame_entrada_funcion import CalculadoraCientificaFrame


class MetodoNewRaphFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configurar_interfaz()

    def configurar_interfaz(self):
        frame_contenedor = ctk.CTkFrame(self)
        frame_contenedor.pack(expand=True, fill='both', padx=20, pady=20)

        # Frame para entradas de Newton-Raphson
        ctk.CTkLabel(frame_contenedor, text="Función f(x):").grid(row=0, column=0, padx=10, pady=10)
        self.entry_de_funcion = ctk.CTkEntry(frame_contenedor, width=200)
        self.entry_de_funcion.grid(row=0, column=1, padx=10, pady=10)


        ctk.CTkLabel(frame_contenedor, text="Valor inicial (X0):").grid(row=1, column=0, padx=10, pady=10)
        self.entry_x0 = ctk.CTkEntry(frame_contenedor, width=200)
        self.entry_x0.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_contenedor, text="Error de tolerancia:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_error_tol = ctk.CTkEntry(frame_contenedor, width=200)
        self.entry_error_tol.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_contenedor, text="Máximo de iteraciones:").grid(row=3, column=0, padx=10, pady=10)
        self.entry_max_iter = ctk.CTkEntry(frame_contenedor, width=200)
        self.entry_max_iter.grid(row=3, column=1, padx=10, pady=10)

        # Entrada de la función
        # ctk.CTkLabel(frame_contenedor, text="Función f(x):").grid(row=3, column=0, padx=10, pady=10)
        self.entry_funcion = CalculadoraCientificaFrame(frame_contenedor, self.entry_de_funcion)
        self.entry_funcion.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Botón para calcular
        btn_calcular_newton = ctk.CTkButton(frame_contenedor, text="Calcular por Newton-Raphson",
                                            command=self.newton_raphson)
        btn_calcular_newton.grid(row=5, column=0, columnspan=2, pady=20)

    def newton_raphson(self):
        try:
            expr_texto = self.entry_funcion.obtener_funcion()
            x0 = float(self.entry_x0.get())
            error_tol = float(self.entry_error_tol.get())
            max_iter = int(self.entry_max_iter.get()) if self.entry_max_iter.get() else 100

            x = sp.symbols('x')
            funcion = sp.sympify(expr_texto)

            metodo_newton = NewtonRaphson(funcion, x)
            raiz, iteraciones, converged = metodo_newton.calcular_raiz(x0, tolerancia=error_tol, max_iter=max_iter)

            # Mostrar resultado paso a paso
            self.mostrar_resultados(iteraciones, raiz, converged, self)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def mostrar_resultados(self, iteraciones, xr, converged, frame):
        # todo: mostrat toleranica de error
        resultados_ventana = ctk.CTkToplevel(frame)
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

        texto_resultados.config(state='disabled')
        texto_resultados.pack(expand=True, fill='both')


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Métodos Numéricos")

        metodos_frame = MetodoNewRaphFrame(self)
        metodos_frame.pack(expand=True, fill='both')


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()