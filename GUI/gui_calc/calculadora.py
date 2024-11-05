import sympy as sp
import customtkinter as ctk
from tkinter import messagebox, Text, END
from GUI.gui_calc.frame_entrada_funcion import CalculadoraCientificaFrame

class MetodosRaicesFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Etiquetas y entradas para la interfaz
        ctk.CTkLabel(self, text="Intervalo inferior (Xi):").grid(row=0, column=0, padx=10, pady=10)
        self.entry_xi = ctk.CTkEntry(self, width=200)
        self.entry_xi.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(self, text="Intervalo superior (Xu):").grid(row=1, column=0, padx=10, pady=10)
        self.entry_xu = ctk.CTkEntry(self, width=200)
        self.entry_xu.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(self, text="Error de tolerancia:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_error_tol = ctk.CTkEntry(self, width=200)
        self.entry_error_tol.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(self, text="Máximo de iteraciones (opcional):").grid(row=3, column=0, padx=10, pady=10)
        self.entry_max_iter = ctk.CTkEntry(self, width=200)
        self.entry_max_iter.grid(row=3, column=1, padx=10, pady=10)

        self.entrada_funcion = CalculadoraCientificaFrame(self)
        self.entrada_funcion.grid(row=4, column=0, pady=20, columnspan=2)

        # Botones para calcular
        btn_calcular_falsa = ctk.CTkButton(self, text="Calcular por Falsa Posición", command=self.falsa_posicion)
        btn_calcular_falsa.grid(row=5, column=0, pady=20)

        btn_calcular_biseccion = ctk.CTkButton(self, text="Calcular por Bisección", command=self.biseccion)
        btn_calcular_biseccion.grid(row=5, column=1, pady=20)

    def mostrar_resultados(self, iteraciones, xr, converged, metodo):
        resultados_ventana = ctk.CTkToplevel(self)
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

    def falsa_posicion(self):
        try:
            # expr_latex = self.entry_expr.get()
            expr_latex = self.entrada_funcion.obtener_funcion()
            xi = float(self.entry_xi.get())
            xu = float(self.entry_xu.get())
            error_tol = float(self.entry_error_tol.get())
            max_iter = int(self.entry_max_iter.get()) if self.entry_max_iter.get() else 100

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

                iteraciones.append((i + 1, xi, xu, xr, ea))

                if ea < error_tol:
                    converged = True
                    break

                if funcion.subs(x, xi) * funcion.subs(x, xr) < 0:
                    xu = xr
                else:
                    xi = xr

                xr_old = xr

            self.mostrar_resultados(iteraciones, xr, converged, "Falsa Posición")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def biseccion(self):
        try:
            # expr_latex = self.entry_expr.get()
            expr_latex = self.entrada_funcion.obtener_funcion()
            xi = float(self.entry_xi.get())
            xu = float(self.entry_xu.get())
            error_tol = float(self.entry_error_tol.get())
            max_iter = int(self.entry_max_iter.get()) if self.entry_max_iter.get() else 100

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

                iteraciones.append((i + 1, xi, xu, xr, ea))

                if ea < error_tol:
                    converged = True
                    break

                if funcion.subs(x, xi) * funcion.subs(x, xr) < 0:
                    xu = xr
                else:
                    xi = xr

                xr_old = xr

            self.mostrar_resultados(iteraciones, xr, converged, "Bisección")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("App Principal")

        # Inicia el Frame de métodos de raíces
        metodos_frame = MetodosRaicesFrame(self)
        metodos_frame.pack(expand=True, fill='both')

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()