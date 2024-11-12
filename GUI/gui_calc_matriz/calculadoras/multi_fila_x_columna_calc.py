"""
Archivo: multi_fila_x_columna_calc.py 2.2.3
Descripcion: Archivo que contiene el diseño del frame para operaciones de vector x vector.
"""
from CTkToolTip import *
from ctkcomponents import *
from models.modelos_matriz_vector.clase_muli_vectores import VectorMultiplicacionCalculadora
from GUI.gui_calc_matriz.interfaz_entrada.entrada_vector_frame import *
from funciones_adicionales.convertir_formato_lista import *
from GUI.gui_calc_matriz.tablas_gui.modulo_tablas_entradas import TablasFrame
from Historial.historial_matriz.historial_popup.historial_popup_ui import *


class VectorMultiplicacionFrame(ctk.CTkFrame):
    """
    Frame para la multiplicación de un vector fila por un vector columna utilizando customtkinter.

    Args:
        parent (CTkWidget): El widget padre que contendrá este frame.
    """

    def __init__(self, parent, historial):
        super().__init__(parent)
        self.historial = historial
        self.calculadora = VectorMultiplicacionCalculadora()

        # Frame para entrada
        self.entrada_frame = ctk.CTkFrame(self)
        self.entrada_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame para resultados
        self.resultado_frame = ctk.CTkFrame(self)
        self.resultado_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Configuración del frame
        self.label_fila = ctk.CTkLabel(self.entrada_frame, text="Introduce el vector fila:")
        self.label_fila.grid(row=0, column=0, padx=10, pady=10)

        self.btn_importar_hist_fila = ctk.CTkButton(self.entrada_frame, text="Importar", command=self.abrir_historial)
        self.btn_importar_hist_fila.grid(row=1, column=0, padx=10, pady=10)
        self.tooltip_importar = CTkToolTip(self.btn_importar_hist_fila,
                                           message="Importar un vector fila del historial")

        self.entry_fila = FrameEntradaVector(self.entrada_frame)
        self.entry_fila.grid(row=2, column=0, padx=10, pady=10)

        self.label_columna = ctk.CTkLabel(self.entrada_frame, text="Introduce el vector columna:")
        self.label_columna.grid(row=0, column=1, padx=10, pady=10)

        self.btn_importar_hist_columna = ctk.CTkButton(self.entrada_frame, text="Importar",
                                                       command=self.abrir_historial2)
        self.btn_importar_hist_columna.grid(row=1, column=1, padx=10, pady=10)
        self.tooltip_importar = CTkToolTip(self.btn_importar_hist_columna,
                                           message="Importar un vector columna del historial")

        self.entry_columna = FrameEntradaVector(self.entrada_frame)
        self.entry_columna.grid(row=2, column=1, padx=10, pady=10)

        self.button_calculate = ctk.CTkButton(self.entrada_frame, text="Calcular Multiplicación",
                                              command=self.calcular_multiplicacion)
        self.button_calculate.grid(row=3, column=0, padx=10, pady=10, sticky="n", columnspan=2)

        self.result_text = ctk.CTkTextbox(self.resultado_frame, height=200, width=300)
        self.result_text.pack(pady=10, padx=10)
        self.result_text.configure(state="disabled")  # Hacer que el textbox sea de solo lectura

        self.button_clear = ctk.CTkButton(self.resultado_frame, text="Limpiar", command=self.limpiar_entradas)
        self.button_clear.pack(pady=10)

        self.tablas_entrada = None
        self.tablas_salida = None

    def calcular_multiplicacion(self):
        """
        Función que obtiene los vectores de entrada, realiza el cálculo y muestra el resultado.
        """
        try:
            # Obtener valores de entrada
            fila_str = self.entry_fila.obtener_matriz_como_array()
            columna_str = self.entry_columna.obtener_matriz_como_array()

            # Parsear vectores como fracciones
            fila = a_lista_simple(fila_str)
            columna = a_lista_simple(columna_str)

            # Configurar vectores en la calculadora
            self.calculadora.set_vectores(fila, columna)
            proceso_y_resultado = self.calculadora.calcular()

            # Mostrar el proceso y el resultado
            self.result_text.configure(state="normal")
            self.result_text.delete(1.0, ctk.END)
            self.result_text.insert(ctk.END, f"Proceso de la multiplicación:\n{proceso_y_resultado}")
            self.result_text.configure(state="disabled")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error en el cálculo: {e}",
                          icon="warning", option_1="Entendido", button_hover_color="green", fade_in_duration=2)
        self.crear_tablas()

    def crear_tablas(self):
        fila = [self.calculadora.vector_fila]
        vector_fila = fila
        columna = self.calculadora.vector_columna
        vector_columna = convertir_a_array_columnas(columna)
        self.tablas_entrada = TablasFrame(self, tabla1=vector_fila,
                                          tabla2=vector_columna, texto1="Vector Fila:",
                                          texto2="Vector Columna")
        self.tablas_entrada.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        resultado = [[self.calculadora.resultado]]
        self.tablas_salida = TablasFrame(self, tabla1=resultado, texto1="Resultado:")
        self.tablas_salida.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # botón de guardado
        self.btn_guardar = ctk.CTkButton(self.tablas_salida.frame_entradas, text="Guardar",
                                         command=self.accionar_guardado)
        self.btn_guardar.pack(padx=10, pady=10)
        self.tooltip_guardar = CTkToolTip(self.btn_guardar,
                                          message="Guardar en historial")

    def limpiar_entradas(self):
        """Limpia los campos de entrada y el texto de salida."""
        self.entry_fila.limpiar_entradas()
        self.entry_columna.limpiar_entradas()
        self.result_text.configure(state="normal")
        self.result_text.delete(1.0, ctk.END)
        self.result_text.configure(state="disabled")
        self.tablas_entrada.limpiar_tablas()
        self.tablas_salida.limpiar_tablas()

    def accionar_guardado(self):
        fila = [self.calculadora.vector_fila]
        vector_fila = fila
        columna = self.calculadora.vector_columna
        vector_columna = convertir_a_array_columnas(columna)
        resultado = [[self.calculadora.resultado]]
        self.guardar_en_historial(vector_fila, vector_columna,
                                  resultado)

    def guardar_en_historial(self, matriz_1, matriz_2, solucion):
        self.historial.agregar_problema(matriz1=matriz_1, matriz2=matriz_2, solucion=solucion, tipo="dos",
                                        clasificacion="vector")
        CTkNotification(master=self, state="info",
                        message=f"{self.historial.problemas[-1]['nombre']} ha sido guardado exitosamente!",
                        side="right_bottom")

    def abrir_historial(self):
        """Abre el pop-up del historial"""
        historial_popup = HistorialPopup(self, self.historial, self.historial)
        historial_popup.grab_set()  # Esperar hasta que se cierre el popup

        # Obtener la matriz importada después de cerrar el popup
        self.wait_window(historial_popup)  # Espera hasta que se cierre el popup
        self.cargar_vector_fila_importada(historial_popup)

    def cargar_vector_fila_importada(self, historial_popup):
        """Carga la matriz importada al Textbox del FrameEntradaMatriz."""
        matriz_importada = historial_popup.retornar_matriz_importada()
        if len(matriz_importada[0]) > 1:
            matriz = convertir_a_vector_columnar(matriz_importada)
            self.entry_fila.importar_desde_historial(matriz)
        else:
            CTkMessagebox(title="Error", message=f"No selecciono un vector fila, por favor ingrese un vector fila.",
                          icon="warning", option_1="Entendido", button_hover_color="green", fade_in_duration=2)

    def abrir_historial2(self):
        """Abre el pop-up del historial"""
        historial_popup = HistorialPopup(self, self.historial, self.historial)
        historial_popup.grab_set()  # Esperar hasta que se cierre el popup

        # Obtener la matriz importada después de cerrar el popup
        self.wait_window(historial_popup)  # Espera hasta que se cierre el popup
        self.cargar_vector_columna_importada(historial_popup)

    def cargar_vector_columna_importada(self, historial_popup):
        """Carga la matriz importada al Textbox del FrameEntradaMatriz."""
        matriz = historial_popup.retornar_matriz_importada()
        self.entry_columna.importar_desde_historial(matriz)


# Uso en una aplicación más grande
if __name__ == "__main__":
    class AplicacionPrincipal(ctk.CTk):
        """
        Aplicación principal que contiene el frame de multiplicación de vectores.
        """
        def __init__(self):
            super().__init__()

            historial = []
            self.title("Multiplicación de Vectores Fila y Columna")
            self.geometry("600x600")

            # Frame de Multiplicación de Vectores
            self.vector_multiplicacion_frame = VectorMultiplicacionFrame(self, historial)
            self.vector_multiplicacion_frame.pack(padx=20, pady=20, fill="both", expand=True)


    app = AplicacionPrincipal()
    app.mainloop()

