"""
Archivo: frame_grafica.py 1.0.0
Descripción: Este archivo contiene la interfáz gráfica de la grafica en un window.
"""
# todo: funciones complejas no se grafican, x^3, trig, exp.
# todo: queda un subproceso lo cual no permite cerrar correctamente la App

import customtkinter as ctk
import matplotlib.pyplot as plt
from sympy import symbols, sin, cos, log, exp, sqrt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math


class GraficarFuncionFrame(ctk.CTkFrame):
    def __init__(self, master, textbox):
        super().__init__(master)
        self.textbox = textbox
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(pady=10, fill="both", expand=True)

        # Etiqueta para mostrar los valores al pasar el mouse sobre la gráfica
        self.valor_label = ctk.CTkLabel(self, text="Valor: (x, y)", font=("Arial", 14))
        self.valor_label.pack(pady=10)

        # Botón de graficar
        self.boton_graficar = ctk.CTkButton(self, text="Graficar Función", command=self.graficar_funcion, width=200, height=40)
        self.boton_graficar.pack(pady=10)

    def obtener_funcion(self):
        """Convierte la expresión ingresada en el textbox a una función entendible por Python."""
        expresion = self.textbox.get()

        # Reemplazar caracteres especiales con equivalentes válidos en Python
        expresion = expresion.replace('²', '**2')
        expresion = expresion.replace('³', '**3')
        expresion = expresion.replace('π', 'math.pi')
        expresion = expresion.replace('e', 'math.e')
        expresion = expresion.replace('√', 'math.sqrt')
        expresion = expresion.replace('ln', 'math.log')
        expresion = expresion.replace('log', 'math.log10')
        expresion = expresion.replace('abs', 'math.fabs')
        expresion = expresion.replace('sin', 'math.sin')
        expresion = expresion.replace('cos', 'math.cos')
        expresion = expresion.replace('tan', 'math.tan')
        expresion = expresion.replace('asin', 'math.asin')
        expresion = expresion.replace('acos', 'math.acos')
        expresion = expresion.replace('atan', 'math.atan')
        expresion = expresion.replace('exp', 'math.exp')

        def funcion(x):
            return eval(expresion)

        return funcion

    def graficar_funcion(self):
        funcion = self.obtener_funcion()

        try:
            # Generar puntos para graficar
            x_vals = np.linspace(-10, 10, 400)
            y_vals = [funcion(x) for x in x_vals]

            # Crear la figura y personalizar la apariencia con tema oscuro
            fig, ax = plt.subplots(figsize=(8, 6), facecolor='#2e2e2e')  # Fondo oscuro para la figura
            ax.plot(x_vals, y_vals, label="f(x)", color='#00bcd4', linewidth=2)  # Color moderno de la línea
            ax.set_title("Gráfica de la Función", fontsize=16, fontweight='bold', color='white')
            ax.set_xlabel("x", fontsize=14, color='white')
            ax.set_ylabel("f(x)", fontsize=14, color='white')

            # Personalizar los ejes con color blanco
            ax.tick_params(axis='x', colors='white', labelsize=12)
            ax.tick_params(axis='y', colors='white', labelsize=12)

            # Personalizar el fondo y la malla
            ax.set_facecolor('#121212')  # Fondo de los ejes oscuro
            ax.grid(True, linestyle='--', color='gray', alpha=0.5)

            # Leyenda en blanco
            ax.legend(frameon=False, loc='best', fontsize=12, labelcolor='white')

            # Función para mostrar el valor en el label cuando el cursor pasa sobre la gráfica
            def on_move(event):
                """Actualizar el valor del punto bajo el cursor."""
                if event.inaxes != ax:
                    return

                # Obtener la posición del cursor en el gráfico
                x_pos = event.xdata
                y_pos = funcion(x_pos)

                # Actualizar el texto del valor en la etiqueta
                self.valor_label.configure(text=f"Valor: (x: {x_pos:.2f}, y: {y_pos:.2f})")

            # Conectar el evento de movimiento del mouse
            fig.canvas.mpl_connect('motion_notify_event', on_move)

            # Mostrar la gráfica en el canvas
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()  # Limpiar el canvas previo

            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            print("Error al graficar la función:", e)
