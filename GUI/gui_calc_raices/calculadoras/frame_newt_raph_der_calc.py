"""
Archivo: frame_newt_raph_der_calc.py 1.0.0
Descripción: Archivo que contiene el frame como clase de la calculadora de metodo de newton raphston.
"""
import sympy as sp
import customtkinter as ctk
from tkinter import messagebox, Text, END
from models.modelos_func.clase_newton_raphson import NewtonRaphson


class MetodoNewRaphFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configurar_interfaz()

    def configurar_interfaz(self):
        frame_contenedor = ctk.CTkFrame(self)
        frame_contenedor.pack(expand=True, fill='both', padx=20, pady=20)

        # Frame izquierdo para seleccionar funciones
        self.frame_izquierdo = ctk.CTkFrame(frame_contenedor)
        self.frame_izquierdo.grid(row=0, column=2, rowspan=4, padx=10, pady=10, sticky="nsew")

        # Diccionario de categorías y botones
        self.categories = {
            "Trigonometría": ['sin', 'cos', 'tan'],
            "Funciones": ['ln', 'log', 'sqrt'],
            "(123)": ['^2', '^3', 'x^x', '(', ')', 'pi', 'e']
        }

        # Dropdown para seleccionar categoría
        self.category_var = ctk.StringVar(value="(123)")
        self.dropdown_menu = ctk.CTkOptionMenu(
            self.frame_izquierdo, variable=self.category_var,
            values=list(self.categories.keys()),
            command=self.show_category_buttons
        )
        self.dropdown_menu.pack(fill="x", padx=2, pady=2)

        # Frame para mostrar botones de la categoría seleccionada en grid
        self.category_buttons_frame = ctk.CTkFrame(self.frame_izquierdo)
        self.category_buttons_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.show_category_buttons(self.category_var.get())

        # Frame derecho para entradas de Newton-Raphson
        ctk.CTkLabel(frame_contenedor, text="Valor inicial (X0):").grid(row=0, column=0, padx=10, pady=10)
        self.entry_x0 = ctk.CTkEntry(frame_contenedor, width=200)
        self.entry_x0.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_contenedor, text="Error de tolerancia:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_error_tol = ctk.CTkEntry(frame_contenedor, width=200)
        self.entry_error_tol.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_contenedor, text="Máximo de iteraciones:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_max_iter = ctk.CTkEntry(frame_contenedor, width=200)
        self.entry_max_iter.grid(row=2, column=1, padx=10, pady=10)

        # Entrada de la función
        ctk.CTkLabel(frame_contenedor, text="Función f(x):").grid(row=3, column=0, padx=10, pady=10)
        self.entry_funcion = ctk.CTkEntry(frame_contenedor, width=200)
        self.entry_funcion.grid(row=3, column=1, padx=10, pady=10)

        # Botón para calcular
        btn_calcular_newton = ctk.CTkButton(frame_contenedor, text="Calcular por Newton-Raphson", command=self.newton_raphson)
        btn_calcular_newton.grid(row=4, column=0, columnspan=2, pady=20)

    def show_category_buttons(self, category_name):
        """Muestra los botones específicos de una categoría seleccionada en formato de cuadrícula (grid)."""
        for widget in self.category_buttons_frame.winfo_children():
            widget.destroy()  # Limpiar el frame de botones antes de agregar nuevos

        buttons = self.categories[category_name]
        for idx, text in enumerate(buttons):
            button = ctk.CTkButton(self.category_buttons_frame, text=text, command=lambda t=text: self.on_button_press(t))
            button.grid(row=idx // 3, column=idx % 3, padx=2, pady=2, sticky="nsew")

    def on_button_press(self, button_text):
        """Maneja los eventos de los botones y añade el texto al input actual."""
        current_expression = self.entry_funcion.get()

        if button_text in {'sin', 'cos', 'tan', 'ln', 'log', 'sqrt'}:
            self.entry_funcion.insert(END, f"{button_text}(")
        elif button_text == '^2':
            self.entry_funcion.insert(END, '**2')
        elif button_text == '^3':
            self.entry_funcion.insert(END, '**3')
        elif button_text == 'x^x':
            self.entry_funcion.insert(END, '**')
        elif button_text == 'pi':
            self.entry_funcion.insert(END, 'pi')
        elif button_text == 'e':
            self.entry_funcion.insert(END, 'E')
        else:
            self.entry_funcion.insert(END, button_text)

    def newton_raphson(self):
        try:
            expr_texto = self.entry_funcion.get()
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

    def obtener_funcion(self):
        """Devuelve la función ingresada en formato interpretable por SymPy."""
        funcion = self.entry_funcion.get()

        # Reemplazar patrones como 2x o 2(x) con 2*x o 2*(x)
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

    def mostrar_resultados(self, iteraciones, xr, converged, frame):
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