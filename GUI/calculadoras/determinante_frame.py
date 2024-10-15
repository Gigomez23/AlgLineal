import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from fractions import Fraction
from models.operaciones_determinante import OperacionesDeterminante


class DeterminanteFrame(ctk.CTkFrame):
    """
    Frame para realizar el cálculo de determinantes usando el método de Laplace.

    Args:
        parent (CTk): El widget padre que contendrá este frame.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.operaciones_determinante = OperacionesDeterminante()

        # Frame para entradas
        self.entrada_frame = ctk.CTkFrame(self)
        self.entrada_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame para resultados
        self.resultado_frame = ctk.CTkFrame(self)
        self.resultado_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Componentes del frame de entrada
        self.label_matriz = ctk.CTkLabel(self.entrada_frame, text="Matriz (separada por espacios, cada fila en una línea):")
        self.label_matriz.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        # Textbox para ingresar la matriz
        self.text_matriz = ctk.CTkTextbox(self.entrada_frame, width=400, height=150)
        self.text_matriz.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        # Botón para calcular
        self.btn_calcular = ctk.CTkButton(self.entrada_frame, text="Calcular", command=self.calcular_determinante)
        self.btn_calcular.grid(row=3, column=0, padx=10, pady=10)

        # Botón para limpiar
        self.btn_limpiar = ctk.CTkButton(self.entrada_frame, text="Limpiar", command=self.limpiar_entradas)
        self.btn_limpiar.grid(row=3, column=1, padx=10, pady=10)

        # Frame para resultados
        self.label_resultado = ctk.CTkLabel(self.resultado_frame, text="Resultado:")
        self.label_resultado.grid(row=0, column=0, padx=10, pady=10)

        self.text_salida = ctk.CTkTextbox(self.resultado_frame, width=400, height=150)
        self.text_salida.grid(row=1, column=0, padx=10, pady=10)

    def calcular_determinante(self):
        """Realiza el cálculo del determinante de la matriz introducida por el usuario."""
        matriz_text = self.text_matriz.get("1.0", "end-1c")

        if not matriz_text.strip():
            CTkMessagebox(title="Error", message="Las entradas de la matriz están vacías.", icon="warning",
                          option_1="Entendido", button_hover_color="green")
            return

        try:
            matriz_filas = matriz_text.split("\n")
            matriz = []
            for fila in matriz_filas:
                if fila.strip():
                    matriz.append([Fraction(x) for x in fila.split()])

            if len(matriz) != len(matriz[0]):
                raise ValueError("La matriz debe ser cuadrada.")

        except ValueError:
            CTkMessagebox(title="Error", message="Las entradas de la matriz contienen caracteres inválidos.",
                          icon="warning", option_1="Entendido", button_hover_color="green")
            return

        # Pasar la matriz a la clase de OperacionesDeterminante
        self.operaciones_determinante.ingresar_datos(matriz)
        det = self.operaciones_determinante.calcular_determinante()

        # Mostrar el resultado
        self.text_salida.delete("1.0", "end")
        self.text_salida.insert("end", f"Determinante: {det}\n")
        self.text_salida.insert("end", self.operaciones_determinante.obtener_procedimiento())

    def limpiar_entradas(self):
        """Limpia los campos de entrada y salida."""
        self.text_matriz.delete("1.0", "end")
        self.text_salida.delete("1.0", "end")


if __name__ == "__main__":
    root = ctk.CTk()
    app_frame = DeterminanteFrame(root)
    app_frame.pack(padx=10, pady=10, fill="both", expand=True)
    root.mainloop()