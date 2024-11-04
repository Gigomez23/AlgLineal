# Archivo: cramer_frame.py
from ctkcomponents import *
from CTkToolTip import *
from Historial.historial_matriz.historial_popup.historial_popup_ui import *
from models.operacion_cramer import CreadorDeCramer
from GUI.gui_calc_matriz.interfaz_entrada.entrada_matriz_frame import *
from funciones_adicionales.convertir_formato_lista import *
from GUI.gui_calc_matriz.tablas_gui.modulo_tablas_entradas import TablasFrame


class CramerFrame(ctk.CTkFrame):
    """
    Frame para resolver un sistema de ecuaciones lineales usando la Regla de Cramer.

    Args:
        parent (CTk): El widget padre que contendrá este frame.
    """
    def __init__(self, parent, historial):
        super().__init__(parent)
        self.operacion_cramer = CreadorDeCramer()
        self.historial = historial

        self.matriz_entrada = []
        self.solucion = []

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
                                         text="Ingrese la matriz aumentada:")
        self.label_matriz.grid(row=0, column=0, padx=10, pady=10)

        self.btn_importar_hist = ctk.CTkButton(self.entrada_frame, text="Importar", command=self.abrir_historial)
        self.btn_importar_hist.grid(row=1, column=0, padx=10, pady=10)
        self.tooltip_importar = CTkToolTip(self.btn_importar_hist,
                                           message="Importar una matriz del historial")

        # frame para entrada
        self.text_matriz = FrameEntradaMatriz(self.entrada_frame)
        self.text_matriz.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Botón para resolver
        self.btn_resolver = ctk.CTkButton(self.entrada_frame, text="Resolver", command=self.resolver_cramer)
        self.btn_resolver.grid(row=3, column=0, padx=10, pady=10)

        # Botón para limpiar entradas y resultados
        self.btn_limpiar = ctk.CTkButton(self.resultado_frame, text="Limpiar", command=self.limpiar_entradas)
        self.btn_limpiar.grid(row=4, column=0, padx=10, pady=10)

        # Frame para resultados
        self.label_resultado = ctk.CTkLabel(self.resultado_frame, text="Resultado:")
        self.label_resultado.grid(row=0, column=0, padx=10, pady=10)

        self.text_salida = ctk.CTkTextbox(self.resultado_frame, width=400, height=150)
        self.text_salida.grid(row=1, column=0, padx=10, pady=10)

        self.tablas_entradas = None
        self.tablas_salidas = None

    def resolver_cramer(self):
        """Obtiene la matriz aumentada, procesa los datos y resuelve el sistema de ecuaciones."""
        matriz_text = self.text_matriz.obtener_matriz_como_array()

        if not matriz_text:
            self.mostrar_error("Las entradas de la matriz están vacías.")
            return

        try:
            # matriz_filas = matriz_text.split("\n")
            # matriz_aumentada = [list(map(Fraction, fila.split())) for fila in matriz_filas]

            # Pasar la matriz aumentada a la clase OperacionCramer
            self.operacion_cramer.ingresar_datos_cramer(matriz_text)
            soluciones, procedimiento = self.operacion_cramer.resolver_cramer()

            # Mostrar el resultado y el procedimiento detallado
            self.mostrar_resultado(soluciones, procedimiento)
        except ValueError as e:
            self.mostrar_error(str(e))

    def mostrar_resultado(self, soluciones, procedimiento):
        """Muestra las soluciones y el procedimiento en la interfaz gráfica."""
        self.text_salida.delete("1.0", "end")
        for paso in procedimiento:
            self.text_salida.insert("end", f"{paso}\n")

        self.text_salida.insert("end", "\nSoluciones del sistema:\n")
        for i, solucion in enumerate(soluciones):
            self.text_salida.insert("end", f"x{i + 1} = {solucion}\n")
        self.crear_tablas()

    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error en la interfaz gráfica."""
        self.text_salida.delete("1.0", "end")
        self.text_salida.insert("end", f"Error: {mensaje}\n")

    def crear_tablas(self):
        """Crea los frames con CTkTable para mostrar las matrices."""
        # tablas para la frame 1 que contiene los datos de entrada
        datos_tabla_entrada = self.operacion_cramer.matriz_original  # Usamos la matriz original
        self.tablas_entradas = TablasFrame(self, tabla1=datos_tabla_entrada, texto1="Matriz Ingresada:")
        self.tablas_entradas.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # tablas para la frame 2 que contiene los datos de salida
        datos_tabla_salida = lista_a_matriz(self.operacion_cramer.solucion)
        self.tablas_salidas = TablasFrame(self, tabla1=datos_tabla_salida, texto1="Solución:")
        self.tablas_salidas.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        # botón de guardado
        self.btn_guardar = ctk.CTkButton(self.tablas_salidas.frame_entradas, text="Guardar",
                                         command=self.accionar_guardado)
        self.btn_guardar.pack(padx=10, pady=10)
        self.tooltip_guardar = CTkToolTip(self.btn_guardar,
                                            message="Guardar en historial")

    def limpiar_entradas(self):
        """Limpia los campos de entrada y salida."""
        # self.limpiar_tablas()
        self.tablas_entradas.limpiar_tablas()
        self.tablas_salidas.limpiar_tablas()
        self.text_salida.delete("1.0", "end")

    def accionar_guardado(self):
        matriz_solucion = lista_a_matriz(self.operacion_cramer.solucion)
        self.guardar_en_historial(self.operacion_cramer.matriz_original, matriz_solucion)

    def guardar_en_historial(self, matriz1, solucion):
        self.historial.agregar_problema(matriz1=matriz1, solucion=solucion,
                                        tipo="uno", clasificacion="matriz")
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

# Inicializar la aplicación
if __name__ == "__main__":
    root = ctk.CTk()
    historial = []
    app_frame = CramerFrame(root, historial)
    app_frame.pack(padx=10, pady=10, fill="both", expand=True)
    root.mainloop()