"""
Archivo: determinante_frame.py 1.3.0
Descripción: Este archivo contiene la interfáz gráfica de la calculadora de determinantes.
"""
from CTkTable import CTkTable
from ctkcomponents import *
from CTkToolTip import *
from funciones_adicionales.convertir_formato_lista import lista_a_matriz
from models.operaciones_determinante import *
from Historial.historial_popup.historial_popup_ui import *
from GUI.interfaz_entrada.entrada_matriz_frame import *
from GUI.tablas_gui.modulo_tablas_entradas import TablasFrame


class DeterminanteFrame(ctk.CTkFrame):
    """
    Frame para realizar el cálculo de determinantes usando el método de Laplace.

    Args:
        parent (CTk): El widget padre que contendrá este frame.
    """
    def __init__(self, parent, historial):
        super().__init__(parent)
        self.operaciones_determinante = CreadorDeOperacionDeterminantes()
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
                                         text="Ingrese la matriz:")
        self.label_matriz.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        # botón importar
        self.btn_importar_hist = ctk.CTkButton(self.entrada_frame, text="Importar", command=self.abrir_historial)
        self.btn_importar_hist.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        self.tooltip_importar1 = CTkToolTip(self.btn_importar_hist,
                                            message="Importar una matriz del historial")

        # frame para entrada
        self.text_matriz = FrameEntradaMatriz(self.entrada_frame)
        self.text_matriz.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Botón para calcular
        self.btn_calcular = ctk.CTkButton(self.entrada_frame, text="Calcular", command=self.calcular_determinante)
        self.btn_calcular.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

        # Botón para limpiar
        self.btn_limpiar = ctk.CTkButton(self.resultado_frame, text="Limpiar", command=self.limpiar_entradas)
        self.btn_limpiar.grid(row=3, column=0, padx=10, pady=10)

        # Frame para resultados
        self.label_resultado = ctk.CTkLabel(self.resultado_frame, text="Resultado:")
        self.label_resultado.grid(row=0, column=0, padx=10, pady=10)

        self.text_salida = ctk.CTkTextbox(self.resultado_frame, width=400, height=150)
        self.text_salida.grid(row=1, column=0, padx=10, pady=10)

        self.tablas_entradas = None
        self.tablas_salidas = None

    def calcular_determinante(self):
        """Realiza el cálculo del determinante de la matriz introducida por el usuario."""
        matriz_text = self.text_matriz.obtener_matriz_como_array()

        # Pasar la matriz a la clase de OperacionesDeterminante
        self.operaciones_determinante.ingresar_datos(matriz_text)
        det = self.operaciones_determinante.calcular_determinante()

        # Mostrar el resultado
        self.text_salida.delete("1.0", "end")
        self.text_salida.insert("end", f"Determinante: {det}\n")
        self.text_salida.insert("end", self.operaciones_determinante.obtener_procedimiento())

        self.crear_tablas()

    def crear_tablas(self):
        """Crea los frames con CTkTable para mostrar las matrices."""
        # tablas para la frame 1 que contiene los datos de entrada
        datos_tabla_entrada = self.operaciones_determinante.matriz
        datos_tabla_salida = lista_a_matriz(self.operaciones_determinante.determinantes)

        self.tablas_entradas = TablasFrame(self, tabla1=datos_tabla_entrada, texto1="Matriz Ingresada:")
        self.tablas_entradas.grid(row=1, column=0, pady=10, sticky="nsew")
        self.tablas_salidas = TablasFrame(self, tabla1=datos_tabla_salida, texto1="Solución Det. A:")
        self.tablas_salidas.grid(row=1, column=1, pady=10, sticky="n")

        #botón de guardado
        self.btn_guardar = ctk.CTkButton(self.tablas_salidas.frame_entradas, text="Guardar",
                                         command=self.accionar_guardado)
        self.btn_guardar.pack(padx=10, pady=10)
        self.tooltip_guardar = CTkToolTip(self.btn_guardar,
                                            message="Guardar en historial")

    def limpiar_entradas(self):
        """Limpia los campos de entrada y salida."""
        self.text_matriz.limpiar_entradas()
        self.text_salida.delete("1.0", "end")
        self.tablas_entradas.limpiar_tablas()
        self.tablas_salidas.limpiar_tablas()

    def accionar_guardado(self):
        solucion = lista_a_matriz(self.operaciones_determinante.determinantes)
        self.guardar_en_historial(self.operaciones_determinante.matriz, solucion)

    def guardar_en_historial(self, matriz1, solucion):
        self.historial.agregar_problema(matriz1=matriz1, solucion=solucion, tipo="uno", clasificacion="matriz")
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
        print(matriz)


if __name__ == "__main__":
    root = ctk.CTk()
    historial = []
    app_frame = DeterminanteFrame(root, historial)
    app_frame.pack(padx=10, pady=10, fill="both", expand=True)
    root.mainloop()