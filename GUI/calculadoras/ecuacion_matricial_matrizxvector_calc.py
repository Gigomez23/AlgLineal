"""
Archivo: ecuacion_matricial_matrizxvector_calc.py 2.4.5
Descripción: Archivo contiene la interfaz grafica para la ecuacion matricial
"""
from ctkcomponents import *
from CTkMessagebox import CTkMessagebox
from CTkTable import CTkTable
from CTkToolTip import *
from models.clase_matriz_operaciones import *
from funciones_adicionales.convertir_formato_lista import *
from Historial.historial_popup.historial_popup_ui import *
from GUI.interfaz_entrada.entrada_matriz_frame import *
from GUI.interfaz_entrada.entrada_vector_frame import *
# todo: fix la salida del vector en el texbox


class MultiplicacionMatricesFrame(ctk.CTkFrame):
    def __init__(self, parent, historial):
        super().__init__(parent)
        self.matriz_operaciones = CreadorDeOperaciones()
        self.historial = historial
        self.matriz_entrada = []
        self.vector_entrada = []
        self.matriz_salida = []

        # Crear el frame izquierdo para las entradas y botones
        self.frame_izquierdo = ctk.CTkFrame(self)
        self.frame_izquierdo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Crear el frame derecho para la salida
        self.frame_derecho = ctk.CTkFrame(self)
        self.frame_derecho.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Configurar pesos para que los frames se ajusten al redimensionar
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Frame Izquierdo: Entradas ---
        # Entradas para la matriz A
        self.label_matriz_A = ctk.CTkLabel(self.frame_izquierdo,
                                           text="Matriz A (filas separadas por enter, "
                                                "valores separados por espacios):")
        self.label_matriz_A.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        # boton para importar en primera entrada
        self.btn_importar_hist_entrada1 = ctk.CTkButton(self.frame_izquierdo, text="Importar",
                                                        command=self.abrir_historial1)
        self.btn_importar_hist_entrada1.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        # tooltip de importar
        self.tooltip_importar1 = CTkToolTip(self.btn_importar_hist_entrada1,
                                            message="Importar una matriz del historial")

        # textbox para primera entrada
        self.text_matriz_A = FrameEntradaMatriz(self.frame_izquierdo)
        self.text_matriz_A.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        # Entradas para la matriz b
        self.label_matriz_b = ctk.CTkLabel(self.frame_izquierdo,
                                           text="Vector/matriz b (valores separados por espacios):")
        self.label_matriz_b.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

        # botón para importar en segunda entrada
        self.btn_importar_hist_entrada2 = ctk.CTkButton(self.frame_izquierdo, text="Importar",
                                                        command=self.abrir_historial2)
        self.btn_importar_hist_entrada2.grid(row=5, column=0, padx=10, pady=10, columnspan=2)

        # tooltip para botón de importar
        self.tooltip_importar2 = CTkToolTip(self.btn_importar_hist_entrada2,
                                            message="Importar un vector del historial")

        self.text_matriz_b = FrameEntradaVector(self.frame_izquierdo)
        self.text_matriz_b.grid(row=6, column=0, padx=10, pady=10, columnspan=2)

        # Botones debajo de las entradas
        self.btn_calcular = ctk.CTkButton(self.frame_izquierdo, text="Calcular Ax = b",
                                          command=self.calcular_multiplicacion)
        self.btn_calcular.grid(row=7, column=0, padx=10, pady=10)

        self.tooltip_calcular = CTkToolTip(self.btn_calcular,
                                            message="Encontrar solución")

        self.btn_mostrar_pasos = ctk.CTkButton(self.frame_izquierdo, text="Mostrar Resultado con Pasos",
                                               command=self.mostrar_resultado_con_pasos)
        self.btn_mostrar_pasos.grid(row=7, column=1, padx=10, pady=10)
        self.tooltip_pasos = CTkToolTip(self.btn_mostrar_pasos,
                                            message="Mostrar solución con pasos. ")

        # --- Frame Derecho: Salida y Botón de Limpiar ---
        self.label_salida = ctk.CTkLabel(self.frame_derecho, text="Solución:")
        self.label_salida.grid(row=0, column=0, padx=10, pady=10)

        self.text_salida_frame = ctk.CTkFrame(self.frame_derecho)
        self.text_salida_frame.grid(row=1, column=0, padx=10, pady=10)

        self.text_salida = ctk.CTkTextbox(self.text_salida_frame, width=400, height=150, wrap="none")
        self.text_salida.pack(side="left", fill="both", expand=True)

        # Scrollbar para el text_salida
        self.scrollbar = ctk.CTkScrollbar(self.text_salida_frame, command=self.text_salida.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.text_salida.configure(yscrollcommand=self.scrollbar.set)

        # Botón de limpiar debajo del textbox de salida
        self.btn_limpiar = ctk.CTkButton(self.frame_derecho, text="Limpiar", command=self.clear_inputs)
        self.btn_limpiar.grid(row=2, column=0, padx=10, pady=10)

        # Variables para los frames y tablas adicionales
        self.frame_matriz1 = None
        self.frame_matriz2 = None
        self.tabla_matriz = None
        self.tabla_matriz2 = None
        self.tabla_reducida = None
        self.tabla_entrada = None
        self.tabla_salida = None

    def calcular_multiplicacion(self):
        """Calcula la multiplicación Ax = b y muestra el resultado sin pasos"""
        # Obtener el contenido de las entradas de texto
        matriz_A_text = self.text_matriz_A.obtener_matriz_como_array()
        matriz_b_text = self.text_matriz_b.obtener_matriz_como_array()

        # Verificar si alguno de los campos de entrada está vacío
        if not matriz_A_text or not matriz_b_text:
            CTkMessagebox(title="Error de entrada", message="Todos los campos deben estar llenos.", icon="warning",
                          option_1="Entendido", button_hover_color="green", fade_in_duration=2)
            return

        try:
            # Obtener la matriz A y calcular filas y columnas automáticamente
            matriz_A = matriz_A_text

            # Verificar si las filas de la matriz A tienen el mismo número de columnas
            columnas_A = len(matriz_A[0]) if matriz_A else 0
            for fila in matriz_A:
                if len(fila) != columnas_A:
                    CTkMessagebox(title="Error de formato",
                                  message="Todas las filas de la matriz A deben tener el mismo número de columnas.",
                                  icon="warning",
                                  option_1="Entendido", button_hover_color="green", fade_in_duration=2)
                    return

            self.matriz_entrada = matriz_A
            filas_A = len(matriz_A)

            self.vector_entrada = matriz_b_text
            matriz_b = matriz_b_text
            filas_b = len(matriz_b)

            if columnas_A != filas_b:
                CTkMessagebox(title="Error de formato", message=f"No se puede multiplicar A de tamaño "
                                                                f"({filas_A}x{columnas_A}) con b de tamaño ({filas_b})."
                                                                f"\nEl número de columnas de A debe ser igual al número "
                                                                f"de filas de b.",
                              icon="warning", option_1="Entendido", button_hover_color="green", fade_in_duration=2)
                return

        except ValueError as e:
            # Error si se intenta ingresar letras en lugar de números
            CTkMessagebox(title="Error de formato", message="Por favor, ingresa solo números válidos (sin letras).",
                          icon="warning", option_1="Entendido", button_hover_color="green", fade_in_duration=2)
            return

        except ZeroDivisionError:
            # Error si se intenta dividir por 0
            CTkMessagebox(title="Error de división", message="No se puede dividir por cero.", icon="warning",
                          option_1="Entendido", button_hover_color="green", fade_in_duration=2)
            return

        # Si está correcto, proceder con la operación
        self.matriz_operaciones.A = matriz_A
        self.matriz_operaciones.b = convertir_a_matriz_de_fracciones(matriz_b)
        self.matriz_operaciones.filas_A = filas_A
        self.matriz_operaciones.columnas_A = columnas_A
        self.matriz_operaciones.filas_b = filas_b

        self.text_salida.delete("1.0", "end")
        self.matriz_operaciones.imprimir_matrices(self.text_salida)
        self.matriz_operaciones.imprimir_solucion(self.text_salida, mostrar_pasos=False)

        # mostramos tablas
        self.crear_tablas()

    def mostrar_resultado_con_pasos(self):
        """Muestra el resultado de la multiplicación y los pasos"""
        # Obtener el contenido de las entradas de texto
        matriz_A_text = self.text_matriz_A.obtener_matriz_como_array()
        matriz_b_text = self.text_matriz_b.obtener_matriz_como_array()

        # Verificar si alguno de los campos de entrada está vacío
        if not matriz_A_text or not matriz_b_text:
            CTkMessagebox(title="Error de entrada", message="Todos los campos deben estar llenos.", icon="warning",
                          option_1="Entendido", button_hover_color="green", fade_in_duration=2)
            return

        try:
            # Obtener la matriz A y calcular filas y columnas automáticamente
            matriz_A = matriz_A_text

            self.matriz_entrada = matriz_A
            filas_A = len(matriz_A)
            columnas_A = len(matriz_A[0]) if filas_A > 0 else 0

            self.vector_entrada = matriz_b_text
            matriz_b = matriz_b_text
            filas_b = len(matriz_b)

            if columnas_A != filas_b:
                CTkMessagebox(title="Error de Dimensiones", message=f"No se puede multiplicar A de tamaño "
                                                                    f"({filas_A}x{columnas_A}) con b de tamaño ({filas_b})."
                                                                    f"\nEl número de columnas de A debe ser "
                                                                    f"igual al número de filas de b.",
                              icon="warning", option_1="Entendido", button_hover_color="green", fade_in_duration=2)
                return

        except ValueError as e:
            # Error si se intenta ingresar letras en lugar de números
            CTkMessagebox(title="Error de formato", message="Por favor, ingresa solo números válidos (sin letras).",
                          icon="warning", option_1="Entendido", button_hover_color="green", fade_in_duration=2)
            return

        except ZeroDivisionError:
            # Error si se intenta dividir por 0
            CTkMessagebox(title="Error de división", message="No se puede dividir por cero.", icon="warning",
                          option_1="Entendido", button_hover_color="green", fade_in_duration=2)
            return

        # Si está correcto, proceder con la operación
        self.matriz_operaciones.A = matriz_A
        self.matriz_operaciones.b = convertir_a_matriz_de_fracciones(matriz_b)
        self.matriz_operaciones.filas_A = filas_A
        self.matriz_operaciones.columnas_A = columnas_A
        self.matriz_operaciones.filas_b = filas_b

        self.text_salida.delete("1.0", "end")
        self.matriz_operaciones.imprimir_matrices(self.text_salida)
        self.matriz_operaciones.imprimir_solucion(self.text_salida, mostrar_pasos=True)

        # mostramos tablas
        self.crear_tablas()

    def crear_tablas(self):
        """Crea los frames con CTkTable para mostrar las matrices."""
        if self.frame_matriz1 or self.frame_matriz2:
            self.limpiar_tablas()

        # Frame para la primera serie de tablas
        self.frame_matriz1 = ctk.CTkFrame(self)
        self.frame_matriz1.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        # Frame para la serie de tablas de solucion y el boton de guardar
        self.frame_matriz2 = ctk.CTkFrame(self)
        self.frame_matriz2.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        # labels para frames
        self.tabla_matriz1 = ctk.CTkLabel(self.frame_matriz1, text="Matriz Ingresada:")
        self.tabla_matriz1.pack(padx=10, pady=10)
        self.tabla_matriz2 = ctk.CTkLabel(self.frame_matriz2, text="Solución:")
        self.tabla_matriz2.pack(padx=10, pady=10)

        # tablas para la frame 1 que contiene los datos de entrada
        # tabla para la matriz original
        datos_tabla_matriz = self.matriz_entrada
        self.tabla_matriz = CTkTable(self.frame_matriz1, values=datos_tabla_matriz)
        self.tabla_matriz.pack(padx=10, pady=10)

        # label para vector ingresado
        self.label_vector_ingresada = ctk.CTkLabel(self.frame_matriz1, text="Vector Ingresado:")
        self.label_vector_ingresada.pack(padx=10, pady=10)

        # tabla para el vector ingresado
        datos_tabla_entrada = self.vector_entrada
        self.tabla_entrada = CTkTable(self.frame_matriz1, values=datos_tabla_entrada)
        self.tabla_entrada.pack(padx=10, pady=10)

        # tablas para la frame 2 que contiene los datos de salida
        datos_tabla_salida = lista_a_matriz(self.matriz_operaciones.solucion)
        self.tabla_salida = CTkTable(self.frame_matriz2, values=datos_tabla_salida)
        self.tabla_salida.pack(padx=10, pady=10)

        #botón de guardado
        self.btn_guardar = ctk.CTkButton(self.frame_matriz2, text="Guardar",
                                         command=self.accionar_guardado_en_historial)
        self.btn_guardar.pack(padx=10, pady=10)
        self.tooltip_guardar = CTkToolTip(self.btn_importar_hist_entrada2,
                                            message="Guardar en historial")

    def limpiar_tablas(self):
        """Elimina los frames con las tablas y reinicia las soluciones."""
        # Limpiar la lista de soluciones
        self.matriz_operaciones.solucion = []

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

    def clear_inputs(self):
        """Limpia todas las entradas y la salida"""
        # self.entry_nombre.delete(0, 'end')
        self.text_matriz_A.limpiar_entradas()
        self.text_matriz_b.limpiar_entradas()
        self.text_salida.delete("1.0", "end")
        self.limpiar_tablas()

    def accionar_guardado_en_historial(self):
        datos_tabla_salida = lista_a_matriz(self.matriz_operaciones.solucion)
        self.guardar_en_historial(self.matriz_entrada, self.vector_entrada, datos_tabla_salida)

    def guardar_en_historial(self, matriz1, matriz2, solucion):
        self.historial.agregar_problema(matriz1=matriz1,matriz2=matriz2, solucion=solucion, tipo='dos',
                                        clasificacion="mixto")
        CTkNotification(master=self, state="info",
                        message=f"{self.historial.problemas[-1]['nombre']} ha sido guardado exitosamente!",
                        side="right_bottom")

    def abrir_historial1(self):
        """Abre el pop-up del historial."""
        historial_popup = HistorialPopup(self, self.historial, self.historial)
        historial_popup.grab_set()  # Foco en el pop-up

        # Obtener la matriz importada después de cerrar el popup
        self.wait_window(historial_popup)  # Espera hasta que se cierre el popup
        self.cargar_matriz_importada(historial_popup)

    def cargar_matriz_importada(self, historial_popup):
        """Carga la matriz importada al Textbox del FrameEntradaMatriz."""
        matriz = historial_popup.retornar_matriz_importada()
        self.text_matriz_A.importar_desde_historial(matriz)

    def abrir_historial2(self):
        """Abre el pop-up del historial."""
        historial_popup = HistorialPopup(self, self.historial, self.historial)
        historial_popup.grab_set()  # Foco en el pop-up

        # Obtener la matriz importada después de cerrar el popup
        self.wait_window(historial_popup)  # Espera hasta que se cierre el popup
        self.cargar_matriz_importada2(historial_popup)

    def cargar_matriz_importada2(self, historial_popup):
        """Carga la matriz importada al Textbox del FrameEntradaMatriz."""
        matriz = historial_popup.retornar_matriz_importada()
        self.text_matriz_b.importar_desde_historial(matriz)


if __name__ == "__main__":
    root = ctk.CTk()
    historial = []
    app_frame = MultiplicacionMatricesFrame(root, historial)
    app_frame.pack(padx=10, pady=10, fill="both", expand=True)
    root.mainloop()