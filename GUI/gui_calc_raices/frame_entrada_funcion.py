import customtkinter as ctk
from sympy import symbols, sympify, sin, cos, tan, log, sqrt, pi, E
import matplotlib.pyplot as plt
import numpy as np

# Definir símbolo para las expresiones
x = symbols('x')


class CalculadoraCientificaFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Variable para el contenido del display
        self.expression = ""
        self.display_var = ctk.StringVar(value="Ingrese función en términos de x")

        # Cuadro de texto para ingresar la expresión
        self.display_box = ctk.CTkEntry(self, textvariable=self.display_var, font=("Arial", 18), width=300)
        self.display_box.pack(pady=10, padx=10)

        # Frame para los botones de números y operaciones aritméticas
        self.frame_derecho = ctk.CTkFrame(self)
        self.frame_derecho.pack(side="right", fill="y", expand=True, padx=5, pady=5)

        # Frame para las categorías de botones adicionales
        self.frame_izquierdo = ctk.CTkFrame(self)
        self.frame_izquierdo.pack(side="left", fill="y", expand=True, padx=5, pady=5)

        # Diccionario de categorías y botones
        self.categories = {
            "Trigonometría": ['sin', 'cos', 'tan'],
            "Funciones": ['ln', 'log', 'sqrt'],  # Incluye ln y log
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
        current_expression = self.display_box.get()

        if button_text == 'C':
            self.expression = current_expression[:-1]  # Eliminar último caracter
        elif button_text == 'Borrar':
            self.expression = ""
            self.display_box.delete(0, "end")
        elif button_text == '^2':
            self.expression = current_expression + '**2'
        elif button_text == '^3':
            self.expression = current_expression + '**3'
        elif button_text == 'x^x':
            self.expression = current_expression + '**'
        elif button_text in {'sin', 'cos', 'tan', 'ln', 'log', 'sqrt'}:
            self.expression = current_expression + f"{button_text}("
        elif button_text == 'pi':
            self.expression = current_expression + 'pi'
        elif button_text == 'e':
            self.expression = current_expression + 'E'
        else:
            # Aquí se agrega la lógica para detectar y manejar 2x como 2*x
            if current_expression and (current_expression[-1].isdigit() or current_expression[-1] == ')'):
                self.expression = current_expression + '*' + button_text
            else:
                self.expression = current_expression + button_text

        # Actualizar el cuadro de entrada y mover el cursor al final
        self.display_var.set(self.expression)
        self.display_box.icursor(len(self.expression))  # Mover cursor al final

    def obtener_funcion(self):
        """Devuelve la función ingresada en formato interpretable por Python."""
        funcion = self.display_box.get()

        # Reemplazar patrones como 2x o 2(x) con 2*x o 2*(x)
        funcion_modificada = ""
        for i in range(len(funcion)):
            if i > 0 and (
                    (funcion[i].isalpha() and funcion[i - 1].isdigit()) or  # Detecta casos como '2x'
                    (funcion[i] == '(' and funcion[i - 1].isdigit()) or  # Detecta casos como '2('
                    (funcion[i].isdigit() and funcion[i - 1] == ')')  # Detecta casos como ')2'
            ):
                funcion_modificada += '*' + funcion[i]  # Agrega '*' antes del carácter
            else:
                funcion_modificada += funcion[i]

        return funcion_modificada

    def mostrar_grafica(self):
        """Genera y muestra la gráfica de la función ingresada en modo oscuro."""
        try:
            # Configurar el tema oscuro para la gráfica
            plt.style.use('dark_background')  # Tema oscuro en Matplotlib

            # Analizar y evaluar la expresión
            parsed_expr = sympify(self.obtener_funcion(),
                                  locals={"sin": sin, "cos": cos, "tan": tan, "ln": log, "log": log, "sqrt": sqrt,
                                          "pi": pi, "E": E})
            x_vals = np.linspace(-10, 10, 400)
            y_vals = [parsed_expr.subs(x, val).evalf() for val in x_vals]

            plt.figure("Gráfica de la función")
            plt.plot(x_vals, y_vals, label=self.obtener_funcion(), color="cyan")  # Línea en color claro
            plt.xlabel("x", color="white")
            plt.ylabel("y", color="white")
            plt.title("Gráfica de la función", color="white")
            plt.legend(facecolor="black", edgecolor="white")
            plt.grid(color="gray")
            plt.show()

        except Exception as e:
            print(f"Error al mostrar la gráfica: {e}")


# Clase principal de la aplicación
class Aplicacion(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Científica")
        self.geometry("600x400")

        # Crear la calculadora científica
        self.calculadora_frame = CalculadoraCientificaFrame(self)
        self.calculadora_frame.pack(fill="both", expand=True)


# Inicializar y ejecutar la aplicación
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
