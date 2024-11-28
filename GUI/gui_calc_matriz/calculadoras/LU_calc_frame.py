"""
Archivo: LU_calc_frame.py 1.1.8
Descripción: Este archivo contiene el diseño del frame para la calculadora de matrices
por método escalonado o de Gauss-Jordan para resolver por Ax=b por factorización LU.
"""
from ctkcomponents import *
from CTkToolTip import *
from models.modelos_matriz_vector.clase_matriz_fact_LU import LUFactorization
from Historial.historial_matriz.historial_popup.historial_popup_ui import *
from GUI.gui_calc_matriz.interfaz_entrada.entrada_matriz_frame import *
from GUI.gui_calc_matriz.interfaz_entrada.entrada_vector_frame import *
from funciones_adicionales.convertir_formato_lista import *
from GUI.gui_calc_matriz.tablas_gui.modulo_tablas_entradas import TablasFrame


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
        self.label_matrix = ctk.CTkLabel(self.input_frame, text="Ingrese la matriz A:", font=("Arial", 17))
        self.label_matrix.pack(padx=5, pady=5)

        self.btn_importar_hist = ctk.CTkButton(self.input_frame, text="Importar", command=self.abrir_historial,
                                               font=("Georgia", 15))
        self.btn_importar_hist.pack(padx=10, pady=10)
        self.tooltip_importar = CTkToolTip(self.btn_importar_hist,
                                           message="Importar una matriz del historial")

        self.matriz_entrada = FrameEntradaMatriz(self.input_frame)
        self.matriz_entrada.pack(padx=5, pady=5)

        self.label_vector = ctk.CTkLabel(self.input_frame, text="Ingrese el vector b:", font=("Arial", 17))
        self.label_vector.pack(padx=5, pady=5)

        self.btn_importar_hist2 = ctk.CTkButton(self.input_frame, text="Importar", command=self.abrir_historial2,
                                                font=("Georgia", 15))
        self.btn_importar_hist2.pack(padx=10, pady=10)
        self.tooltip_importar2 = CTkToolTip(self.btn_importar_hist2,
                                            message="Importar un vector del historial")

        self.vector_entrada = FrameEntradaVector(self.input_frame)
        self.vector_entrada.pack(padx=5, pady=5)

        self.calculate_button = ctk.CTkButton(self.input_frame, text="Calcular", command=self.calculate_lu,
                                              font=("Georgia", 15))
        self.calculate_button.pack(padx=5, pady=10)

        # Widgets en el frame derecho (salida)
        self.output_label = ctk.CTkLabel(self.output_frame, text="Resultado",  font=("Arial", 17))
        self.output_label.pack(padx=5, pady=5)

        self.textbox_output = ctk.CTkTextbox(self.output_frame, width=450, height=200)
        self.textbox_output.pack(padx=5, pady=5)

        self.clear_button = ctk.CTkButton(self.output_frame, text="Limpiar", command=self.limpiar_entradas,
                                          font=("Georgia", 15))
        self.clear_button.pack(padx=5, pady=10)

        # Variables para los frames y tablas adicionales
        self.frame_tablas_izq = None
        self.frame_tablas_der = None
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
            CTkMessagebox(title="Error", message=f"Hubo un problema con las entradas: {str(e)}", icon="warning",
                          option_1="Entendido", button_hover_color="green", fade_in_duration=2)

    def limpiar_entradas(self):
        """Limpia los cuadros de texto de entrada y salida."""
        self.matriz_entrada.limpiar_entradas()
        self.vector_entrada.limpiar_entradas()
        self.textbox_output.delete("1.0", "end")
        self.frame_tablas_izq.limpiar_tablas()
        self.frame_tablas_der.limpiar_tablas()

    def crear_tablas(self):
        """Crea los frames con CTkTable para mostrar las matrices."""
        # tablas para la frame 1 que contiene los datos de entrada
        datos_tabla_entrada = self.lu_solver.original_matrix_A  # Usamos la matriz original
        datos_tabla_salida = convertir_a_array_columnas(self.lu_solver.original_vector_b)
        datos_tabla_reducida = self.lu_solver.L
        self.frame_tablas_izq = TablasFrame(self, tabla1=datos_tabla_entrada,
                                            tabla2=datos_tabla_salida, tabla3=datos_tabla_reducida,
                                            texto1="Matriz A:", texto2="Vector b:", texto3="Matriz L:")
        self.frame_tablas_izq.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        # tabla para matriz reduciad en frame 1
        datos_tabla_reducida = self.lu_solver.U
        datos_tabla_salida = convertir_a_array_columnas(self.lu_solver.solution_x)
        self.frame_tablas_der = TablasFrame(self, tabla1=datos_tabla_reducida, tabla2=datos_tabla_salida,
                                            texto1="Matriz U:", texto2="Vector x:")
        self.frame_tablas_der.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        #botón de guardado
        self.btn_guardar = ctk.CTkButton(self.frame_tablas_der.frame_entradas, text="Guardar",
                                         command=self.accionar_guardado)
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
