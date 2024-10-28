"""
Archivo: Au_Ax_calc.py 1.3.1
Descripción: diseño de frame para gui de problemas tipo de Au + Av
"""
from ctkcomponents import *
from CTkTable import CTkTable
from CTkToolTip import *
from models.clase_matriz_vectores import *
from funciones_adicionales.convertir_formato_lista import *
from Historial.historial_popup.historial_popup_ui import *
# todo: agregar nuevos metodos de ingresar datos


class CalculadoraDeMatrizxVectoresFrame(ctk.CTkFrame):
    def __init__(self, parent, historial):
        super().__init__(parent)
        self.matriz_operaciones = CreadorDeOperacionMatrizVector()
        self.historial = historial
        self.mensaje = "Importar una matriz del historial."

        # Crear el frame izquierdo para las entradas
        self.frame_izquierdo = ctk.CTkFrame(self)
        self.frame_izquierdo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Crear el frame derecho para la salida y controles
        self.frame_derecho = ctk.CTkFrame(self)
        self.frame_derecho.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Configurar pesos para que los frames se ajusten al redimensionar
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Frame Izquierdo: Entradas ---
        self.label_matriz_A = ctk.CTkLabel(self.frame_izquierdo,
                                           text="Matriz A (fila separadas por enter, "
                                                "valores separados por espacios):")
        self.label_matriz_A.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="w")

        # boton para importar en primera entrada
        self.btn_importar_hist_entrada1 = ctk.CTkButton(self.frame_izquierdo, text="Importar",
                                                        command=self.abrir_historial1)
        self.btn_importar_hist_entrada1.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        #tooltip para boton de importar
        self.tooltip_importar1 = CTkToolTip(self.btn_importar_hist_entrada1,
                                            message="Importar una matriz del historial")


        self.text_matriz_A = ctk.CTkTextbox(self.frame_izquierdo, width=300, height=100)
        self.text_matriz_A.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        self.label_vector_u = ctk.CTkLabel(self.frame_izquierdo,
                                           text="Vector u (valores separados por espacios):")
        self.label_vector_u.grid(row=4, column=0, padx=10, pady=10, columnspan=2, sticky="w")

        # boton para importar en segunda entrada
        self.btn_importar_hist_entrada2 = ctk.CTkButton(self.frame_izquierdo, text="Importar",
                                                        command=self.abrir_historial2)
        self.btn_importar_hist_entrada2.grid(row=5, column=0, padx=10, pady=10, columnspan=2)

        # tooltip para boton de importar 2
        self.tooltip_importar2 = CTkToolTip(self.btn_importar_hist_entrada2,
                                            message="Importar un vector del historial")

        self.text_vector_u = ctk.CTkTextbox(self.frame_izquierdo, width=300, height=50)
        self.text_vector_u.grid(row=6, column=0, padx=10, pady=10, columnspan=2)

        self.label_vector_v = ctk.CTkLabel(self.frame_izquierdo,
                                           text="Vector v (valores separados por espacios):")
        self.label_vector_v.grid(row=7, column=0, padx=10, pady=10, columnspan=2, sticky="w")

        # boton para importar en primera entrada
        self.btn_importar_hist_entrada3 = ctk.CTkButton(self.frame_izquierdo, text="Importar",
                                                        command=self.abrir_historial3)
        self.btn_importar_hist_entrada3.grid(row=8, column=0, padx=10, pady=10, columnspan=2)

        # tooltip para boton de importación
        self.tooltip_importar3 = CTkToolTip(self.btn_importar_hist_entrada3,
                                            message="Importar un vector del historial")

        self.text_vector_v = ctk.CTkTextbox(self.frame_izquierdo, width=300, height=50)
        self.text_vector_v.grid(row=9, column=0, padx=10, pady=10, columnspan=2)

        # --- Frame Derecho: Controles y Salida ---
        self.label_metodo = ctk.CTkLabel(self.frame_derecho, text="Método de Resolución:")
        self.label_metodo.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.metodo_var = ctk.StringVar(value="directo")
        self.radio_directo = ctk.CTkRadioButton(self.frame_derecho, text="A(u + v)", variable=self.metodo_var,
                                                value="directo")
        self.radio_directo.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.radio_separado = ctk.CTkRadioButton(self.frame_derecho, text="A(u) + A(v)", variable=self.metodo_var,
                                                 value="separado")
        self.radio_separado.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        self.radio_ambos = ctk.CTkRadioButton(self.frame_derecho, text="Ambos métodos", variable=self.metodo_var,
                                              value="ambos")
        self.radio_ambos.grid(row=2, column=0, padx=10, pady=5, columnspan=2, sticky="nsew")

        # Botón de calcular
        self.btn_calcular = ctk.CTkButton(self.frame_derecho, text="Calcular", width=100,
                                          command=self.calcular_multiplicacion)
        self.btn_calcular.grid(row=3, column=0, padx=10, pady=10, columnspan=2, sticky="w")

        # Área de salida
        self.label_salida = ctk.CTkLabel(self.frame_derecho, text="Solución:")
        self.label_salida.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.text_salida_frame = ctk.CTkFrame(self.frame_derecho)
        self.text_salida_frame.grid(row=5, column=0, padx=10, pady=10)

        self.text_salida = ctk.CTkTextbox(self.text_salida_frame, width=400, height=150, wrap="none")
        self.text_salida.pack(side="left", fill="both", expand=True)

        # Scrollbar para el text_salida
        self.scrollbar = ctk.CTkScrollbar(self.text_salida_frame, command=self.text_salida.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.text_salida.configure(yscrollcommand=self.scrollbar.set)

        # Botón de limpiar debajo del textbox de salida
        self.btn_limpiar = ctk.CTkButton(self.frame_derecho, text="Limpiar", width=100, command=self.clear_inputs)
        self.btn_limpiar.grid(row=6, column=0, padx=10, pady=10, columnspan=2, sticky="w")

        # Variables para los frames y tablas adicionales
        self.frame_matriz1 = None
        self.frame_matriz2 = None
        self.tabla_matriz = None
        self.tabla_matriz2 = None
        self.tabla_reducida = None
        self.tabla_entrada = None
        self.tabla2_entrada = None
        self.tabla_salida = None
        self.tabla_entrada2 = None
        self.frame_matriz_ingresada = None
        self.frame_vectores_ingresados = None
        self.tabla_matriz1 = None
        self.frame_vector_uno = None

    def calcular_multiplicacion(self):
        """Calcula la multiplicación según el método seleccionado"""
        metodo = self.metodo_var.get()

        # Obtener el contenido de los campos de texto
        matriz_A_text = self.text_matriz_A.get("1.0", "end-1c").strip()
        vector_u_text = self.text_vector_u.get("1.0", "end-1c").strip()
        vector_v_text = self.text_vector_v.get("1.0", "end-1c").strip()

        # Verificar si algún campo de entrada está vacío
        if not matriz_A_text or not vector_u_text or not vector_v_text:
            CTkMessagebox(title="Error de entrada", message="Todos los campos deben estar llenos.", icon="warning",
                          option_1="Entendido", button_hover_color="green", fade_in_duration=2)
            return

        try:
            # Obtener la matriz A y calcular filas y columnas automáticamente
            matriz_A_text = matriz_A_text.split("\n")
            matriz_A = [[Fraction(x) for x in fila.split()] for fila in matriz_A_text if fila.strip()]

            filas_A = len(matriz_A)
            columnas_A = len(matriz_A[0]) if filas_A > 0 else 0

            # Obtener vectores u y v
            vector_u = [Fraction(x) for x in vector_u_text.split()]
            vector_v = [Fraction(x) for x in vector_v_text.split()]

            # Validar si el tamaño de los vectores coincide con el número de columnas de la matriz A
            if len(vector_u) != columnas_A or len(vector_v) != columnas_A:
                raise ValueError("El tamaño de los vectores no coincide con el número de columnas de la matriz A.")

        except ValueError as e:
            # Mensaje de error por tamaño de vectores o fracciones no válidas
            CTkMessagebox(title="Error de formato", message=str(e), icon="warning", option_1="Entendido",
                          button_hover_color="green", fade_in_duration=2)
            return
        except ZeroDivisionError:
            # Mensaje de error si el usuario intenta dividir por 0
            CTkMessagebox(title="Error de división", message="No se puede dividir por cero.", icon="warning",
                          option_1="Entendido", button_hover_color="green", fade_in_duration=2)
            return
        except Exception:
            # Mensaje de error por entradas no numéricas
            CTkMessagebox(title="Error de entrada",
                          message="Por favor, ingresa solo números válidos (sin letras ni símbolos).", icon="warning",
                          option_1="Entendido", button_hover_color="green", fade_in_duration=2)
            return

        # Almacenar datos en la instancia de operaciones
        self.matriz_operaciones.A = matriz_A
        self.matriz_operaciones.u = vector_u
        self.matriz_operaciones.v = vector_v
        self.matriz_operaciones.filas_A = filas_A
        self.matriz_operaciones.columnas_A = columnas_A

        # Limpiar el área de salida antes de mostrar resultados
        self.text_salida.delete("1.0", "end")

        # Resolver según el método seleccionado
        mostrar_pasos = True  # Puedes modificar esto si no deseas mostrar los pasos
        self.matriz_operaciones.imprimir_solucion(metodo, self.text_salida, mostrar_pasos)

        self.crear_tablas()

    # función para crear tablas
    def crear_tablas(self):
        """Crea los frames con CTkTable para mostrar las matrices."""
        if self.frame_matriz1 or self.frame_matriz2:
            self.limpiar_tablas()

        # Frame para la primera serie de tablas
        self.frame_matriz1 = ctk.CTkFrame(self)
        self.frame_matriz1.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        # subFrame para la matriz
        self.frame_matriz_ingresada = ctk.CTkFrame(self.frame_matriz1)
        self.frame_matriz_ingresada.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.frame_vectores_ingresados = ctk.CTkFrame(self.frame_matriz1)
        self.frame_vectores_ingresados.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        # Frame para la serie de tablas de solucion y el boton de guardar
        self.frame_matriz2 = ctk.CTkFrame(self)
        self.frame_matriz2.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        # label para matriz
        self.tabla_matriz1 = ctk.CTkLabel(self.frame_matriz_ingresada, text="Matriz Ingresada:")
        self.tabla_matriz1.pack(padx=10, pady=10)
        # labels para frames
        self.tabla_matriz2 = ctk.CTkLabel(self.frame_matriz2, text="Solución:")
        self.tabla_matriz2.pack(padx=10, pady=10)

        # tablas para la frame 1 que contiene los datos de entrada
        # tabla para la matriz original
        datos_tabla_matriz = self.matriz_operaciones.A
        self.tabla_matriz = CTkTable(self.frame_matriz_ingresada, values=datos_tabla_matriz)
        self.tabla_matriz.pack(padx=10, pady=10)

        # frame exclusivo para vector 1 ingresado
        self.frame_vector_uno = ctk.CTkFrame(self.frame_vectores_ingresados)
        self.frame_vector_uno.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # label para vector 1 ingresado
        self.label_vector_ingresada = ctk.CTkLabel(self.frame_vector_uno, text="Vector u:")
        self.label_vector_ingresada.pack(padx=10, pady=10)

        # tabla para el vector ingresado
        datos_tabla_entrada = lista_a_matriz(self.matriz_operaciones.u)
        self.tabla_entrada = CTkTable(self.frame_vector_uno, values=datos_tabla_entrada)
        self.tabla_entrada.pack(padx=10, pady=10)

        # frame exclusivo para vector 2 ingresado
        self.frame_vector_dos = ctk.CTkFrame(self.frame_vectores_ingresados)
        self.frame_vector_dos.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        # label para vector 2 ingresado
        self.label_vector_ingresado2 = ctk.CTkLabel(self.frame_vector_dos, text="Vector v:")
        self.label_vector_ingresado2.pack(padx=10, pady=10)

        # tabla para el vector ingresado
        datos_tabla_entrada2 = lista_a_matriz(self.matriz_operaciones.v)
        self.tabla_entrada2 = CTkTable(self.frame_vector_dos, values=datos_tabla_entrada2)
        self.tabla_entrada2.pack(padx=10, pady=10)

        # tablas para la frame 2 que contiene los datos de salida
        datos_tabla_salida = lista_a_matriz(self.matriz_operaciones.solucion)
        self.tabla_salida = CTkTable(self.frame_matriz2, values=datos_tabla_salida)
        self.tabla_salida.pack(padx=10, pady=10)

        #botón de guardado
        self.btn_guardar = ctk.CTkButton(self.frame_matriz2, text="Guardar",
                                         command=self.accionar_guardado_en_historial)
        self.btn_guardar.pack(padx=10, pady=10)
        self.tooltip_guardar = CTkToolTip(self.btn_guardar,
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
        if self.tabla_entrada2:
            self.tabla_entrada2.destroy()
            self.tabla_entrada2 = None
        if self.tabla_reducida:
            self.tabla_reducida.destroy()
            self.tabla_reducida = None

    def clear_inputs(self):
        """Limpia los campos de entrada y salida"""
        self.text_matriz_A.delete("1.0", "end")
        self.text_vector_u.delete("1.0", "end")
        self.text_vector_v.delete("1.0", "end")
        self.text_salida.delete("1.0", "end")
        self.limpiar_tablas()

    def accionar_guardado_en_historial(self):
        tabla_u = lista_a_matriz(self.matriz_operaciones.u)
        tabla_v = lista_a_matriz(self.matriz_operaciones.v)
        datos_tabla_salida = lista_a_matriz(self.matriz_operaciones.solucion)
        self.guardar_en_historial(self.matriz_operaciones.A, tabla_u, tabla_v, datos_tabla_salida)

    def guardar_en_historial(self, matriz1, matriz2, matriz3, solucion):
        self.historial.agregar_problema(matriz1=matriz1, matriz2=matriz2, matriz3=matriz3, solucion=solucion,
                                        tipo='tres', clasificacion="mixto")
        CTkNotification(master=self, state="info",
                        message=f"{self.historial.problemas[-1]['nombre']} ha sido guardado exitosamente!",
                        side="right_bottom")

    def abrir_historial1(self):
        """Abre el pop-up del historial."""
        historial_popup = HistorialPopup(self, self.historial, self.text_matriz_A)
        historial_popup.grab_set()  # Foco en el pop-up

    def abrir_historial2(self):
        """Abre el pop-up del historial."""
        historial_popup = HistorialPopup(self, self.historial, self.text_vector_u)
        historial_popup.grab_set()  # Foco en el pop-up

    def abrir_historial3(self):
        """Abre el pop-up del historial."""
        historial_popup = HistorialPopup(self, self.historial, self.text_vector_v)
        historial_popup.grab_set()  # Foco en el pop-up


# Ejemplo de uso del frame en una aplicación principal de tkinter
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x400")
    root.title("Calculadora de Ecuaciones Matriciales")
    historial = []

    frame = CalculadoraDeMatrizxVectoresFrame(root, historial)
    frame.pack(fill="both", expand=True)

    root.mainloop()