"""
Archivo: entrada_vector_esclavo_identica.py 1.0.0
Descripción: Este archivo contiene la interfáz gráfica de las entradas para las calculadoras con matrices.
"""
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from fractions import Fraction
from GUI.gui_calc_matriz.interfaz_entrada.entrada_matriz_frame import FrameEntradaMatriz
# todo: fix que columna solo se actualiza si se modifica fila


class FrameEsclavoMatriz(ctk.CTkFrame):
    def __init__(self, padre, matriz_original: FrameEntradaMatriz):
        super().__init__(padre)
        self.matriz_original = matriz_original

        # Crear frame para el vector esclavo dentro del contenedor pasado como "padre"
        self.frame_vector_esclavo = ctk.CTkFrame(self)
        self.frame_vector_esclavo.pack(pady=20)

        # Inicializar variables para filas y columnas basadas en la matriz original
        self.filas = self.matriz_original.columnas
        self.columnas = 1
        self.matriz = []
        self.construir_matriz_esclava()

        # Vincular los métodos para actualizar la matriz esclava cuando cambien las dimensiones en la matriz original
        self.matriz_original.bind("<Configure>", self.actualizar_matriz_esclava)

    def construir_matriz_esclava(self):
        """Construye la matriz esclava que replica la estructura de la matriz original."""
        for widget in self.frame_vector_esclavo.winfo_children():
            widget.destroy()

        self.matriz = []
        for r in range(self.filas):
            fila = []
            for c in range(self.columnas):
                entrada = ctk.CTkEntry(self.frame_vector_esclavo, width=50)
                entrada.grid(row=r, column=c, padx=5, pady=5)
                entrada.bind("<space>", lambda e, row=r, col=c: self.focus_siguiente_entrada(row, col))
                fila.append(entrada)
            self.matriz.append(fila)

    def actualizar_matriz_esclava(self, event=None):
        """Actualiza la matriz esclava cuando cambian las dimensiones de la matriz original."""
        self.filas = self.matriz_original.columnas
        self.columnas = 1
        self.construir_matriz_esclava()

    def focus_siguiente_entrada(self, fila_actual, columna_actual):
        """Mueve el foco a la siguiente entrada al presionar espacio."""
        siguiente_columna = columna_actual + 1
        siguiente_fila = fila_actual

        if siguiente_columna >= self.columnas:
            siguiente_columna = 0
            siguiente_fila += 1

        if siguiente_fila < self.filas:
            siguiente_entrada = self.matriz[siguiente_fila][siguiente_columna]
            siguiente_entrada.focus_set()

    def obtener_matriz_como_array(self):
        """Devuelve los valores de la matriz como un array de fracciones."""
        matriz_array = []

        for fila in self.matriz:
            datos_fila = []
            for entrada in fila:
                valor = entrada.get().strip()  # Eliminar espacios en blanco

                if not valor:
                    CTkMessagebox(title="Error", message="Hay celdas vacías en la matriz.", icon="warning",
                                  fade_in_duration=2)
                    return None  # Detener la ejecución

                try:
                    fraccion = Fraction(valor)  # Intentar convertir a fracción
                except ValueError:
                    CTkMessagebox(title="Error", message=f"Valor inválido: '{valor}'", icon="warning",
                                  fade_in_duration=2)
                    return None  # Detener la ejecución

                datos_fila.append(fraccion)

            matriz_array.append(datos_fila)

        return matriz_array

    def limpiar_entradas(self):
        """Limpia todas las entradas de la matriz y las dimensiones."""
        # Limpiar las entradas de la matriz
        for fila in self.matriz:
            for entrada in fila:
                entrada.delete(0, ctk.END)

    def importar_desde_historial(self, matriz_array):
        """Importa una matriz desde un historial y la coloca en las entradas."""
        matriz = matriz_array
        filas = len(matriz)
        columnas = len(matriz[0]) if filas > 0 else 0

        if columnas != 1:
            CTkMessagebox(title="Error", message="Lo importado no es un vector, "
                                                 "por favor selecciona un vector para este campo.", icon="warning",
                          fade_in_duration=2)
        else:
            self.filas = filas
            self.columnas = columnas

            self.construir_matriz_esclava()

            # Colocar los valores importados en las entradas de la matriz.
            for r in range(filas):
                for c in range(columnas):
                    valor = matriz[r][c]
                    valor_num = valor  # Se usa directamente como Fraction.

                    # Insertar el valor en el TextBox como string.
                    self.matriz[r][c].insert(0, str(valor_num))


# ejemplo de uso
class Aplicacion(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación Principal con MarcoMatriz")
        self.geometry("800x600")

        # Frame principal para contener la matriz original
        self.frame_matriz_principal = ctk.CTkFrame(self)
        self.frame_matriz_principal.pack(side="left", padx=20, pady=20)

        # Crear la primera instancia del frame de entrada de matriz dentro del frame principal.
        self.marco_matriz = FrameEntradaMatriz(self.frame_matriz_principal)
        self.marco_matriz.pack(pady=20)

        # Frame secundario para contener el frame esclavo
        self.frame_matriz_esclavo_container = ctk.CTkFrame(self)
        self.frame_matriz_esclavo_container.pack(side="right", padx=20, pady=20)

        # Crear la instancia del frame esclavo que se actualiza automáticamente dentro del frame secundario.
        self.marco_matriz_esclavo = FrameEsclavoMatriz(self.frame_matriz_esclavo_container, self.marco_matriz)
        self.marco_matriz_esclavo.pack(pady=20)

        # Botón para obtener los datos de la matriz.
        self.boton_obtener_datos_matriz = ctk.CTkButton(
            self.frame_matriz_principal, text="Obtener Datos de la Matriz", command=self.obtener_datos_matriz
        )
        self.boton_obtener_datos_matriz.pack(pady=10)

        # Botón para limpiar las entradas.
        self.boton_limpiar = ctk.CTkButton(
            self.frame_matriz_principal, text="Limpiar Entradas", command=self.limpiar_datos)
        self.boton_limpiar.pack(pady=10)

    def limpiar_datos(self):
        self.marco_matriz.limpiar_entradas()
        self.marco_matriz_esclavo.limpiar_entradas()

    def obtener_datos_matriz(self):
        """Imprime los datos de la matriz como un array de fracciones."""
        datos_matriz = self.marco_matriz.obtener_matriz_como_array()
        datos_matriz_2 = self.marco_matriz_esclavo.obtener_matriz_como_array()
        print(datos_matriz)
        print(datos_matriz_2)

if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Opcional, modo de apariencia
    ctk.set_default_color_theme("blue")  # Opcional, tema de color
    app = Aplicacion()
    app.mainloop()