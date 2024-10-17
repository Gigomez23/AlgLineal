# Archivo: cramer_frame.py
import customtkinter as ctk
from fractions import Fraction
from models.operacion_cramer import CreadorDeCramer


class CramerFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.operacion_cramer = CreadorDeCramer()

        # Definir widgets
        self.lbl_matriz = ctk.CTkLabel(self, text="Ingrese la matriz de coeficientes (una fila por línea):")
        self.txt_matriz = ctk.CTkTextbox(self, width=400, height=200)

        self.lbl_vector = ctk.CTkLabel(self, text="Ingrese el vector de términos independientes (separados por espacios):")
        self.txt_vector = ctk.CTkTextbox(self, width=400, height=50)

        self.btn_resolver = ctk.CTkButton(self, text="Resolver", command=self.resolver)
        self.txt_resultado = ctk.CTkTextbox(self, width=400, height=200)

        # Posicionar widgets dentro del frame
        self.lbl_matriz.pack(pady=10)
        self.txt_matriz.pack(pady=5)
        self.lbl_vector.pack(pady=10)
        self.txt_vector.pack(pady=5)
        self.btn_resolver.pack(pady=10)
        self.txt_resultado.pack(pady=10)

    def resolver(self):
        # Obtener los datos ingresados
        matriz_str = self.txt_matriz.get("1.0", "end-1c")
        vector_str = self.txt_vector.get("1.0", "end-1c")

        # Procesar la matriz y el vector
        matriz = self._procesar_entrada_matriz(matriz_str)
        vector = list(map(Fraction, vector_str.split()))

        # Ingresar los datos a la clase y resolver
        try:
            self.operacion_cramer.ingresar_datos_cramer(matriz, vector)
            soluciones = self.operacion_cramer.resolver_cramer()
            self.mostrar_resultado(soluciones)
        except ValueError as e:
            self.txt_resultado.insert("1.0", f"Error: {str(e)}\n")

    def _procesar_entrada_matriz(self, matriz_str):
        """Convierte la entrada de texto en una matriz."""
        filas = matriz_str.strip().split("\n")
        matriz = [list(map(Fraction, fila.split())) for fila in filas]
        return matriz

    def mostrar_resultado(self, soluciones):
        """Muestra el resultado paso a paso en la interfaz gráfica."""
        self.txt_resultado.delete("1.0", "end")  # Limpiar el cuadro de texto
        for i, solucion in enumerate(soluciones):
            self.txt_resultado.insert("end", f"x{i + 1} = {solucion}\n")

# Ejemplo de uso
if __name__ == "__main__":
    app = ctk.CTk()  # Crear la ventana principal
    app.title("Aplicación de Cramer en un Frame")

    # Crear el frame CramerFrame y agregarlo a la ventana principal
    cramer_frame = CramerFrame(app)
    cramer_frame.pack(pady=20, padx=20)

    app.mainloop()
