"""
Archivo: frame_entrada_funcion.py 1.3.1
Descripción: Este archivo contiene la interfáz gráfica de las entradas para las calculadoras de raices.
"""
# todo: bug: al presionar botón se agrega símbolo de multiplicar
# todo: convertir todo a español
# todo: agregar botones faltantes
# todo: mejorar gráfica
# todo: que pueda encontrar interválos superior e inferiores
import customtkinter as ctk
from sympy import symbols, sympify, sin, cos, tan, log, sqrt, pi, E, Eq, solve
import matplotlib.pyplot as plt
import numpy as np
from CTkMessagebox import CTkMessagebox

# Definir símbolo para las expresiones
x = symbols('x')


class CalculadoraCientificaFrame(ctk.CTkFrame):
    def __init__(self, parent, parent_textbox):
        super().__init__(parent)

        # Guardar la referencia al textbox del parent
        self.parent_textbox = parent_textbox

        # Variable para el contenido de la expresión
        self.expression = ""

        # Frame para los botones de números y operaciones aritméticas
        self.frame_derecho = ctk.CTkFrame(self)
        self.frame_derecho.pack(side="right", fill="y", expand=True, padx=5, pady=5)

        # Frame para las categorías de botones adicionales
        self.frame_izquierdo = ctk.CTkFrame(self)
        self.frame_izquierdo.pack(side="left", fill="y", expand=True, padx=5, pady=5)

        # Diccionario de categorías y botones
        self.categories = {
            "Trigonometría": ['sin', 'cos', 'tan'],
            "Funciones": ['ln', 'log', 'sqrt'],
            "(123)": ['^2', '^3', 'x^x', '(', ')', 'pi', 'e']
        }

        # Dropdown para seleccionar categoría
        self.category_var = ctk.StringVar(value="(123)")
        self.dropdown_menu = ctk.CTkOptionMenu(self.frame_izquierdo, variable=self.category_var,
                                               values=list(self.categories.keys()),
                                               command=self.show_category_buttons)
        self.dropdown_menu.pack(fill="x", padx=2, pady=2)

        # Frame para mostrar botones de la categoría seleccionada en grid
        self.category_buttons_frame = ctk.CTkFrame(self.frame_izquierdo)
        self.category_buttons_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Inicializar con los botones de la categoría seleccionada por defecto
        self.show_category_buttons(self.category_var.get())

        # Crear los botones en el frame derecho para números, operaciones aritméticas y limpiar
        self.create_numeric_buttons()
        self.create_arithmetic_buttons()
        self.create_clear_button()

        # Botón para mostrar la gráfica
        self.graph_button = ctk.CTkButton(self, text="Mostrar gráfica", command=self.mostrar_grafica)
        self.graph_button.pack(pady=10)

    def show_category_buttons(self, category_name):
        """Muestra los botones específicos de una categoría seleccionada en formato de cuadrícula (grid)."""
        for widget in self.category_buttons_frame.winfo_children():
            widget.destroy()  # Limpiar el frame de botones antes de agregar nuevos

        buttons = self.categories[category_name]
        for idx, text in enumerate(buttons):
            button = ctk.CTkButton(self.category_buttons_frame, text=text,
                                   command=lambda t=text: self.on_button_press(t))
            button.grid(row=idx // 3, column=idx % 3, padx=2, pady=2, sticky="nsew")

    def create_numeric_buttons(self):
        """Crea los botones de números y los coloca en el frame derecho."""
        for i in range(1, 10):
            button = ctk.CTkButton(self.frame_derecho, text=str(i),
                                   command=lambda t=str(i): self.on_button_press(t))
            button.grid(row=(i - 1) // 3, column=(i - 1) % 3, sticky="nsew", padx=2, pady=2)
        zero_button = ctk.CTkButton(self.frame_derecho, text="0", command=lambda: self.on_button_press("0"))
        zero_button.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)
        dot_button = ctk.CTkButton(self.frame_derecho, text=".", command=lambda: self.on_button_press("."))
        dot_button.grid(row=3, column=2, sticky="nsew", padx=2, pady=2)

    def create_arithmetic_buttons(self):
        """Crea botones de operaciones aritméticas y los coloca en el frame derecho."""
        operations = ['+', '-', '*', '/']
        for i, op in enumerate(operations):
            button = ctk.CTkButton(self.frame_derecho, text=op, command=lambda t=op: self.on_button_press(t))
            button.grid(row=i, column=3, sticky="nsew", padx=2, pady=2)

    def create_clear_button(self):
        """Crea el botón de limpiar y lo coloca en el frame derecho."""
        clear_button = ctk.CTkButton(self.frame_derecho, text="C", command=lambda: self.on_button_press("C"))
        clear_button.grid(row=3, column=3, sticky="nsew", padx=2, pady=2)

        boton_borrar = ctk.CTkButton(self.frame_derecho, text="Borrar", command=lambda: self.on_button_press("Borrar"))
        boton_borrar.grid(row=4, column=0, padx=2, pady=2)

    def on_button_press(self, button_text):
        """Maneja los eventos de los botones y añade el texto al input actual."""
        current_expression = self.parent_textbox.get("1.0", "end-1c")  # Obtener texto actual del textbox parent

        if button_text == 'C':
            self.expression = current_expression[:-1]
        elif button_text == 'Borrar':
            self.expression = ""
        elif button_text == '^2':
            self.expression = current_expression + '^2'
        elif button_text == '^3':
            self.expression = current_expression + '^3'
        elif button_text == 'x^x':
            self.expression = current_expression + '^'
        elif button_text in {'sin', 'cos', 'tan', 'ln', 'log', 'sqrt'}:
            self.expression = current_expression + f"{button_text}("
        elif button_text == 'pi':
            self.expression = current_expression + 'pi'
        elif button_text == 'e':
            self.expression = current_expression + 'E'
        else:
            self.expression = current_expression + button_text

        # Actualizar el textbox del parent
        self.parent_textbox.delete("1.0", "end")
        self.parent_textbox.insert("1.0", self.expression)

    def obtener_funcion(self):
        """Devuelve la función ingresada en el textbox del parent en formato interpretable por Python."""
        funcion = self.parent_textbox.get("1.0", "end-1c")
        funcion_modificada = ""
        for i in range(len(funcion)):
            if i > 0 and (
                    (funcion[i].isalpha() and funcion[i - 1].isdigit()) or
                    (funcion[i] == '(' and funcion[i - 1].isdigit()) or
                    (funcion[i].isdigit() and funcion[i - 1] == ')')
            ):
                funcion_modificada += '*' + funcion[i]
            else:
                funcion_modificada += funcion[i]

        return funcion_modificada

    def mostrar_grafica(self):
        """Genera y muestra la gráfica de la función ingresada en el textbox del parent."""
        try:
            plt.style.use('dark_background')
            parsed_expr = sympify(self.obtener_funcion(), locals={"sin": sin, "cos": cos, "tan": tan, "ln": log, "log": log, "sqrt": sqrt, "pi": pi, "e": E})
            intercepts = solve(parsed_expr, x)
            if not intercepts:
                intercepts = []
            center = 0 if not intercepts else float(intercepts[0])
            x_vals = np.linspace(center - 20, center + 20, 400)
            f = lambda x: float(parsed_expr.subs({'x': x})) if not isinstance(parsed_expr.subs({'x': x}), complex) else float(parsed_expr.subs({'x': x}).real)
            y_vals = [f(x_val) for x_val in x_vals]
            plt.plot(x_vals, y_vals, label=str(parsed_expr), color="cyan")
            plt.axhline(0, color='white', linewidth=0.7)
            plt.axvline(0, color='white', linewidth=0.7)
            plt.legend()
            plt.show()

        except Exception as e:
            CTkMessagebox(title="Error", message="Error al graficar: Verifique la función")


# Clase principal de la aplicación
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Científica")
        self.geometry("500x500")

        # Crear un textbox en el frame principal
        self.textbox = ctk.CTkTextbox(self, width=400, height=50)
        self.textbox.pack(pady=10)

        # Crear una instancia de CalculadoraCientificaFrame y pasarle el textbox
        self.calculadora_frame = CalculadoraCientificaFrame(self, self.textbox)
        self.calculadora_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.boton_imprimir = ctk.CTkButton(self, text="Imprimir Función", command=self.imprimir_funcion)
        self.boton_imprimir.pack(pady=10)

    def imprimir_funcion(self):
        imprimir = self.calculadora_frame.obtener_funcion()
        print(imprimir)


# Iniciar la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()
