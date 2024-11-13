"""
Archivo: frame_entrada_funcion.py 1.4.2 incomplete
Descripción: Este archivo contiene la interfáz gráfica de las entradas para las calculadoras de raices.
"""
# todo: bug: problema al graficar funciones como x^2+3
# todo: bug: al presionar botones se agregan al final
# todo: mejorar gráfica
# todo: que pueda encontrar interválos superior e inferiores
import customtkinter as ctk
from sympy import symbols, sympify, sin, cos, tan, log, sqrt, pi, E, Eq, solve
from sympy import lambdify
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
        self.expresion = ""

        # Frame para los botones de números y operaciones aritméticas
        self.frame_derecho = ctk.CTkFrame(self)
        self.frame_derecho.pack(side="right", fill="y", expand=True, padx=5, pady=5)

        # Frame para las categorías de botones adicionales
        self.frame_izquierdo = ctk.CTkFrame(self)
        self.frame_izquierdo.pack(side="left", fill="y", expand=True, padx=5, pady=5)

        # Diccionario de categorías y botones
        self.categorias = {
            "Trigonometría": ['sen', 'cos', 'tan'],
            "Funciones": ['ln', 'log', '√'],
            "(123)": ['^2', '^3', 'x^x', '(', ')', 'pi', 'e']
        }

        # Dropdown para seleccionar categoría
        self.categoria_var = ctk.StringVar(value="(123)")
        self.menu_desplegable = ctk.CTkOptionMenu(self.frame_izquierdo, variable=self.categoria_var,
                                                  values=list(self.categorias.keys()),
                                                  command=self.mostrar_botones_categoria)
        self.menu_desplegable.pack(fill="x", padx=2, pady=2)

        # Frame para mostrar botones de la categoría seleccionada en grid
        self.categoria_botones_frame = ctk.CTkFrame(self.frame_izquierdo)
        self.categoria_botones_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Inicializar con los botones de la categoría seleccionada por defecto
        self.mostrar_botones_categoria(self.categoria_var.get())

        # Crear los botones en el frame derecho para números, operaciones aritméticas y limpiar
        self.crear_botones_numericos()
        self.crear_botones_aritmeticos()
        self.crear_boton_limpiar()

        # Botón para mostrar la gráfica
        self.boton_grafica = ctk.CTkButton(self, text="Mostrar gráfica", command=self.mostrar_grafica)
        self.boton_grafica.pack(pady=10)

    def mostrar_botones_categoria(self, nombre_categoria):
        """Muestra los botones específicos de una categoría seleccionada en formato de cuadrícula (grid)."""
        for widget in self.categoria_botones_frame.winfo_children():
            widget.destroy()  # Limpiar el frame de botones antes de agregar nuevos

        botones = self.categorias[nombre_categoria]
        for idx, texto in enumerate(botones):
            boton = ctk.CTkButton(self.categoria_botones_frame, text=texto,
                                  command=lambda t=texto: self.al_presionar_boton(t))
            boton.grid(row=idx // 3, column=idx % 3, padx=2, pady=2, sticky="nsew")

    def crear_botones_numericos(self):
        """Crea los botones de números y los coloca en el frame derecho."""
        for i in range(1, 10):
            boton = ctk.CTkButton(self.frame_derecho, text=str(i),
                                  command=lambda t=str(i): self.al_presionar_boton(t))
            boton.grid(row=(i - 1) // 3, column=(i - 1) % 3, sticky="nsew", padx=2, pady=2)

        # Botón '0'
        boton_cero = ctk.CTkButton(self.frame_derecho, text="0", command=lambda: self.al_presionar_boton("0"))
        boton_cero.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)

        # Botón '.'
        boton_punto = ctk.CTkButton(self.frame_derecho, text=".", command=lambda: self.al_presionar_boton("."))
        boton_punto.grid(row=3, column=2, sticky="nsew", padx=2, pady=2)

        # Botón 'x'
        boton_x = ctk.CTkButton(self.frame_derecho, text="x", command=lambda: self.al_presionar_boton("x"))
        boton_x.grid(row=3, column=1, columnspan=1, sticky="nsew", padx=2, pady=2)

    def crear_botones_aritmeticos(self):
        """Crea botones de operaciones aritméticas y los coloca en el frame derecho."""
        operaciones = ['+', '-', '*', '/']
        for i, op in enumerate(operaciones):
            boton = ctk.CTkButton(self.frame_derecho, text=op, command=lambda t=op: self.al_presionar_boton(t))
            boton.grid(row=i, column=3, sticky="nsew", padx=2, pady=2)

    def crear_boton_limpiar(self):
        """Crea el botón de limpiar y lo coloca en el frame derecho."""
        boton_limpiar = ctk.CTkButton(self.frame_derecho, text="C", command=lambda: self.al_presionar_boton("C"))
        boton_limpiar.grid(row=3, column=3, sticky="nsew", padx=2, pady=2)

        boton_borrar = ctk.CTkButton(self.frame_derecho, text="Borrar", command=lambda: self.al_presionar_boton("Borrar"))
        boton_borrar.grid(row=4, column=0, padx=2, pady=2)

    def al_presionar_boton(self, texto_boton):
        """Maneja los eventos de los botones y añade el texto al input actual."""
        expresion_actual = self.parent_textbox.get("1.0", "end-1c")  # Obtener texto actual del textbox parent

        if texto_boton == 'C':
            self.expresion = expresion_actual[:-1]
        elif texto_boton == 'Borrar':
            self.expresion = ""
        elif texto_boton == '^2':
            self.expresion = expresion_actual + '^2'
        elif texto_boton == '^3':
            self.expresion = expresion_actual + '^3'
        elif texto_boton == 'x^x':
            self.expresion = expresion_actual + '^'
        elif texto_boton in {'sen', 'cos', 'tan', 'ln', 'log'}:
            self.expresion = expresion_actual + f"{texto_boton}("
        elif texto_boton == 'pi':
            self.expresion = expresion_actual + 'pi'
        elif texto_boton == 'e':
            self.expresion = expresion_actual + 'E'
        elif texto_boton == '√':
            self.expresion = expresion_actual + '√('
        else:
            self.expresion = expresion_actual + texto_boton

        # Actualizar el textbox del parent
        self.parent_textbox.delete("1.0", "end")
        self.parent_textbox.insert("1.0", self.expresion)

    def obtener_funcion(self):
        """Devuelve la función ingresada en el textbox del parent en formato interpretable por Python."""
        funcion = self.parent_textbox.get("1.0", "end-1c")
        # Reemplazar nombres de funciones y corregir instancias como 3x a 3*x, y ^ por **
        funcion_modificada = funcion.replace('sen', 'sin').replace('√', 'sqrt').replace('^', '**')

        # Añadir un operador * entre un número y una variable (por ejemplo, convierte '3x' en '3*x')
        import re
        funcion_modificada = re.sub(r'(\d)(x)', r'\1*\2', funcion_modificada)

        return funcion_modificada

    def mostrar_grafica(self):
        """Genera y muestra la gráfica de la función ingresada en el textbox del parent."""
        try:
            plt.style.use('dark_background')
            # Convertir la expresión con sympify para obtener una función matemática de sympy
            expresion = sympify(self.obtener_funcion(),
                                locals={"sin": sin, "cos": cos, "tan": tan, "ln": log, "log": log, "sqrt": sqrt,
                                        "pi": pi, "e": E})

            # Resolver los interceptos de la función para centrar la gráfica
            interceptos = solve(expresion, x)
            centro = 0 if not interceptos else float(interceptos[0])

            # Definir valores de x y limitar a valores positivos si es necesario
            if 'sqrt' in str(expresion):
                x_vals = np.linspace(0, centro + 20, 400)  # Limitar x a valores positivos
            else:
                x_vals = np.linspace(centro - 20, centro + 20, 400)

            # Definir función lambda para evaluar la expresión en x
            f = lambdify(x, expresion, 'numpy')

            # Evaluar y manejar excepciones para valores no evaluables
            y_vals = []
            for x_val in x_vals:
                try:
                    y_val = f(x_val)
                    # Filtrar complejos o valores extremos de y
                    if np.iscomplex(y_val) or abs(y_val) > 1e6:
                        y_vals.append(np.nan)
                    else:
                        y_vals.append(y_val)
                except:
                    y_vals.append(np.nan)  # Si hay error en la evaluación, asignar NaN

            # Convertir y_vals a numpy array para graficar
            y_vals = np.array(y_vals, dtype=np.float64)

            # Graficar la función
            plt.plot(x_vals, y_vals, label=str(expresion), color="cyan")
            plt.axhline(0, color='white', linewidth=0.7)
            plt.axvline(0, color='white', linewidth=0.7)
            plt.legend()
            plt.show()

        except Exception as e:
            CTkMessagebox(title="Error", message="Error al graficar: Verifique la función", icon="warning",
                          fade_in_duration=2)


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
