"""
Archivo: frame_grafica.py 1.0.0
Descripción: Este archivo contiene la interfáz gráfica de la grafica en un window.
"""
# todo: funciones complejas no se grafican, x^3, trig, exp.
# todo: queda un subproceso lo cual no permite cerrar correctamente la App

import re
import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, sympify, lambdify
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CTkMessagebox import CTkMessagebox

class GraficarFuncionFrame(ctk.CTkFrame):
    def __init__(self, master, textbox):
        super().__init__(master)
        self.textbox = textbox
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Etiqueta para mostrar los valores al pasar el mouse sobre la gráfica
        self.valor_label = ctk.CTkLabel(self, text="Valor: (x, y)", font=("Arial", 14))
        self.valor_label.pack(pady=10, padx=10)

        # Botón de graficar
        self.boton_graficar = ctk.CTkButton(self, text="Graficar Función", command=self.graficar_funcion, width=200, height=40)
        self.boton_graficar.pack(pady=10)

        # Inicializar canvas
        self.canvas = None

    def obtener_funcion(self):
        """Convierte la expresión ingresada en el textbox a una función entendible por Python."""
        expresion = self.textbox.get()

        # Reemplazar superíndices y operadores de potencia
        expresion = expresion.replace('²', '**2')  # Superíndice 2
        expresion = expresion.replace('³', '**3')  # Superíndice 3
        expresion = expresion.replace('^', '**')   # Operador ^ por **

        # Reemplazar funciones trigonométricas en español por las equivalentes en inglés
        expresion = expresion.replace('sen', 'sin')
        expresion = expresion.replace('cos', 'cos')
        expresion = expresion.replace('tan', 'tan')
        expresion = expresion.replace('sec', 'sec')

        # Agregar multiplicación implícita donde sea necesario
        expresion = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expresion)  # Ejemplo: 2x -> 2*x, 2(x+1) -> 2*(x+1)

        x = symbols('x')  # Definir el símbolo 'x'

        try:
            # Convertir la expresión a formato simbólico
            funcion_simb = sympify(expresion)
            # Convertir la expresión simbólica a una función numérica para graficar
            funcion_numerica = lambdify(x, funcion_simb, modules=['numpy'])
            return funcion_numerica
        except Exception as e:
            raise ValueError(f"Error al interpretar la función: {e}")

    def graficar_funcion(self):
        try:
            # Obtener la función en formato numérico
            funcion = self.obtener_funcion()

            # Generar puntos para graficar
            x_vals = np.linspace(-10, 10, 400)
            y_vals = funcion(x_vals)

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
                try:
                    y_pos = funcion(x_pos)
                    self.valor_label.configure(text=f"Valor: (x: {x_pos:.2f}, y: {y_pos:.2f})")
                except Exception:
                    self.valor_label.configure(text="Valor: No definido")

            # Conectar el evento de movimiento del mouse
            fig.canvas.mpl_connect('motion_notify_event', on_move)

            # Limpiar el canvas anterior si existe
            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            # Mostrar la nueva gráfica
            self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)

        except ValueError as ve:
            CTkMessagebox(title="Error", message=f"{ve}", icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error al graficar la función: {e}", icon="cancel")
            print("Error al graficar la función:", e)

    def destroy(self):
        # Asegurarse de destruir el canvas al cerrar la ventana
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        super().destroy()
