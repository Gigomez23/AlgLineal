"""
Archivo: frame_entrada_funcion.py 1.7.1
Descripción: Este archivo contiene la interfáz gráfica de las entradas para las calculadoras de raices.
"""
import re
import customtkinter as ctk
from sympy import symbols, pi, E

x = symbols('x')  # Definir símbolo para la expresión


class CalculadoraCientificaFrame(ctk.CTkFrame):
    def __init__(self, parent, parent_textbox):
        super().__init__(parent)
        self.parent_textbox = parent_textbox
        self.expresion = ""
        self.modo_superindice = False  # Modo superíndice

        self.frame_derecho = ctk.CTkFrame(self)
        self.frame_derecho.pack(side="right", fill="y", expand=True, padx=5, pady=5)

        self.frame_izquierdo = ctk.CTkFrame(self)
        self.frame_izquierdo.pack(side="left", fill="y", expand=True, padx=5, pady=5)

        self.categorias = {
            "Trigonometría": ['sen', 'cos', 'tan', 'sec'],
            "Funciones": ['ln', 'log', '√'],
            "Exponenciales": ['^2', '^3', 'x^x', '(', ')', 'pi', 'e']
        }

        self.categoria_var = ctk.StringVar(value="Exponenciales")
        self.menu_desplegable = ctk.CTkOptionMenu(self.frame_izquierdo, variable=self.categoria_var,
                                                  values=list(self.categorias.keys()),
                                                  command=self.mostrar_botones_categoria)
        self.menu_desplegable.pack(fill="x", padx=2, pady=2)

        self.categoria_botones_frame = ctk.CTkFrame(self.frame_izquierdo)
        self.categoria_botones_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.mostrar_botones_categoria(self.categoria_var.get())

        self.crear_botones_numericos()
        self.crear_botones_aritmeticos()
        self.crear_boton_limpiar()

        # Vincular eventos de teclado
        self.parent_textbox.bind("<Key>", self.procesar_tecla)
        self.parent_textbox.bind("<Shift_L>", self.activar_superindice)
        self.parent_textbox.bind("<KeyRelease-Shift_L>", self.desactivar_superindice)

        # Vincular las flechas del teclado
        self.parent_textbox.bind("<Left>", self.mover_caret_izquierda)
        self.parent_textbox.bind("<Right>", self.mover_caret_derecha)

    def activar_superindice(self, event):
        """Activar modo superíndice cuando se presiona Shift."""
        self.modo_superindice = True

    def desactivar_superindice(self, event):
        """Desactivar modo superíndice al soltar Shift."""
        self.modo_superindice = False

    def mover_caret_izquierda(self, event):
        """Mover el cursor hacia la izquierda."""
        pos_actual = self.parent_textbox.index("insert")
        nueva_pos = max(0, int(pos_actual) - 1)
        self.parent_textbox.icursor(nueva_pos)
        return "break"

    def mover_caret_derecha(self, event):
        """Mover el cursor hacia la derecha."""
        pos_actual = self.parent_textbox.index("insert")
        nueva_pos = min(len(self.parent_textbox.get()), int(pos_actual) + 1)
        self.parent_textbox.icursor(nueva_pos)
        return "break"

    def procesar_tecla(self, event):
        """Procesar entrada del teclado."""
        tecla = event.keysym  # Usar keysym para detectar teclas como Backspace
        caret_pos = self.parent_textbox.index("insert")  # Posición actual del cursor

        if tecla == "BackSpace":
            if int(caret_pos) > 0:  # Asegurarse de no borrar fuera de los límites
                expresion_actual = self.parent_textbox.get()
                # Borrar el carácter antes del cursor
                nueva_expresion = expresion_actual[:int(caret_pos) - 1] + expresion_actual[int(caret_pos):]
                self.parent_textbox.delete(0, "end")
                self.parent_textbox.insert(0, nueva_expresion)
                # Ajustar la posición del cursor después de borrar
                self.parent_textbox.icursor(int(caret_pos) - 1)
            return "break"  # Evitar que se ejecute el comportamiento predeterminado

        elif self.modo_superindice and event.char.isdigit():
            # Convertir el dígito a superíndice
            superindices = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵',
                            '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}
            texto_superindice = superindices.get(event.char, event.char)
            self.parent_textbox.insert("insert", texto_superindice)
            return "break"  # Evitar que la tecla normal se agregue

        elif event.char in ('+', '-', '*', '/', '.', 'x', '(', ')'):
            # Permitir caracteres especiales
            return

        elif event.char.isdigit():
            # Permitir números si no está en modo superíndice
            return

        else:
            # Bloquear cualquier otra entrada
            return "break"

    def mostrar_botones_categoria(self, nombre_categoria):
        for widget in self.categoria_botones_frame.winfo_children():
            widget.destroy()

        botones = self.categorias[nombre_categoria]
        for idx, texto in enumerate(botones):
            boton = ctk.CTkButton(self.categoria_botones_frame, text=texto,
                                  command=lambda t=texto: self.al_presionar_boton(t))
            boton.grid(row=idx // 3, column=idx % 3, padx=2, pady=2, sticky="nsew")

    def crear_botones_numericos(self):
        for i in range(1, 10):
            boton = ctk.CTkButton(self.frame_derecho, text=str(i),
                                  command=lambda t=str(i): self.al_presionar_boton(t))
            boton.grid(row=(i - 1) // 3, column=(i - 1) % 3, sticky="nsew", padx=2, pady=2)
        boton_cero = ctk.CTkButton(self.frame_derecho, text="0", command=lambda: self.al_presionar_boton("0"))
        boton_cero.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)
        boton_punto = ctk.CTkButton(self.frame_derecho, text=".", command=lambda: self.al_presionar_boton("."))
        boton_punto.grid(row=3, column=2, sticky="nsew", padx=2, pady=2)
        boton_x = ctk.CTkButton(self.frame_derecho, text="x", command=lambda: self.al_presionar_boton("x"))
        boton_x.grid(row=3, column=1, sticky="nsew", padx=2, pady=2)

    def crear_botones_aritmeticos(self):
        operaciones = ['+', '-', '*', '÷']
        for i, op in enumerate(operaciones):
            boton = ctk.CTkButton(self.frame_derecho, text=op, command=lambda t=op: self.al_presionar_boton(t))
            boton.grid(row=i, column=3, sticky="nsew", padx=2, pady=2)

    def crear_boton_limpiar(self):
        boton_limpiar = ctk.CTkButton(self.frame_derecho, text="C", command=lambda: self.al_presionar_boton("C"))
        boton_limpiar.grid(row=4, column=1, sticky="nsew", padx=2, pady=2)
        boton_borrar = ctk.CTkButton(self.frame_derecho, text="Borrar", command=lambda: self.al_presionar_boton("Borrar"))
        boton_borrar.grid(row=4, column=0, padx=2, pady=2)

    def al_presionar_boton(self, texto_boton):
        """Maneja la lógica al presionar un botón."""
        # Obtiene la posición actual del caret (cursor)
        caret_pos = self.parent_textbox.index("insert")
        expresion_actual = self.parent_textbox.get()

        if texto_boton == 'C':
            self.expresion = expresion_actual[:int(caret_pos) - 1] + expresion_actual[int(caret_pos):]
        elif texto_boton == 'Borrar':
            self.expresion = ""
        elif texto_boton == '^2':
            self.expresion = expresion_actual[:int(caret_pos)] + '²' + expresion_actual[int(caret_pos):]
        elif texto_boton == '^3':
            self.expresion = expresion_actual[:int(caret_pos)] + '³' + expresion_actual[int(caret_pos):]
        elif texto_boton == 'x^x':
            # Activar modo superíndice y esperar el valor ingresado
            self.modo_superindice = True
            self.expresion = expresion_actual  # No agrega ningún símbolo visible
        elif texto_boton in {'sen', 'cos', 'tan', 'ln', 'log', 'sec'}:
            self.expresion = expresion_actual[:int(caret_pos)] + f"{texto_boton}(" + expresion_actual[int(caret_pos):]
        elif texto_boton == 'pi':
            self.expresion = expresion_actual[:int(caret_pos)] + 'pi' + expresion_actual[int(caret_pos):]
        elif texto_boton == 'e':
            self.expresion = expresion_actual[:int(caret_pos)] + 'E' + expresion_actual[int(caret_pos):]
        elif texto_boton == '√':
            self.expresion = expresion_actual[:int(caret_pos)] + '√' + expresion_actual[int(caret_pos):]
        else:
            if self.modo_superindice and texto_boton.isdigit():
                # Mapea el número al superíndice Unicode si estamos en modo superíndice
                superindices = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵',
                                '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}
                self.expresion = (expresion_actual[:int(caret_pos)] +
                                  superindices.get(texto_boton, texto_boton) +
                                  expresion_actual[int(caret_pos):])
            else:
                self.expresion = expresion_actual[:int(caret_pos)] + texto_boton + expresion_actual[int(caret_pos):]

        # Actualiza el contenido del textbox
        self.parent_textbox.delete(0, 'end')
        self.parent_textbox.insert(0, self.expresion)

        # Mueve el caret a la posición después del texto insertado
        nueva_pos = int(caret_pos) + len(texto_boton)
        if texto_boton in {'^2', '^3', '²', '³', '√'}:  # Ajusta para caracteres especiales
            nueva_pos -= len(texto_boton) - 1
        self.parent_textbox.icursor(nueva_pos + 1)

    def procesar_shift(self, event):
        """Desactiva el modo superíndice al presionar Shift."""
        if event.keysym == "Shift_L" or event.keysym == "Shift_R":
            self.modo_superindice = False

    def obtener_funcion(self):
        """Devuelve la función ingresada en el textbox del parent en formato interpretable por Python."""
        funcion = self.parent_textbox.get()

        # Reemplaza superíndices Unicode por '**' para interpretación en Python
        funcion_modificada = funcion.replace('²', '**2').replace('³', '**3').replace('⁴', '**4').replace('⁵', '**5') \
            .replace('⁶', '**6').replace('⁷', '**7').replace('⁸', '**8').replace('⁹', '**9') \
            .replace('⁰', '**0')

        # Reemplazar nombres de funciones y corregir instancias como 3x a 3*x
        funcion_modificada = funcion_modificada.replace('sen', 'sin').replace('√', 'sqrt').replace('^', '**')

        # Reemplazar sec por 1/cos
        funcion_modificada = funcion_modificada.replace('sec', '1/cos')

        # Reemplazar el símbolo ÷ por /
        funcion_modificada = funcion_modificada.replace('÷', '/')

        # Añadir un operador * entre número y variable (por ejemplo, 3x -> 3*x)
        funcion_modificada = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', funcion_modificada)

        # Devolver la función modificada
        return funcion_modificada


# Clase principal de la aplicación
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Científica")
        self.geometry("500x500")

        # Crear un textbox en el frame principal
        self.textbox = ctk.CTkEntry(self, width=400)
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
