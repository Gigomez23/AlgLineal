"""
Archivo: LU_calc_frame.py 1.0.0
Descripción: Este archivo contiene el diseño del frame para la calculadora de matrices
por método escalonado o de Gauss-Jordan para resolver por Ax=b por factorización LU.
"""
import customtkinter as ctk
from ctkcomponents import *
from tkinter import messagebox
from CTkToolTip import *
from CTkTable import CTkTable
from models.clase_matriz_fact_LU import LUFactorization
from Historial.historial_popup.historial_popup_ui import *
from GUI.interfaz_entrada.entrada_matriz_frame import *
from GUI.interfaz_entrada.entrada_vector_frame import *
from funciones_adicionales.convertir_formato_lista import *


class LUFactorizationFrame(ctk.CTkFrame):
    def __init__(self, parent, historial, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.historial = historial

        # Frames para las entradas y las salidas
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Widgets en el frame izquierdo (entrada)
        self.label_matrix = ctk.CTkLabel(self.input_frame, text="Ingrese la matriz A:")
        self.label_matrix.grid(row=0, column=0, padx=5, pady=5)

        self.btn_importar_hist = ctk.CTkButton(self.input_frame, text="Importar", command=self.abrir_historial)
        self.btn_importar_hist.grid(row=1, column=0, padx=10, pady=10)
        self.tooltip_importar = CTkToolTip(self.btn_importar_hist,
                                           message="Importar una matriz del historial")

        self.matriz_entrada = FrameEntradaMatriz(self.input_frame)
        self.matriz_entrada.grid(row=2, column=0, padx=5, pady=5)

        self.label_vector = ctk.CTkLabel(self.input_frame, text="Ingrese el vector b:")
        self.label_vector.grid(row=3, column=0, padx=5, pady=5)

        self.btn_importar_hist2 = ctk.CTkButton(self.input_frame, text="Importar", command=self.abrir_historial2)
        self.btn_importar_hist2.grid(row=4, column=0, padx=10, pady=10)
        self.tooltip_importar2 = CTkToolTip(self.btn_importar_hist2,
                                            message="Importar un vector del historial")

        self.vector_entrada = FrameEntradaVector(self.input_frame)
        self.vector_entrada.grid(row=5, column=0, padx=5, pady=5)

        self.calculate_button = ctk.CTkButton(self.input_frame, text="Calcular", command=self.calculate_lu)
        self.calculate_button.grid(row=6, column=0, padx=5, pady=10)

        # Widgets en el frame derecho (salida)
        self.output_label = ctk.CTkLabel(self.output_frame, text="Resultado")
        self.output_label.grid(row=0, column=0, padx=5, pady=5)

        self.textbox_output = ctk.CTkTextbox(self.output_frame, width=300, height=250)
        self.textbox_output.grid(row=1, column=0, padx=5, pady=5)

        self.clear_button = ctk.CTkButton(self.output_frame, text="Limpiar", command=self.limpiar_entradas)
        self.clear_button.grid(row=2, column=0, padx=5, pady=10)

        # Variables para los frames y tablas adicionales
        self.frame_matriz1 = None
        self.frame_matriz2 = None
        self.tabla_matriz_entrada = None
        self.tabla_vector_entrada = None
        self.tabla_matriz_L = None
        self.tabla_matriz_U = None
        self.tabla_vector_solucion = None
        self.lu_solver = None

    def calculate_lu(self):
        """Obtiene los valores del textbox y calcula la factorización LU."""
        try:
            # Obtener la matriz y vector del usuario
            matrix_A = self.matriz_entrada.obtener_matriz_como_array()
            vector_b = self.vector_entrada.obtener_matriz_como_array()

            # Crear instancia de la clase LUFactorization
            self.lu_solver = LUFactorization(matrix_A, vector_b)
            solution = self.lu_solver.solve()

            # Mostrar los pasos en el frame de salida
            steps = self.lu_solver.get_steps()
            self.textbox_output.delete("1.0", "end")
            self.textbox_output.insert("1.0", f"{steps}\n\nSolución (x): {solution}")

            self.crear_tablas()
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema con las entradas: {str(e)}")

    def limpiar_entradas(self):
        """Limpia los cuadros de texto de entrada y salida."""
        self.matriz_entrada.limpiar_entradas()
        self.vector_entrada.limpiar_entradas()
        self.textbox_output.delete("1.0", "end")
        self.limpiar_tablas()

    def limpiar_tablas(self):
        """Elimina los frames con las tablas y reinicia las soluciones."""

        # Destruir los frames de las tablas si existen
        if self.frame_matriz1:
            self.frame_matriz1.destroy()
            self.frame_matriz1 = None
        if self.frame_matriz2:
            self.frame_matriz2.destroy()
            self.frame_matriz2 = None

        # Reiniciar las tablas de entrada, salida y matriz reducida
        if self.tabla_matriz_entrada:
            self.tabla_matriz_entrada.destroy()
            self.tabla_matriz_entrada = None
        if self.tabla_vector_entrada:
            self.tabla_vector_entrada.destroy()
            self.tabla_vector_entrada = None
        if self.tabla_matriz_U:
            self.tabla_matriz_U.destroy()
            self.tabla_matriz_U = None
        if self.tabla_matriz_L:
            self.tabla_matriz_L.destroy()
            self.tabla_matriz_L = None
        if self.tabla_vector_solucion:
            self.tabla_vector_solucion.destroy()
            self.tabla_vector_solucion = None

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
        self.tabla_matriz1 = ctk.CTkLabel(self.frame_matriz1, text="Matriz A:")
        self.tabla_matriz1.pack(padx=10, pady=10)

        # tablas para la frame 1 que contiene los datos de entrada
        datos_tabla_entrada = self.lu_solver.original_matrix_A  # Usamos la matriz original
        self.tabla_matriz_entrada = CTkTable(self.frame_matriz1, values=datos_tabla_entrada)
        self.tabla_matriz_entrada.pack(padx=10, pady=10)

        #label para vector B
        self.label_vector_b = ctk.CTkLabel(self.frame_matriz1, text="Vector b:")
        self.label_vector_b.pack(padx=10, pady=10)

        # tablas para la frame 2 que contiene los datos de salida
        datos_tabla_salida = convertir_a_array_columnas(self.lu_solver.original_vector_b)
        self.tabla_vector_solucion = CTkTable(self.frame_matriz1, values=datos_tabla_salida)
        self.tabla_vector_solucion.pack(padx=10, pady=10)

        # label para matriz L
        self.label_matriz_L = ctk.CTkLabel(self.frame_matriz2, text="Matriz L:")
        self.label_matriz_L.pack(padx=10, pady=10)

        # tabla para matriz reduciad en frame 1
        datos_tabla_reducida = self.lu_solver.L
        self.tabla_matriz_L = CTkTable(self.frame_matriz2, values=datos_tabla_reducida)
        self.tabla_matriz_L.pack(padx=10, pady=10)

        # label para matriz U
        self.label_matriz_U = ctk.CTkLabel(self.frame_matriz2, text="Matriz U:")
        self.label_matriz_U.pack(padx=10, pady=10)

        # tabla para matriz reduciad en frame 1
        datos_tabla_reducida = self.lu_solver.U
        self.tabla_matriz_U = CTkTable(self.frame_matriz2, values=datos_tabla_reducida)
        self.tabla_matriz_U.pack(padx=10, pady=10)

        # label para vector x
        self.label_matriz_U = ctk.CTkLabel(self.frame_matriz2, text="Vector x:")
        self.label_matriz_U.pack(padx=10, pady=10)

        # tablas para la frame 2 que contiene los datos de salida
        datos_tabla_salida = convertir_a_array_columnas(self.lu_solver.solution_x)
        self.tabla_vector_solucion = CTkTable(self.frame_matriz2, values=datos_tabla_salida)
        self.tabla_vector_solucion.pack(padx=10, pady=10)

        #botón de guardado
        self.btn_guardar = ctk.CTkButton(self.frame_matriz2, text="Guardar", command=self.accionar_guardado)
        self.btn_guardar.pack(padx=10, pady=10)
        self.tooltip_guardar = CTkToolTip(self.btn_guardar,
                                            message="Guardar en historial")

    def accionar_guardado(self):
        vector_b = convertir_a_array_columnas(self.lu_solver.original_vector_b)
        solucion = convertir_a_array_columnas(self.lu_solver.solution_x)
        self.guardar_en_historial(self.lu_solver.original_matrix_A,
                                  vector_b, self.lu_solver.L,
                                  self.lu_solver.U, solucion)

    def guardar_en_historial(self, matriz1, matriz2, matriz3, matriz4, solucion):
        self.historial.agregar_problema(matriz1=matriz1, matriz2=matriz2, matriz3=matriz3, matriz4=matriz4,
                                        solucion=solucion, tipo="cuatro", clasificacion="mixto")
        CTkNotification(master=self, state="info",
                        message=f"{self.historial.problemas[-1]['nombre']} ha sido guardado exitosamente!",
                        side="right_bottom")

    def abrir_historial(self):
        """Abre el pop-up del historial"""
        historial_popup = HistorialPopup(self, self.historial, self.historial)
        historial_popup.grab_set()  # Esperar hasta que se cierre el popup

        # Obtener la matriz importada después de cerrar el popup
        self.wait_window(historial_popup)  # Espera hasta que se cierre el popup
        self.cargar_matriz_importada(historial_popup)

    def cargar_matriz_importada(self, historial_popup):
        """Carga la matriz importada al Textbox del FrameEntradaMatriz."""
        matriz = historial_popup.retornar_matriz_importada()
        self.matriz_entrada.importar_desde_historial(matriz)

    def abrir_historial2(self):
        """Abre el pop-up del historial"""
        historial_popup = HistorialPopup(self, self.historial, self.historial)
        historial_popup.grab_set()  # Esperar hasta que se cierre el popup

        # Obtener la matriz importada después de cerrar el popup
        self.wait_window(historial_popup)  # Espera hasta que se cierre el popup
        self.cargar_matriz_importada2(historial_popup)

    def cargar_matriz_importada2(self, historial_popup):
        """Carga la matriz importada al Textbox del FrameEntradaMatriz."""
        matriz = historial_popup.retornar_matriz_importada()
        self.vector_entrada.importar_desde_historial(matriz)


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora LU")
        self.geometry("800x400")
        historial = []

        # Crear y posicionar el frame de factorización LU
        self.lu_frame = LUFactorizationFrame(self, historial)
        self.lu_frame.pack(expand=True, fill="both")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
