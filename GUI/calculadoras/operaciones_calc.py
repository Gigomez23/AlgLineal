"""
Archivo: operaciones_calc.py 2.3.1
Descripción: Este archivo contiene la interfáz gráfica de la calculadora de operaciones de matrices.
"""
from ctkcomponents import *
from CTkTable import *
from CTkToolTip import *
from models.clase_matriz_op_ari import *
from Historial.historial_popup.historial_popup_ui import *
from GUI.interfaz_entrada.entrada_matriz_frame import *
from GUI.interfaz_entrada.entrada_matriz_esclava_identica import FrameEsclavoMatriz
from GUI.tablas_gui.modulo_tablas_entradas import TablasFrame


class OperacionesAritmeticasMatrizFrame(ctk.CTkFrame):
    def __init__(self, parent, historial):
        super().__init__(parent)
        self.historial_frame = None  # Placeholder para el frame del historial
        self.historial = historial
        self.operaciones = CreadorDeMatricesAritmeticas()
        self.operacion_seleccionada = ctk.StringVar(value="sumar")
        self.matriz_entrada1 = []
        self.matriz_entrada2 = []
        self.matriz_solucion = []

        # Frame para entradas
        self.entrada_frame = ctk.CTkFrame(self)
        self.entrada_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame para resultados
        self.resultado_frame = ctk.CTkFrame(self)
        self.resultado_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Componentes del frame de entrada
        self.label_matriz1 = ctk.CTkLabel(self.entrada_frame, text="Ingrese la primera matriz:")
        self.label_matriz1.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.btn_importar_hist_entrada1 = ctk.CTkButton(self.entrada_frame, text="Importar",
                                                        command=self.abrir_historial1)
        self.btn_importar_hist_entrada1.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
        self.tooltip_importar1 = CTkToolTip(self.btn_importar_hist_entrada1,
                                            message="Importar una matriz del historial")

        # frame para entrada
        self.text_matriz1 = FrameEntradaMatriz(self.entrada_frame)
        self.text_matriz1.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        self.label_matriz2 = ctk.CTkLabel(self.entrada_frame, text="Ingrese la segunda matriz:")
        self.label_matriz2.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

        self.btn_importar_hist_entrada2 = ctk.CTkButton(self.entrada_frame, text="Importar",
                                                        command=self.abrir_historial2)
        self.btn_importar_hist_entrada2.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
        self.tooltip_importar2 = CTkToolTip(self.btn_importar_hist_entrada2,
                                            message="Importar una matriz del historial")

        self.text_matriz2 = FrameEsclavoMatriz(self.entrada_frame, self.text_matriz1)
        self.text_matriz2.grid(row=6, column=0, padx=10, pady=10, columnspan=2)

        # Radio buttons para seleccionar operación
        self.radio_suma = ctk.CTkRadioButton(self.entrada_frame, text="Sumar", variable=self.operacion_seleccionada,
                                             value="sumar")
        self.radio_suma.grid(row=7, column=0, padx=10, pady=10)

        self.radio_resta = ctk.CTkRadioButton(self.entrada_frame, text="Restar", variable=self.operacion_seleccionada,
                                              value="restar")
        self.radio_resta.grid(row=7, column=1, padx=10, pady=10)

        self.radio_multiplicar = ctk.CTkRadioButton(self.entrada_frame, text="Multiplicar",
                                                    variable=self.operacion_seleccionada, value="multiplicar")
        self.radio_multiplicar.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # Botón para calcular
        self.btn_calcular = ctk.CTkButton(self.entrada_frame, text="Calcular", command=self.calcular_operacion)
        self.btn_calcular.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        # Frame para resultados
        self.label_salida = ctk.CTkLabel(self.resultado_frame, text="Resultado y Procedimiento:")
        self.label_salida.grid(row=0, column=0, padx=10, pady=10)

        self.text_salida_frame = ctk.CTkFrame(self.resultado_frame)
        self.text_salida_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.text_salida = ctk.CTkTextbox(self.text_salida_frame, width=400, height=150, wrap="none")
        self.text_salida.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.text_salida_frame, command=self.text_salida.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.text_salida.configure(yscrollcommand=self.scrollbar.set)

        self.btn_limpiar = ctk.CTkButton(self.resultado_frame, text="Limpiar", command=self.limpiar_entradas)
        self.btn_limpiar.grid(row=2, column=0, padx=10, pady=10)

        # Frames para las tablas vacías
        self.tabla_frame1 = None
        self.tabla_frame2 = None

        # # Aquí enlazamos el evento en este FramePadre
        # self.text_matriz1.bind("<<EventoPersonalizado>>", self.propagar_evento)

    # def propagar_evento(self):
    #     # Propagar manualmente el evento hacia FrameEsclavoMatriz
    #     self.text_matriz2.event_generate("<<EventoPersonalizado>>")
    #     print('Evento capturado en Calculadora')

    def obtener_matrices(self, operacion):
        """Función que extrae y valida las matrices según la operación seleccionada.

        :param operacion: str - La operación a realizar ("sumar", "restar", "multiplicar")
        :return: bool
        """
        matriz1_text = self.text_matriz1.obtener_matriz_como_array()
        matriz2_text = self.text_matriz2.obtener_matriz_como_array()

        try:
            self.operaciones.matriz1 = matriz1_text
            self.operaciones.matriz2 = matriz2_text

            self.matriz_entrada1 = self.operaciones.matriz1
            self.matriz_entrada2 = self.operaciones.matriz2

            if operacion in ["sumar", "restar"]:
                if not self.validar_dimensiones_para_operaciones():
                    raise ValueError("Las matrices deben tener las mismas dimensiones para suma/resta.")
            elif operacion == "multiplicar":
                if not self.validar_dimensiones_para_multiplicacion():
                    raise ValueError("El número de columnas de la Matriz 1 debe coincidir con "
                                     "el número de filas de la Matriz 2 para multiplicación.")
        except ValueError as e:
            CTkMessagebox(title="Error de formato", message=f"Error: {str(e)}",
                          icon="warning", option_1="Entendido", button_hover_color="green", fade_in_duration=2)
            return False

        return True

    def validar_dimensiones_para_operaciones(self):
        """Función que valida las dimensiones para las operaciones de sumar y restar
        :return
            bool
        """
        if len(self.operaciones.matriz1) != len(self.operaciones.matriz2):
            return False
        for fila1, fila2 in zip(self.operaciones.matriz1, self.operaciones.matriz2):
            if len(fila1) != len(fila2):
                return False
        return True

    def validar_dimensiones_para_multiplicacion(self):
        """Función que valida las dimensiones para la multiplicación
        :return
            bool
        """
        if not self.operaciones.matriz1 or not self.operaciones.matriz2:
            return False
        return len(self.operaciones.matriz1[0]) == len(self.operaciones.matriz2)

    def calcular_operacion(self):
        """Función que selecciona y realiza el cálculo según la operación seleccionada."""
        matriz1_text = self.text_matriz1.obtener_matriz_como_array()
        matriz2_text = self.text_matriz2.obtener_matriz_como_array()

        # Verificar si los campos están vacíos
        if not matriz1_text or not matriz2_text:
            CTkMessagebox(title="Advertencia", message="Por favor, ingrese ambas matrices antes de calcular.",
                          icon="warning", option_1="Entendido", button_hover_color="green", fade_in_duration=2)
            return

        operacion = self.operacion_seleccionada.get()

        if self.obtener_matrices(operacion):
            try:
                if operacion == "sumar":
                    self.operaciones.suma_matrices()
                elif operacion == "restar":
                    self.operaciones.resta_matrices()
                elif operacion == "multiplicar":
                    self.operaciones.multiplicar_matrices()

                self.mostrar_resultado()
                self.mostrar_tablas()  # Muestra las tablas vacías
            except Exception as e:
                CTkMessagebox(title="Error en la operación", message=f"Ocurrió un error durante la operación: {str(e)}",
                              icon="warning", option_1="Entendido", button_hover_color="red", fade_in_duration=2)

    def mostrar_resultado(self):
        """Función muestra los resultados en el textbox de salida."""
        resultado_formato = self.operaciones.formato_matriz(self.operaciones.resultado)
        self.matriz_solucion = self.operaciones.resultado
        procedimiento = self.operaciones.procedimiento
        self.text_salida.delete("1.0", "end")
        self.text_salida.insert("end", f"{procedimiento}\n\nResultado:\n{resultado_formato}")

    def mostrar_tablas(self):
        """Muestra las tablas vacías cuando se presiona el botón 'Calcular'."""
        # Tablas del frame1 que contienen los datos de entradas mostradas en una tabla cTkTable
        datos_tabla_1 = self.text_matriz1.obtener_matriz_como_array()
        datos_tabla_2 = self.text_matriz2.obtener_matriz_como_array()
        self.tabla_frame1 = TablasFrame(self, tabla1=datos_tabla_1, tabla2=datos_tabla_2,
                                        texto1="Matriz Ingresada 1:", texto2="Matriz Ingresada 2:")
        self.tabla_frame1.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        datos_tabla_solucion = self.operaciones.resultado
        self.tabla_frame2 = TablasFrame(self, tabla1=datos_tabla_solucion, texto1="Solución:")
        self.tabla_frame2.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        # boton para guardar
        self.btn_guardar = ctk.CTkButton(self.tabla_frame2.frame_entradas, text="Guardar",
                                         command=self.accionar_guardado_en_historial)
        self.btn_guardar.pack(padx=10, pady=10)
        self.tooltip_guardar = CTkToolTip(self.btn_guardar,
                                          message="Guardar en historial")

    def limpiar_entradas(self):
        """Limpia las entradas y elimina las tablas."""
        # Limpiar los campos de entrada
        self.limpiar_y_actualizar()
        self.text_salida.delete("1.0", "end")
        self.tabla_frame1.limpiar_tablas()
        self.tabla_frame2.limpiar_tablas()

    def limpiar_y_actualizar(self):
        """Limpia las entradas y actualiza ambos marcos."""
        self.text_matriz1.limpiar_entradas()
        self.text_matriz2.limpiar_entradas()

    def accionar_guardado_en_historial(self):
        self.guardar_en_historial(self.matriz_entrada1, self.matriz_entrada2, self.matriz_solucion)

    def guardar_en_historial(self, matriz1, matriz2, solucion):
        self.historial.agregar_problema(matriz1=matriz1, matriz2=matriz2, solucion=solucion,
                                        tipo='dos', clasificacion="matriz")
        CTkNotification(master=self, state="info",
                        message=f"{self.historial.problemas[-1]['nombre']} ha sido guardado exitosamente!",
                        side="right_bottom")

    def abrir_historial1(self):
        """Abre el pop-up del historial"""
        historial_popup = HistorialPopup(self, self.historial, self.historial)
        historial_popup.grab_set()  # Esperar hasta que se cierre el popup

        # Obtener la matriz importada después de cerrar el popup
        self.wait_window(historial_popup)  # Espera hasta que se cierre el popup
        self.cargar_matriz_importada1(historial_popup)

    def cargar_matriz_importada1(self, historial_popup):
        """Carga la matriz importada al Textbox del FrameEntradaMatriz."""
        matriz = historial_popup.retornar_matriz_importada()
        self.text_matriz1.importar_desde_historial(matriz)
        print(matriz)

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
        self.text_matriz2.importar_desde_historial(matriz)
        print(matriz)


if __name__ == "__main__":
    root = ctk.CTk()
    historial = []
    app_frame = OperacionesAritmeticasMatrizFrame(root, historial)
    app_frame.pack(padx=10, pady=10, fill="both", expand=True)
    root.mainloop()
