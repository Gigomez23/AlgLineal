import customtkinter as ctk
from tkinter import messagebox

class FrameEsclavoMatriz(ctk.CTkFrame):
    def __init__(self, padre, matriz_original: FrameEntradaMatriz):
        super().__init__(padre)
        self.matriz_original = matriz_original

        # Crear frame para la matriz esclava dentro del contenedor pasado como "padre"
        self.frame_matriz_esclava = ctk.CTkFrame(self)
        self.frame_matriz_esclava.pack(pady=20)

        # Inicializar variables para filas y columnas basadas en la matriz original
        self.filas = self.matriz_original.filas
        self.columnas = self.matriz_original.columnas
        self.matriz = []
        self.construir_matriz_esclava()

        # Vincular los métodos para actualizar la matriz esclava cuando cambien las dimensiones en la matriz original
        self.matriz_original.bind("<Configure>", self.actualizar_matriz_esclava)

    def construir_matriz_esclava(self):
        """Construye la matriz esclava que replica la estructura de la matriz original."""
        for widget in self.frame_matriz_esclava.winfo_children():
            widget.destroy()

        self.matriz = []
        for r in range(self.filas):
            fila = []
            for c in range(self.columnas):
                entrada = ctk.CTkEntry(self.frame_matriz_esclava, width=50, state="disabled")
                entrada.grid(row=r, column=c, padx=5, pady=5)
                fila.append(entrada)
            self.matriz.append(fila)

    def actualizar_matriz_esclava(self, event=None):
        """Actualiza la matriz esclava cuando cambian las dimensiones de la matriz original."""
        self.filas = self.matriz_original.filas
        self.columnas = self.matriz_original.columnas
        self.construir_matriz_esclava()

# Modificación en la clase Aplicacion para incluir otro frame
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
            self.frame_matriz_principal, text="Limpiar Entradas", command=self.marco_matriz.limpiar_entradas
        )
        self.boton_limpiar.pack(pady=10)

    def obtener_datos_matriz(self):
        """Imprime los datos de la matriz como un array de fracciones."""
        datos_matriz = self.marco_matriz.obtener_matriz_como_array()
        print(datos_matriz)
