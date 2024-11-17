"""
Archivo: flasa_pos_bissecion_calc_frame.py 1.2.0
Descripción: Este archivo contiene la interfáz gráfica de las entradas para las calculadoras de raices.
"""
import sympy as sp
import customtkinter as ctk
from tkinter import messagebox, Text, END
from GUI.gui_calc_raices.funciones_entradas.frame_entrada_funcion import CalculadoraCientificaFrame


class MetodosRaicesFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Crear un frame principal dentro del cual estarán todos los elementos
        frame_contenedor = ctk.CTkFrame(self)
        frame_contenedor.pack(expand=True, fill='both', padx=20, pady=20)

        # Etiquetas y entradas para la interfaz dentro del frame
        ctk.CTkLabel(frame_contenedor, text="Funcion f(x):").grid(row=0, column=0, padx=10, pady=10)
        self.entrada_de_funcion = ctk.CTkEntry(frame_contenedor, width=200)
        self.entrada_de_funcion.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_contenedor, text="Intervalo inferior (Xi):").grid(row=1, column=0, padx=10, pady=10)
        self.entry_xi = ctk.CTkEntry(frame_contenedor, width=200)
        self.entry_xi.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_contenedor, text="Intervalo superior (Xu):").grid(row=2, column=0, padx=10, pady=10)
        self.entry_xu = ctk.CTkEntry(frame_contenedor, width=200)
        self.entry_xu.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_contenedor, text="Error de tolerancia:").grid(row=3, column=0, padx=10, pady=10)
        self.entry_error_tol = ctk.CTkEntry(frame_contenedor, width=200)
        self.entry_error_tol.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_contenedor, text="Máximo de iteraciones (opcional):").grid(row=4, column=0, padx=10, pady=10)
        self.entry_max_iter = ctk.CTkEntry(frame_contenedor, width=200)
        self.entry_max_iter.grid(row=4, column=1, padx=10, pady=10)

        # modulo de botones
        self.entrada_funcion = CalculadoraCientificaFrame(frame_contenedor, self.entrada_de_funcion)
        self.entrada_funcion.grid(row=5, column=0, pady=20, columnspan=2)

        # Botones para calcular dentro del frame
        btn_calcular_falsa = ctk.CTkButton(frame_contenedor, text="Calcular por Falsa Posición", command=self.falsa_posicion)
        btn_calcular_falsa.grid(row=6, column=0, pady=20)

        btn_calcular_biseccion = ctk.CTkButton(frame_contenedor, text="Calcular por Bisección", command=self.biseccion)
        btn_calcular_biseccion.grid(row=6, column=1, pady=20)

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
