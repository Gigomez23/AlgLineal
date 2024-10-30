"""
Archivo: jauss_jorda_calc.py 1.8.0
Descripción: Este archivo contiene el diseño del frame para la calculadora de matrices
por método escalonado o de Gauss-Jordan.
"""
from ctkcomponents import *
from CTkToolTip import *
from models.clase_sistema_ecuaciones import *
from Historial.historial_popup.historial_popup_ui import *
from GUI.interfaz_entrada.entrada_matriz_frame import *
from GUI.tablas_gui.modulo_tablas_entradas import TablasFrame


class GaussJordanFrame(ctk.CTkFrame):
    """
    Frame para realizar la reducción de matrices usando el método de Gauss-Jordan.
    """

    def __init__(self, parent, historial):
        super().__init__(parent)
        self.gauss_jordan = CreadorDeEcuaciones()
        self.historial = historial
        self.importar = []

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
                                         text="Ingrese la matriz:")
        self.label_matriz.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.btn_importar_hist = ctk.CTkButton(self.entrada_frame, text="Importar", command=self.abrir_historial)
        self.btn_importar_hist.grid(row=2, column=0, padx=10, pady=10)
        self.tooltip_importar = CTkToolTip(self.btn_importar_hist,
                                           message="Importar una matriz del historial")

        # frame para entrada
        self.text_matriz = FrameEntradaMatriz(self.entrada_frame)
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
        self.tablas_entrada = None
        self.tablas_salidas = None

    def resolver_matriz(self):
        """Realiza la reducción de la matriz y muestra la solución."""
        matriz = self.text_matriz.obtener_matriz_como_array()

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
        self.tablas_entrada = TablasFrame(self, tabla1=self.gauss_jordan.matriz_original,
                                          tabla2=self.gauss_jordan.matriz, texto1="Matriz Ingresada:",
                                          texto2="Matriz Reducida:")
        self.tablas_entrada.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # tablas para la frame 2 que contiene los datos de salida
        datos_tabla_salida = self.gauss_jordan.solucion
        if not datos_tabla_salida:
            datos_vacios = [["El sistema es inconsistente"]]
            self.tablas_salidas = TablasFrame(self, tabla1=datos_vacios, texto1="Solución:")
            self.tablas_salidas.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        else:
            self.tablas_salidas = TablasFrame(self, tabla1=datos_tabla_salida, texto1="Solución:")
            self.tablas_salidas.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # botón de guardado
        self.btn_guardar = ctk.CTkButton(self.tablas_salidas.frame_entradas, text="Guardar",
                                         command=self.accionar_guardado)
        self.btn_guardar.pack(padx=10, pady=10)
        self.tooltip_guardar = CTkToolTip(self.btn_guardar,
                                          message="Guardar en historial")

    def mostrar_paso(self, texto):
        """Muestra un paso del proceso de reducción en el textbox de salida."""
        self.text_salida.insert("end", texto + "\n")

    def limpiar_entradas(self):
        """Limpia los campos de entrada, la salida y las tablas."""
        self.text_matriz.limpiar_entradas()
        self.text_salida.delete("1.0", "end")
        self.gauss_jordan.solucion = []  # Limpiar soluciones previas
        self.tablas_entrada.limpiar_tablas()
        self.tablas_salidas.limpiar_tablas()

    def accionar_guardado(self):
        self.guardar_en_historial(self.gauss_jordan.matriz_original, self.gauss_jordan.matriz,
                                  self.gauss_jordan.solucion)

    def guardar_en_historial(self, matriz_1, matriz_2, solucion):
        self.historial.agregar_problema(matriz1=matriz_1, matriz2=matriz_2, solucion=solucion, tipo="dos",
                                        clasificacion="matriz")
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
        self.text_matriz.importar_desde_historial(matriz)


# Uso del frame
if __name__ == "__main__":
    root = ctk.CTk()
    historial = []
    app_frame = GaussJordanFrame(root, historial)
    app_frame.pack(padx=10, pady=10, fill="both", expand=True)
    root.mainloop()
