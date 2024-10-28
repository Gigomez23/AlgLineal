# Archivo: cramer_frame.py
from CTkTable import CTkTable
from ctkcomponents import *
from CTkToolTip import *
from Historial.historial_popup.historial_popup_ui import *
from models.operacion_cramer import CreadorDeCramer
from GUI.interfaz_entrada.entrada_matriz_frame import *
from funciones_adicionales.convertir_formato_lista import *


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
                                         text="Ingrese la matriz aumentada "
                                              "(separada por espacios):")
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

        # Variables para los frames y tablas adicionales
        self.frame_matriz1 = None
        self.tabla_matriz2 = None
        self.frame_matriz2 = None
        self.tabla_matriz1 = None
        self.tabla_salida = None

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
        datos_tabla_entrada = self.operacion_cramer.matriz_original  # Usamos la matriz original
        self.tabla_entrada = CTkTable(self.frame_matriz1, values=datos_tabla_entrada)
        self.tabla_entrada.pack(padx=10, pady=10)

        # tablas para la frame 2 que contiene los datos de salida
        datos_tabla_salida = lista_a_matriz(self.operacion_cramer.solucion)
        self.tabla_salida = CTkTable(self.frame_matriz2, values=datos_tabla_salida)
        self.tabla_salida.pack(padx=10, pady=10)

        #botón de guardado
        self.btn_guardar = ctk.CTkButton(self.frame_matriz2, text="Guardar", command=self.accionar_guardado)
        self.btn_guardar.pack(padx=10, pady=10)
        self.tooltip_guardar = CTkToolTip(self.btn_guardar,
                                            message="Guardar en historial")

    def limpiar_entradas(self):
        """Limpia los campos de entrada y salida."""
        self.limpiar_tablas()
        self.text_matriz.limpiar_entradas()
        self.text_salida.delete("1.0", "end")

    def limpiar_tablas(self):
        """Elimina los frames con las tablas y reinicia las soluciones."""
        # Limpiar la lista de soluciones
        self.historial_local = []

        # Destruir los frames de las tablas si existen
        if self.frame_matriz1:
            self.frame_matriz1.destroy()
            self.frame_matriz1 = None
        if self.frame_matriz2:
            self.frame_matriz2.destroy()
            self.frame_matriz2 = None

        # Reiniciar las tablas de entrada, salida y matriz reducida
        if self.tabla_salida:
            self.tabla_salida.destroy()
            self.tabla_salida = None

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