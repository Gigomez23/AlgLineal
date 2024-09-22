import customtkinter as ctk
from fractions import Fraction
from tkinter import messagebox


class VectorMultiplicacionFrame(ctk.CTkFrame):
    """
    Frame para la multiplicación de un vector fila por un vector columna utilizando customtkinter.

    Args:
        parent (CTkWidget): El widget padre que contendrá este frame.
    """
    def __init__(self, parent):
        super().__init__(parent)

        # Configuración del frame
        self.label_fila = ctk.CTkLabel(self, text="Introduce el vector fila (separado por comas):")
        self.label_fila.pack(pady=10)
        self.entry_fila = ctk.CTkEntry(self, width=400)
        self.entry_fila.pack(pady=10)

        self.label_columna = ctk.CTkLabel(self, text="Introduce el vector columna (separado por comas):")
        self.label_columna.pack(pady=10)
        self.entry_columna = ctk.CTkEntry(self, width=400)
        self.entry_columna.pack(pady=10)

        self.button_calculate = ctk.CTkButton(self, text="Calcular Multiplicación", command=self.calcular_multiplicacion)
        self.button_calculate.pack(pady=20)

        self.result_text = ctk.CTkTextbox(self, height=200, width=500)
        self.result_text.pack(pady=10)
        self.result_text.configure(state="disabled")  # Hacer que el textbox sea de solo lectura

    def calcular_multiplicacion(self):
        """
        Función que calcula la multiplicación entre el vector fila y el vector columna y muestra el proceso y el resultado.
        """
        try:
            fila_str = self.entry_fila.get().strip()
            columna_str = self.entry_columna.get().strip()

            # Parse vectors
            fila = list(map(Fraction, fila_str.split(',')))
            columna = list(map(Fraction, columna_str.split(',')))

            # Check dimensions
            if len(fila) != len(columna):
                raise ValueError("El número de elementos en el vector fila debe ser igual al número de elementos en el vector columna.")

            # Calculando el proceso
            process_steps = []
            for i in range(len(fila)):
                process_steps.append(f"{fila[i]} * {columna[i]} = {fila[i] * columna[i]}")

            # Suma de los productos
            result = sum(fila[i] * columna[i] for i in range(len(fila)))

            # Mostrar el proceso y el resultado
            process_str = "\n".join(process_steps)
            result_str = f"\nResultado de la multiplicación: {result}"

            self.result_text.configure(state="normal")  # Habilitar la edición para mostrar resultados
            self.result_text.delete(1.0, ctk.END)
            self.result_text.insert(ctk.END, f"Proceso de la multiplicación:\n{process_str}\n{result_str}")
            self.result_text.configure(state="disabled")  # Volver a dejarlo como solo lectura

        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {e}")


# Uso en una aplicación más grande
if __name__ == "__main__":
    class AplicacionPrincipal(ctk.CTk):
        """
        Aplicación principal que contiene el frame de multiplicación de vectores.
        """
        def __init__(self):
            super().__init__()

            self.title("Multiplicación de Vectores Fila y Columna")
            self.geometry("600x600")

            # Frame de Multiplicación de Vectores
            self.vector_multiplicacion_frame = VectorMultiplicacionFrame(self)
            self.vector_multiplicacion_frame.pack(padx=20, pady=20, fill="both", expand=True)

    app = AplicacionPrincipal()
    app.mainloop()
