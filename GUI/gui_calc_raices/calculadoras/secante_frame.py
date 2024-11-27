"""
Archivo: secante_calc_frame.py 1.2.1
Descripción: Este archivo contiene la interfáz gráfica de las entradas para el método de la secante.
"""
import sympy as sp
import customtkinter as ctk
from tkinter import messagebox, Text, END
from GUI.gui_calc_raices.funciones_entradas.frame_entrada_funcion import CalculadoraCientificaFrame
from models.modelos_func.clase_secante import Secante


class SecanteFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Crear un frame principal dentro del cual estarán todos los elementos
        frame_contenedor = ctk.CTkFrame(self)
        frame_contenedor.pack(expand=True, fill='both', padx=20, pady=20)

        # Etiquetas y entradas para la interfaz dentro del frame
        ctk.CTkLabel(frame_contenedor, text="Función f(x):").grid(row=0, column=0, padx=10, pady=10)
        self.entrada_de_funcion = ctk.CTkEntry(frame_contenedor, width=200)
        self.entrada_de_funcion.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_contenedor, text="Valor inicial (X0):").grid(row=1, column=0, padx=10, pady=10)
        self.entry_x0 = ctk.CTkEntry(frame_contenedor, width=200)
        self.entry_x0.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_contenedor, text="Valor inicial (X1):").grid(row=2, column=0, padx=10, pady=10)
        self.entry_x1 = ctk.CTkEntry(frame_contenedor, width=200)
        self.entry_x1.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_contenedor, text="Error de tolerancia:").grid(row=3, column=0, padx=10, pady=10)
        self.entry_error_tol = ctk.CTkEntry(frame_contenedor, width=200)
        self.entry_error_tol.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_contenedor, text="Máximo de iteraciones (opcional):").grid(row=4, column=0, padx=10, pady=10)
        self.entry_max_iter = ctk.CTkEntry(frame_contenedor, width=200)
        self.entry_max_iter.grid(row=4, column=1, padx=10, pady=10)

        self.btn_limpiar = ctk.CTkButton(frame_contenedor, text="Limpiar", command=self.limpiar_entradas)
        self.btn_limpiar.grid(row=5, column=1, padx=10, pady=10)

        # Calculadora científica para entrada de funciones
        self.entrada_funcion = CalculadoraCientificaFrame(frame_contenedor, self.entrada_de_funcion)
        self.entrada_funcion.grid(row=6, column=0, pady=20, columnspan=2)

        # Botón para calcular
        btn_calcular_secante = ctk.CTkButton(frame_contenedor, text="Calcular por Secante",
                                             command=self.calcular_secante)
        btn_calcular_secante.grid(row=7, column=0, pady=20, columnspan=2)

    def limpiar_entradas(self):
        self.entrada_de_funcion.delete(0, END)
        self.entry_x1.delete(0, END)
        self.entry_x0.delete(0, END)
        self.entry_error_tol.delete(0, END)
        self.entry_max_iter.delete(0, END)

    def calcular_secante(self):
        try:
            # Validar que los campos no estén vacíos
            if not self.entrada_de_funcion.get():
                raise ValueError("La función f(x) no puede estar vacía.")
            if not self.entry_x0.get():
                raise ValueError("El valor inicial X0 no puede estar vacío.")
            if not self.entry_x1.get():
                raise ValueError("El valor inicial X1 no puede estar vacío.")
            if not self.entry_error_tol.get():
                raise ValueError("El error de tolerancia no puede estar vacío.")

            # Validar la función
            try:
                funcion = sp.sympify(self.entrada_funcion.obtener_funcion())
            except Exception:
                raise ValueError("La función ingresada no es válida. Por favor, verifica su sintaxis.")

            # Validar entradas numéricas
            try:
                x0 = float(self.entry_x0.get())
                x1 = float(self.entry_x1.get())
                tolerancia = float(self.entry_error_tol.get())
            except ValueError:
                raise ValueError("X0, X1 y la tolerancia deben ser números reales.")

            # Validar máximo de iteraciones (opcional)
            max_iter = 100  # Valor predeterminado
            if self.entry_max_iter.get():
                try:
                    max_iter = int(self.entry_max_iter.get())
                    if max_iter <= 0:
                        raise ValueError("El máximo de iteraciones debe ser un número entero positivo.")
                except ValueError:
                    raise ValueError("El máximo de iteraciones debe ser un número entero válido.")

            # Variable simbólica
            x = sp.symbols('x')

            # Inicializar la clase Secante
            secante = Secante(funcion, x)
            raiz, iteraciones, convergencia = secante.calcular_raiz(x0, x1, tolerancia, max_iter)

            # Mostrar resultados
            self.mostrar_resultados(iteraciones, raiz, convergencia)

        except ValueError as ve:
            messagebox.showerror("Error de entrada", f"{str(ve)}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ha ocurrido un error inesperado: {str(e)}")

    def mostrar_resultados(self, iteraciones, raiz, converged):
        resultados_ventana = ctk.CTkToplevel(self)
        resultados_ventana.title("Resultados - Método de la Secante")

        texto_resultados = Text(resultados_ventana, wrap='none', font=('Courier', 10))
        texto_resultados.insert(END, f"{'Iteración':<10}{'X0':<10}{'X1':<10}{'Xn':<10}{'f(X0)':<15}{'f(X1)':<15}{'Error Aproximado':<15}\n")
        texto_resultados.insert(END, "-" * 90 + "\n")

        for iteracion in iteraciones:
            texto_resultados.insert(END,
                                    f"{iteracion[0]:<10}{iteracion[1]:<10.5f}{iteracion[2]:<10.5f}{iteracion[3]:<10.5f}{iteracion[4]:<15.5f}{iteracion[5]:<15.5f}{iteracion[6]:<15.5f}\n")

        texto_resultados.insert(END, f"\nLa raíz aproximada es: {raiz:.10f}")
        if converged:
            texto_resultados.insert(END, f"\nEl método converge en {len(iteraciones)} iteraciones.")
        else:
            texto_resultados.insert(END, "\nEl método no converge dentro del número máximo de iteraciones.")

        texto_resultados.config(state='disabled')
        texto_resultados.pack(expand=True, fill='both')


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("App Principal")

        # Inicia el Frame del método de la secante
        secante_frame = SecanteFrame(self)
        secante_frame.pack(expand=True, fill='both')


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()