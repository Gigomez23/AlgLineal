"""
Archivo: estructura_de_calc
Descripcion: Archivo que  se utiliza como base para la estructura de las calculadora
"""


def __init__(self, parent, historial):
    super().__init__(parent)
    self.historial = historial
    self.calculadora = VectorMultiplicacionCalculadora() # operación que se va a ser desde carpeta models.

    # Frame para entrada
    self.entrada_frame = ctk.CTkFrame(self)
    self.entrada_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Frame para resultados
    self.resultado_frame = ctk.CTkFrame(self)
    self.resultado_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")