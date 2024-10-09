"""
Archivo: jauss_jorda_calc.py 1.5.2
Descripción: Este archivo contiene el diseño del frame para la calculadora de matrices
por método escalonado o de Gauss-Jordan.
"""
import customtkinter as ctk
from models.clase_sistema_ecuaciones import *
from Historial.historial_popup_ui import *
from CTkMessagebox import CTkMessagebox
from fractions import Fraction
from CTkTable import CTkTable


class GaussJordanFrame(ctk.CTkFrame):
    """
    Frame para realizar la reducción de matrices usando el método de Gauss-Jordan.
    """

    def __init__(self, parent, historial):
        super().__init__(parent)
        self.gauss_jordan = CreadorDeEcuaciones()
        self.historial = historial

        # Frame para entradas
        self.entrada_frame = ctk.CTkFrame(self)
        self.entrada_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame para resultados
        self.resultado_frame = ctk.CTkFrame(self)
        self.resultado_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Componentes del frame de entrada
        self.label_matriz = ctk.CTkLabel(self.entrada_frame,
                                         text="Matriz (filas separadas "
                                              "por enter, valores separados por espacios):")
        self.label_matriz.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.btn_importar_hist = ctk.CTkButton(self.entrada_frame, text="Importar", command=self.abrir_historial)
        self.btn_importar_hist.grid(row=2, column=0, padx=10, pady=10)

        # Aumentar la altura del Textbox
        self.text_matriz = ctk.CTkTextbox(self.entrada_frame, width=400, height=150)
        self.text_matriz.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Botón único para resolver
        self.btn_resolver = ctk.CTkButton(self.entrada_frame, text="Resolver", command=self.resolver_matriz)
        self.btn_resolver.grid(row=4, column=0, padx=10, pady=10, sticky="")

        # Frame para resultados
        self.label_salida = ctk.CTkLabel(self.resultado_frame, text="Solución:")
        self.label_salida.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.text_salida_frame = ctk.CTkFrame(self.resultado_frame)
        self.text_salida_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.text_salida = ctk.CTkTextbox(self.text_salida_frame, width=400, height=150, wrap="none")
        self.text_salida.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.text_salida_frame, command=self.text_salida.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.text_salida.configure(yscrollcommand=self.scrollbar.set)

        # Botón para limpiar entradas
        self.btn_limpiar = ctk.CTkButton(self.resultado_frame, text="Limpiar", command=self.limpiar_entradas)
        self.btn_limpiar.grid(row=2, column=0, padx=10, pady=10, sticky="")


        # Variables para los frames y tablas adicionales
        self.frame_matriz1 = None
        self.frame_matriz2 = None
        self.tabla_matriz1 = None
        self.tabla_matriz2 = None
        self.tabla_reducida = None
        self.tabla_entrada = None
        self.tabla_salida = None

    def resolver_matriz(self):
        """Realiza la reducción de la matriz y muestra la solución."""
        matriz_text = self.text_matriz.get("1.0", "end-1c")

        if not matriz_text.strip():
            CTkMessagebox(title="Error", message="Las entradas de la matriz están vacías.", icon="warning",
                          option_1="Entendido", button_hover_color="green", fade_in_duration=2)
            return

        try:
            matriz_filas = matriz_text.split("\n")
            matriz = []
            num_columnas = None  # Almacenar el número de columnas de la primera fila

            for fila in matriz_filas:
                if fila.strip():
                    valores_fila = [Fraction(x) for x in fila.split()]

                    if num_columnas is None:
                        num_columnas = len(valores_fila)  # Guardar la cantidad de columnas de la primera fila
                    elif len(valores_fila) != num_columnas:
                        raise ValueError("Por favor revise los valores ingresado, pueda que falte un valor.")

                    matriz.append(valores_fila)

            if not matriz:
                raise ValueError("Matriz vacía")

        except ValueError as e:
            CTkMessagebox(title="Error", message=f"Error: {str(e)}", icon="warning", option_1="Entendido",
                          button_hover_color="green", fade_in_duration=2)
            return

        self.gauss_jordan.matriz = matriz
        self.gauss_jordan.matriz_original = [fila.copy() for fila in matriz]  # Guardar una copia de la matriz original
        self.gauss_jordan.filas = len(matriz)
        self.gauss_jordan.columnas = len(matriz[0]) - 1

        self.text_salida.delete("1.0", "end")
        self.gauss_jordan.pasos = 0
        self.gauss_jordan.mostrar_solucion(self.mostrar_paso)

        # Crear los frames con las tablas al presionar resolver
        self.crear_tablas()

    def crear_tablas(self):
        """Crea los frames con CTkTable para mostrar las matrices."""
        if self.frame_matriz1 or self.frame_matriz2:
            self.limpiar_tablas()

        # Frame para la primera matriz (input)
        self.frame_matriz1 = ctk.CTkFrame(self)
        self.frame_matriz1.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        # Frame para la segunda matriz (output)
        self.frame_matriz2 = ctk.CTkFrame(self)
        self.frame_matriz2.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        # labels para frames
        self.tabla_matriz1 = ctk.CTkLabel(self.frame_matriz1, text="Matriz ingresada:")
        self.tabla_matriz1.pack(padx=10, pady=10)
        self.tabla_matriz2 = ctk.CTkLabel(self.frame_matriz2, text="Solución:")
        self.tabla_matriz2.pack(padx=10, pady=10)

        # tablas para la frame 1 que contiene los datos de entrada
        datos_tabla_entrada = self.gauss_jordan.matriz_original  # Usamos la matriz original
        self.tabla_entrada = CTkTable(self.frame_matriz1, values=datos_tabla_entrada)
        self.tabla_entrada.pack(padx=10, pady=10)

        #label para matriz reducida
        self.label_matriz_reducida = ctk.CTkLabel(self.frame_matriz1, text="Matriz Reducida")
        self.label_matriz_reducida.pack(padx=10, pady=10)

        # tabla para matriz reduciad en frame 1
        datos_tabla_reducida = self.gauss_jordan.matriz
        self.tabla_reducida = CTkTable(self.frame_matriz1, values=datos_tabla_reducida)
        self.tabla_reducida.pack(padx=10, pady=10)

        # tablas para la frame 2 que contiene los datos de salida
        datos_tabla_salida = self.gauss_jordan.solucion
        if not datos_tabla_salida:
            datos_vacios = [["El sistema es inconsistente"]]
            self.tabla_salida = CTkTable(self.frame_matriz2, values=datos_vacios)
            self.tabla_salida.pack(padx=10, pady=10)
        else:
            self.tabla_salida = CTkTable(self.frame_matriz2, values=datos_tabla_salida)
            self.tabla_salida.pack(padx=10, pady=10)

        #botón de guardado
        self.btn_guardar = ctk.CTkButton(self.frame_matriz2, text="Guardar", command=self.accionar_guardado)
        self.btn_guardar.pack(padx=10, pady=10)

    def mostrar_paso(self, texto):
        """Muestra un paso del proceso de reducción en el textbox de salida."""
        self.text_salida.insert("end", texto + "\n")

    def limpiar_entradas(self):
        """Limpia los campos de entrada, la salida y las tablas."""
        self.text_matriz.delete("1.0", "end")
        self.text_salida.delete("1.0", "end")
        self.gauss_jordan.solucion = []  # Limpiar soluciones previas
        self.limpiar_tablas()

    def limpiar_tablas(self):
        """Elimina los frames con las tablas y reinicia las soluciones."""
        # Limpiar la lista de soluciones
        self.gauss_jordan.solucion = []

        # Destruir los frames de las tablas si existen
        if self.frame_matriz1:
            self.frame_matriz1.destroy()
            self.frame_matriz1 = None
        if self.frame_matriz2:
            self.frame_matriz2.destroy()
            self.frame_matriz2 = None

        # Reiniciar las tablas de entrada, salida y matriz reducida
        if self.tabla_entrada:
            self.tabla_entrada.destroy()
            self.tabla_entrada = None
        if self.tabla_salida:
            self.tabla_salida.destroy()
            self.tabla_salida = None
        if self.tabla_reducida:
            self.tabla_reducida.destroy()
            self.tabla_reducida = None

    def accionar_guardado(self):
        self.guardar_en_historial(self.gauss_jordan.matriz_original, self.gauss_jordan.matriz, self.gauss_jordan.solucion)

    def guardar_en_historial(self, matriz1, matriz2, solucion):
        self.historial.agregar_problema(matriz1, matriz2, solucion)
        CTkMessagebox(title="Guardado!", message="El Problema ha sido guardado exitosamente!",
                      icon="check", fade_in_duration=2)

    def abrir_historial(self):
        """Abre el pop-up del historial"""
        historial_popup = HistorialPopup(self, self.historial, self.text_matriz)
        historial_popup.grab_set()


# Uso del frame
if __name__ == "__main__":
    root = ctk.CTk()
    app_frame = GaussJordanFrame(root)
    app_frame.pack(padx=10, pady=10, fill="both", expand=True)
    root.mainloop()