"""
Archivo: operacion_con_vectores_calc.py 1.0.11
Descripción: Archivo que contiene el diseño del frame para operaciones con vectores.
"""
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from models.clase_vector import *
#todo: acomodar mejor el diseño para que se vea bien en la pantalla

class VectorOperacionesFrame(ctk.CTkFrame):
    """
    Frame para realizar operaciones con vectores escalados (suma y resta).

    Args:
        parent (CTk): El widget padre que contendrá este frame.
    """

    def __init__(self, parent, main_app):
        super().__init__(parent)
        self.main_app = main_app  # Guardar referencia a la aplicación principal
        self.entries = []  # Inicializar aquí
        self.scalars = []  # Inicializar aquí

        self.label_dim = ctk.CTkLabel(self, text="Dimensión de los vectores:")
        self.label_dim.pack(pady=10)
        self.entry_dim = ctk.CTkEntry(self)
        self.entry_dim.pack(pady=10)

        self.label_num = ctk.CTkLabel(self, text="Número de vectores:")
        self.label_num.pack(pady=10)
        self.entry_num = ctk.CTkEntry(self)
        self.entry_num.pack(pady=10)

        self.button_create = ctk.CTkButton(self, text="Generar Entradas", command=self.generar_entradas)
        self.button_create.pack(pady=20)

        self.result_text = ctk.CTkTextbox(self, height=200, width=500)
        self.result_text.pack(pady=10)
        self.result_text.configure(state="disabled")  # Deshabilitar edición inicial del textbox

        # Botón "Limpiar"
        self.button_clear = ctk.CTkButton(self, text="Limpiar", command=self.limpiar_campos)
        self.button_clear.pack(pady=10)

    def generar_entradas(self):
        """
        Genera las entradas necesarias para los vectores y escalares según el número de vectores y dimensión.
        """
        try:
            self.dimension = int(self.entry_dim.get())
            self.num_vectores = int(self.entry_num.get())
            if self.dimension <= 0 or self.num_vectores < 2:
                raise ValueError("Dimensión o número de vectores inválidos.")
        except ValueError as e:
            CTkMessagebox(title="Error de formato", message=f"Entrada inválida: {e}",
                          icon="warning", option_1="Entendido", button_hover_color="green")
            return

        for widget in self.winfo_children():
            widget.destroy()

        self.label_op = ctk.CTkLabel(self, text="Selecciona la operación:")
        self.label_op.pack(pady=10)

        self.op_var = ctk.StringVar()
        self.op_add = ctk.CTkRadioButton(self, text="Suma", variable=self.op_var, value='suma')
        self.op_add.pack(pady=5)
        self.op_sub = ctk.CTkRadioButton(self, text="Resta", variable=self.op_var, value='resta')
        self.op_sub.pack(pady=5)
        self.op_both = ctk.CTkRadioButton(self, text="Ambas", variable=self.op_var, value='ambas')
        self.op_both.pack(pady=5)

        # Crear entradas de vectores y escalares
        for i in range(self.num_vectores):
            ctk.CTkLabel(self, text=f"Vector {i + 1} (separados por comas):").pack(pady=5)
            entry = ctk.CTkEntry(self)
            entry.pack(pady=5)
            self.entries.append(entry)

            ctk.CTkLabel(self, text=f"Escalar para el Vector {i + 1}:").pack(pady=5)
            scalar = ctk.CTkEntry(self)
            scalar.pack(pady=5)
            self.scalars.append(scalar)

        self.result_text = ctk.CTkTextbox(self, height=200, width=500)
        self.result_text.pack(pady=10)
        self.result_text.configure(state="disabled")  # Deshabilitar edición del resultado

        # Frame para botones
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10)

        # Botones
        self.button_calculate = ctk.CTkButton(self.button_frame, text="Calcular", command=self.calcular_resultados)
        self.button_calculate.pack(side="left", padx=5)

        self.button_back = ctk.CTkButton(self.button_frame, text="Regresar", command=lambda: self.main_app.cambiar_frame_vector(VectorOperacionesFrame))
        self.button_back.pack(side="left", padx=5)

        #todo: asegurar de que todavía pueda hacer calculos despues de "Limpiar"
        self.button_clear = ctk.CTkButton(self.button_frame, text="Limpiar", command=self.limpiar_campos_dos)
        self.button_clear.pack(side="left", padx=5)

    def mostrar_entradas(self):
        """Reinicializa el frame de operaciones con vectores."""
        # Reiniciar el frame actual llamando al método cambiar_frame_vector de la aplicación principal
        self.main_app.cambiar_frame_vector(VectorOperacionesFrame, self.main_app)


    def limpiar_campos(self):
        """Limpia todos los campos de entrada y el resultado."""
        self.entry_dim.delete(0, ctk.END)
        self.entry_num.delete(0, ctk.END)
        for entry in self.entries:
            entry.delete(0, ctk.END)
        for scalar in self.scalars:
            scalar.delete(0, ctk.END)
        self.result_text.configure(state="normal")
        self.result_text.delete(1.0, ctk.END)
        self.result_text.configure(state="disabled")
        self.entries.clear()  # Limpiar la lista de entradas
        self.scalars.clear()  # Limpiar la lista de escalares

    def limpiar_campos_dos(self):
        """Limpia todos los campos de entrada y resultado para el segundo frame"""
        self.result_text.delete(0, ctk.END)
        for entry in self.entries:
            entry.delete(0, ctk.END)
        for scalar in self.scalars:
            scalar.delete(0, ctk.END)
        self.result_text.configure(state="normal")
        self.result_text.delete(1.0, ctk.END)
        self.result_text.configure(state="disabled")
        self.entries.clear()  # Limpiar la lista de entradas
        self.scalars.clear()  # Limpiar la lista de escalares


    def calcular_resultados(self):
        """
        Calcula las operaciones seleccionadas (suma, resta o ambas) con los vectores ingresados.
        """
        try:
            vectores = [Vector(*entry.get().split(',')) for entry in self.entries]
            escalares = [Fraction(scalar.get()) for scalar in self.scalars]

            vectores_escalados = [v.multiplicar_por_escalar(e) for v, e in zip(vectores, escalares)]

            operacion = self.op_var.get()

            if operacion not in {'suma', 'resta', 'ambas'}:
                raise ValueError("Operación no válida.")

            resultados = []

            if operacion == 'suma' or operacion == 'ambas':
                resultado_suma = vectores_escalados[0]
                for v in vectores_escalados[1:]:
                    resultado_suma = resultado_suma + v
                resultados.append(
                    "\nResultado de la suma:\n" + mostrar_vectores_lado_a_lado(vectores_escalados, resultado_suma,
                                                                               'suma'))

            if operacion == 'resta' or operacion == 'ambas':
                resultado_resta = vectores_escalados[0]
                for v in vectores_escalados[1:]:
                    resultado_resta = resultado_resta - v
                resultados.append(
                    "\nResultado de la resta:\n" + mostrar_vectores_lado_a_lado(vectores_escalados, resultado_resta,
                                                                                'resta'))

            self.result_text.configure(state="normal")
            self.result_text.delete(1.0, ctk.END)
            self.result_text.insert(ctk.END, "\n".join(resultados))
            self.result_text.configure(state="disabled")

        except Exception as e:
            CTkMessagebox(title="Advertencia", message=f"Error en el cálculo: {e}",
                          icon="warning", option_1="Entendido", button_hover_color="green")


# Uso en una aplicación más grande
if __name__ == "__main__":
    class AplicacionPrincipal(ctk.CTk):
        """
        Aplicación principal que contiene el frame de operaciones con vectores.
        """

        def __init__(self):
            super().__init__()

            self.title("Operaciones con Vectores Escalados")
            self.geometry("600x600")

            # Frame de operaciones con vectores
            self.vector_operaciones_frame = VectorOperacionesFrame(self, self)
            self.vector_operaciones_frame.pack(padx=20, pady=20, fill="both", expand=True)

        def cambiar_frame_vector(self, frame_class):
            """Cambia el frame actual por uno nuevo."""
            self.vector_operaciones_frame.pack_forget()  # Oculta el frame actual
            self.vector_operaciones_frame = frame_class(self, self)  # Crea un nuevo frame
            self.vector_operaciones_frame.pack(padx=20, pady=20, fill="both", expand=True)  # Muestra el nuevo frame

    app = AplicacionPrincipal()
    app.mainloop()
