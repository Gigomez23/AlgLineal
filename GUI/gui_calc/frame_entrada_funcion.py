import customtkinter as ctk
from sympy import symbols, sympify, sin, cos, tan, log, sqrt, pi, E, solve, Eq
import matplotlib.pyplot as plt
import numpy as np

# Define symbols x and y for calculations
x, y = symbols('x y')


class CalculadoraCientifica(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Científica")
        self.geometry("400x750")

        # Display Frame
        self.display_frame = ctk.CTkFrame(self)
        self.display_frame.pack(pady=10, padx=10, fill="both", expand=False)

        # Input Box for Expression
        self.expression = ""
        self.display_var = ctk.StringVar(value="Ingrese función o ecuación en términos de x o y")
        self.display_box = ctk.CTkEntry(self.display_frame, textvariable=self.display_var, font=("Arial", 18),
                                        width=300)
        self.display_box.pack(pady=10, padx=10)

        # Input Box for x and y values
        self.values_frame = ctk.CTkFrame(self.display_frame)
        self.values_frame.pack(pady=5, padx=10, fill="both", expand=False)

        self.x_value_var = ctk.StringVar(value="Valor de x")
        self.y_value_var = ctk.StringVar(value="Valor de y")

        self.x_value_box = ctk.CTkEntry(self.values_frame, textvariable=self.x_value_var, font=("Arial", 12), width=140)
        self.x_value_box.pack(side="left", padx=5)

        self.y_value_box = ctk.CTkEntry(self.values_frame, textvariable=self.y_value_var, font=("Arial", 12), width=140)
        self.y_value_box.pack(side="right", padx=5)

        # Dropdown to select variable to solve for
        self.solve_for_var = ctk.StringVar(value="Resolver para...")
        self.solve_dropdown = ctk.CTkComboBox(self.display_frame, values=["x", "y"], variable=self.solve_for_var)
        self.solve_dropdown.pack(pady=10)

        # Button Frame
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(fill="both", expand=True)

        # Button Layout
        buttons = [
            ['7', '8', '9', '/', 'C'],
            ['4', '5', '6', '*', 'pi'],
            ['1', '2', '3', '-', 'e'],
            ['0', '.', '(', ')', '+'],
            ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt'],
            ['^', 'x', 'y', 'Borrar', 'Calcular']
        ]

        for row in buttons:
            row_buttons = ctk.CTkFrame(self.button_frame)
            row_buttons.pack(fill="both", expand=True)
            for button_text in row:
                button = ctk.CTkButton(row_buttons, text=button_text,
                                       command=lambda t=button_text: self.on_button_press(t))
                button.pack(side="left", expand=True, fill="both", padx=2, pady=2)

        # Button to Show Graph
        self.graph_button = ctk.CTkButton(self, text="Mostrar gráfica", command=self.show_graph)
        self.graph_button.pack(pady=10)

        # Text Box for Results
        self.result_display = ctk.CTkTextbox(self, height=100)
        self.result_display.pack(pady=10, padx=10, fill="both", expand=True)

        # Allow direct editing in expression box
        self.display_box.configure(state="normal")

    def on_button_press(self, button_text):
        """Handles button press events and appends to the current input."""
        current_expression = self.display_box.get()

        if button_text == 'C':
            self.expression = current_expression[:-1]  # Remove the last character
        elif button_text == 'Borrar':
            self.expression = ""
            self.display_box.delete(0, "end")
            self.result_display.delete("1.0", "end")
        elif button_text == 'Calcular':
            self.calculate_expression()
            return
        elif button_text in {'sin', 'cos', 'tan', 'log', 'ln', 'sqrt'}:
            self.expression = current_expression + f"{button_text}("
        elif button_text == 'pi':
            self.expression = current_expression + 'pi'
        elif button_text == 'e':
            self.expression = current_expression + 'E'
        elif button_text == '^':
            self.expression = current_expression + '**'
        else:
            self.expression = current_expression + button_text

        # Update input box and move cursor to end
        self.display_var.set(self.expression)
        self.display_box.icursor(len(self.expression))  # Move cursor to the end

    def calculate_expression(self):
        """Evaluates the expression or solves an equation entered with sympy and displays the result."""
        self.expression = self.display_box.get()  # Get text from input box
        try:
            # Check if the expression is an equation by looking for the "=" sign
            if "=" in self.expression:
                left_expr, right_expr = self.expression.split("=")
                parsed_left = sympify(left_expr,
                                      locals={"sin": sin, "cos": cos, "tan": tan, "log": log, "ln": log, "sqrt": sqrt,
                                              "pi": pi, "E": E})
                parsed_right = sympify(right_expr,
                                       locals={"sin": sin, "cos": cos, "tan": tan, "log": log, "ln": log, "sqrt": sqrt,
                                               "pi": pi, "E": E})

                equation = Eq(parsed_left, parsed_right)

                # Imprime la ecuación original en el textbox
                self.result_display.insert("end", f"Ecuación dada: {self.expression}\n")

                # Determine if we need to solve for a variable
                solve_for = self.solve_for_var.get()
                if solve_for in ['x', 'y']:
                    # Solve for the specified variable
                    self.result = solve(equation, symbols(solve_for))
                    self.result_display.insert("end", f"Solución para {solve_for}: {self.result}\n")
                else:
                    self.result_display.insert("end", "Por favor, selecciona una variable para resolver.\n")
            else:
                # Parse and evaluate the expression if it's not an equation
                parsed_expr = sympify(self.expression,
                                      locals={"sin": sin, "cos": cos, "tan": tan, "log": log, "ln": log, "sqrt": sqrt,
                                              "pi": pi, "E": E})
                self.result = parsed_expr

                # Imprime la expresión y el resultado en el textbox
                self.result_display.insert("end", f"Expresión dada: {self.expression}\n")

        except Exception as e:
            self.result_display.insert("end", f"Error: {e}\n")

    def show_graph(self):
        """Displays the graph in a separate window."""
        try:
            # Check if it's a function or an equation solution
            if "=" in self.expression:
                # If it's an equation, plot the solution point(s)
                solve_for = self.solve_for_var.get()
                if solve_for in ['x', 'y'] and self.result:
                    # Only plot the first solution point if there are multiple
                    plt.figure("Solución")
                    plt.plot(float(self.result[0]), 0, 'ro', label=f"{solve_for} = {self.result[0]}")
                    plt.xlabel(solve_for)
                    plt.title(f"Punto de solución para {solve_for}")
                    plt.legend()
                    plt.show()
            else:
                # If it's a function, plot the curve
                parsed_expr = sympify(self.expression,
                                      locals={"sin": sin, "cos": cos, "tan": tan, "log": log, "ln": log, "sqrt": sqrt,
                                              "pi": pi, "E": E})
                x_vals = np.linspace(-10, 10, 400)
                y_vals = [parsed_expr.subs(x, val).evalf() for val in x_vals]

                plt.figure("Gráfica de la función")
                plt.plot(x_vals, y_vals, label=self.expression)
                plt.xlabel("x")
                plt.ylabel("y")
                plt.title("Gráfica de la función")
                plt.legend()
                plt.grid()
                plt.show()

        except Exception as e:
            self.result_display.insert("end", f"Error al mostrar la gráfica: {e}\n")


if __name__ == "__main__":
    app = CalculadoraCientifica()
    app.mainloop()
