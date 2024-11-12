"""
Archivo: transpuesta_inversa_calc.py 1.2.1
Descripción: Este archivo contiene la interfáz gráfica de la calculadora de transpuestas e inversas de matrices.
"""
from ctkcomponents import *
from CTkToolTip import *
from models.modelos_matriz_vector.clase_matriz_inv_tran import *
from Historial.historial_matriz.historial_popup.historial_popup_ui import *
from GUI.gui_calc_matriz.interfaz_entrada.entrada_matriz_frame import *
from GUI.gui_calc_matriz.tablas_gui.modulo_tablas_entradas import TablasFrame


class MatrizCalculatorInvTranFrame(ctk.CTkFrame):
    """
    Clase que representa la interfaz gráfica para ingresar una matriz y calcular su transpuesta o inversa.
    Contiene campos de entrada, botones para seleccionar la operación y mostrar resultados.
    """

    def __init__(self, master, historial):
        """
        Inicializa el frame de la calculadora de matrices.

        Args:
            master (tk.Tk): La ventana principal de la aplicación.
        """
        super().__init__(master)

        self.historial = historial
        # Crear elementos de la interfaz
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.input_label = ctk.CTkLabel(self.left_frame,
                                        text="Ingrese la matriz (aumentada para la inversa):")
        self.input_label.pack(pady=10)

        self.btn_importar_hist = ctk.CTkButton(self.left_frame, text="Importar", command=self.abrir_historial)
        self.btn_importar_hist.pack(pady=10)
        self.tooltip_importar1 = CTkToolTip(self.btn_importar_hist,
                                            message="Importar una matriz del historial")

        # frame para entrada
        self.text_matriz = FrameEntradaMatriz(self.left_frame)
        self.text_matriz.pack(pady=10)

        self.operacion = ctk.StringVar(value="transpuesta")
        self.transpuesta_radio = ctk.CTkRadioButton(self.left_frame, text="Transpuesta", variable=self.operacion,
                                                    value="transpuesta")
        self.inversa_radio = ctk.CTkRadioButton(self.left_frame, text="Inversa", variable=self.operacion,
                                                value="inversa")
        self.transpuesta_radio.pack(pady=5)
        self.inversa_radio.pack(pady=5)

        self.calcular_button = ctk.CTkButton(self.left_frame, text="Calcular", command=self.calcular)
        self.calcular_button.pack(pady=10)

        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.solucion_label = ctk.CTkLabel(self.right_frame, text="Solución:")
        self.solucion_label.pack(pady=10)

        self.result_textbox = ctk.CTkTextbox(self.right_frame, width=400, height=150, state="disabled")
        self.result_textbox.pack(pady=10)

        self.limpiar_button = ctk.CTkButton(self.right_frame, text="Limpiar", command=self.limpiar)
        self.limpiar_button.pack(pady=10)

        self.historial_local = []

        # Configurar pesos para que los frames se ajusten al redimensionar
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Variables para los frames y tablas adicionales
        # self.frame_matriz1 = None
        # self.tabla_matriz2 = None
        # self.frame_matriz2 = None
        # self.tabla_matriz1 = None
        # self.tabla_salida = None
        self.tablas_entradas = None
        self.tablas_salidas = None

    def calcular(self):
        """
        Método llamado al presionar el botón "Calcular". Realiza la operación seleccionada (transpuesta o inversa)
        en la matriz ingresada y muestra el resultado en la interfaz.
        """
        operacion = self.operacion.get()
        # matriz_str = self.text_matriz.obtener_matriz_como_array()

        try:
            matriz = self.text_matriz.obtener_matriz_como_array()

            if operacion == "transpuesta":
                transpuesta = MatrizCalculadora.transponer_matriz(matriz)
                transpuesta_str = MatrizCalculadora.matriz_a_string(transpuesta)
                self.mostrar_solucion(f"Matriz Transpuesta:\n{transpuesta_str}")
                self.guardar_en_historial_local("Transpuesta", matriz, transpuesta)
                self.crear_tablas()
            elif operacion == "inversa":
                pasos, inversa = MatrizCalculadora.inversa_matriz_con_pasos(matriz)
                inversa_str = MatrizCalculadora.matriz_a_string(inversa)
                pasos_str = "\n".join(pasos)
                self.mostrar_solucion(f"Pasos para encontrar la inversa:\n{pasos_str}\n\nMatriz Inversa:\n{inversa_str}")
                self.guardar_en_historial_local("Inversa", matriz, inversa)
                self.crear_tablas()
        except ValueError as e:
            CTkMessagebox(title="Error", message=str(e), icon="warning", option_1="Entendido",
                          button_hover_color="green", fade_in_duration=2)

    def mostrar_solucion(self, texto):
        """
        Muestra el resultado de la operación (transpuesta o inversa) en el cuadro de texto de la solución.

        Args:
            texto (str): Texto que se mostrará como resultado.
        """
        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", texto)
        self.result_textbox.configure(state="disabled")

    def crear_tablas(self):
        """Crea los frames con CTkTable para mostrar las matrices."""
        # tablas para la frame 1 que contiene los datos de entrada
        datos_tabla_entrada = self.historial_local[-1]['matriz_entrada']  # Usamos la matriz original
        self.tablas_entradas = TablasFrame(self, tabla1=datos_tabla_entrada, texto1="Matriz Ingresada:")
        self.tablas_entradas.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # tablas para la frame 2 que contiene los datos de salida
        datos_tabla_salida = self.historial_local[-1]['matriz_solucion']
        self.tablas_salidas = TablasFrame(self, tabla1=datos_tabla_salida, texto1="Solución:")
        self.tablas_salidas.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # botón de guardado
        self.btn_guardar = ctk.CTkButton(self.tablas_salidas.frame_entradas, text="Guardar",
                                         command=self.accionar_guardado)
        self.btn_guardar.pack(padx=10, pady=10)
        self.tooltip_guardar = CTkToolTip(self.btn_guardar,
                                            message="Guardar en historial")

    def limpiar(self):
        """
        Limpia el cuadro de texto de entrada y el cuadro de resultado.
        """
        self.text_matriz.limpiar_entradas()
        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.configure(state="disabled")
        self.tablas_entradas.limpiar_tablas()
        self.tablas_salidas.limpiar_tablas()

    def guardar_en_historial_local(self, tipo, matriz_entrada, matriz_solucion):
        """
        Guarda la operación realizada en el historial local.

        Args:
            tipo (str): Tipo de operación realizada (transpuesta o inversa).
            matriz_entrada (list): La matriz original ingresada.
            matriz_solucion (list): El resultado de la operación (matriz transpuesta o inversa).
        """
        self.historial_local.append({
            "tipo": tipo,
            "matriz_entrada": matriz_entrada,
            "matriz_solucion": matriz_solucion
        })

    def accionar_guardado(self):
        self.guardar_en_historial(self.historial_local[-1]['matriz_entrada'],
                                  self.historial_local[-1]['matriz_solucion'])

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


if __name__ == "__main__":
    # Configuración del tema para la interfaz gráfica
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Crear la ventana principal de la aplicación
    app = ctk.CTk()
    app.geometry("800x400")

    historial = []

    # Crear el frame de la calculadora de matrices e iniciarla
    matriz_calculator_frame = MatrizCalculatorInvTranFrame(app, historial)
    matriz_calculator_frame.pack(fill="both", expand=True)

    app.mainloop()
