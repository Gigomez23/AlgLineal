import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from CTkTable import *
from models.clase_matriz_op_ari import *
from Additiona_functions.convertir_formato_lista import convertir_a_formato_lista

class OperacionesAritmeticasMatrizFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.operaciones = CreadorDeMatricesAritmeticas()
        self.operacion_seleccionada = ctk.StringVar(value="sumar")
        self.tablas_mostradas = False  # Para controlar si las tablas están mostradas o no

        # Frame para entradas
        self.entrada_frame = ctk.CTkFrame(self)
        self.entrada_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame para resultados
        self.resultado_frame = ctk.CTkFrame(self)
        self.resultado_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Componentes del frame de entrada
        self.label_matriz1 = ctk.CTkLabel(self.entrada_frame, text="Matriz 1 (separada por espacios, cada fila en una línea):")
        self.label_matriz1.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.text_matriz1 = ctk.CTkTextbox(self.entrada_frame, width=400, height=100)
        self.text_matriz1.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        self.label_matriz2 = ctk.CTkLabel(self.entrada_frame, text="Matriz 2 (separada por espacios, cada fila en una línea):")
        self.label_matriz2.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        self.text_matriz2 = ctk.CTkTextbox(self.entrada_frame, width=400, height=100)
        self.text_matriz2.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

        # Radio buttons para seleccionar operación
        self.radio_suma = ctk.CTkRadioButton(self.entrada_frame, text="Sumar", variable=self.operacion_seleccionada, value="sumar")
        self.radio_suma.grid(row=5, column=0, padx=10, pady=10)

        self.radio_resta = ctk.CTkRadioButton(self.entrada_frame, text="Restar", variable=self.operacion_seleccionada, value="restar")
        self.radio_resta.grid(row=5, column=1, padx=10, pady=10)

        self.radio_multiplicar = ctk.CTkRadioButton(self.entrada_frame, text="Multiplicar", variable=self.operacion_seleccionada, value="multiplicar")
        self.radio_multiplicar.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Botón para calcular
        self.btn_calcular = ctk.CTkButton(self.entrada_frame, text="Calcular", command=self.calcular_operacion)
        self.btn_calcular.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

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
        self.tabla_frame1 = ctk.CTkFrame(self)
        self.tabla_frame2 = ctk.CTkFrame(self)

    def obtener_matrices(self):
        """Función que extrae la matriz de lo que fue digitado al usuario

        :return
            bool
        """
        matriz1_text = self.text_matriz1.get("1.0", "end-1c")
        matriz2_text = self.text_matriz2.get("1.0", "end-1c")

        matriz1_filas = matriz1_text.split("\n")
        matriz2_filas = matriz2_text.split("\n")

        try:
            self.operaciones.matriz1 = [[Fraction(x) for x in fila.split()] for fila in matriz1_filas if fila.strip()]
            self.operaciones.matriz2 = [[Fraction(x) for x in fila.split()] for fila in matriz2_filas if fila.strip()]

            if not self.validar_dimensiones_para_operaciones():
                raise ValueError("Las matrices deben tener las mismas dimensiones para suma/resta.")
        except ValueError as e:
            CTkMessagebox(title="Error de formato", message=f"Error en el formato de las matrices: {str(e)}",
                          icon="warning", option_1="Entendido", button_hover_color="green")
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
        """Función que valída las dimensiones para la multiplicación
        :return
            bool
        """
        return len(self.operaciones.matriz1[0]) == len(self.operaciones.matriz2)

    def calcular_operacion(self):
        """Función que selecciona el cálculo que desea el usuario."""
        matriz1_text = self.text_matriz1.get("1.0", "end-1c").strip()
        matriz2_text = self.text_matriz2.get("1.0", "end-1c").strip()

        # Verificar si los campos están vacíos
        if not matriz1_text or not matriz2_text:
            CTkMessagebox(title="Advertencia", message="Por favor, ingrese ambas matrices antes de calcular.",
                          icon="warning", option_1="Entendido", button_hover_color="green")
            return

        if self.obtener_matrices():
            operacion = self.operacion_seleccionada.get()

            if operacion == "sumar":
                self.operaciones.suma_matrices()
            elif operacion == "restar":
                self.operaciones.resta_matrices()
            elif operacion == "multiplicar":
                if self.validar_dimensiones_para_multiplicacion():
                    self.operaciones.multiplicar_matrices()
                else:
                    CTkMessagebox(title="Error de dimensiones",
                                  message=f"El número de columnas de la Matriz 1 debe coincidir con el número de "
                                          f"filas de la Matriz 2 para multiplicación.",
                                  icon="warning", option_1="Entendido", button_hover_color="green")
                    return

            self.mostrar_resultado()
            self.mostrar_tablas()  # Muestra las tablas vacías

    def mostrar_resultado(self):
        """Función muestra los resultados en el textbox de salida."""
        resultado_formato = self.operaciones.formato_matriz(self.operaciones.resultado)
        procedimiento = self.operaciones.procedimiento
        self.text_salida.delete("1.0", "end")
        self.text_salida.insert("end", f"{procedimiento}\n\nResultado:\n{resultado_formato}")

    def mostrar_tablas(self):
        """Muestra las tablas vacías cuando se presiona el botón 'Calcular'."""
        if not self.tablas_mostradas:
            self.tabla_frame1.grid(row=3, column=0, padx=10, pady=20)
            self.tabla_frame2.grid(row=3, column=1, padx=10, pady=10)

            #Se crea los labels para cada frame de las tablas
            self.label_tabla_entrada = ctk.CTkLabel(self.tabla_frame1,
                                              text="Matrices de entrada: ")
            self.label_tabla_entrada.pack(pady=10, padx=10)
            self.label_tabla_solucion = ctk.CTkLabel(self.tabla_frame2,
                                                    text="Matriz Solución: ")
            self.label_tabla_solucion.pack(padx=10, pady=10)

            # Tablas del frame1 que contienen los datos de entradas mostradas en una tabla cTkTable
            datos_tabla_1 = convertir_a_formato_lista(self.text_matriz1.get("1.0", "end-1c"))
            self.tabla1 = CTkTable(self.tabla_frame1, values=datos_tabla_1)
            self.tabla1.pack(padx=10, pady=10)

            datos_tabla_2 = convertir_a_formato_lista(self.text_matriz2.get("1.0", "end-1c"))
            self.tabla2 = CTkTable(self.tabla_frame1, values=datos_tabla_2)
            self.tabla2.pack(padx=10, pady=10)

            #tabla de solución
            datos_tabla_solucion = self.operaciones.resultado
            self.tabla_solucion = CTkTable(self.tabla_frame2, values=datos_tabla_solucion)
            self.tabla_solucion.pack(padx=10, pady=10)

            self.tablas_mostradas = True

    def limpiar_entradas(self):
        """Limpia las entradas y elimina las tablas."""
        # Limpiar los campos de entrada
        self.text_matriz1.delete("1.0", "end")
        self.text_matriz2.delete("1.0", "end")
        self.text_salida.delete("1.0", "end")

        # Eliminar las tablas si están mostradas
        if self.tablas_mostradas:
            if hasattr(self, 'tabla1'):
                self.tabla1.destroy()
            if hasattr(self, 'tabla2'):
                self.tabla2.destroy()
            if hasattr(self, 'tabla_solucion'):
                self.tabla_solucion.destroy()

            # Eliminar los frames de las tablas
            self.tabla_frame1.grid_forget()
            self.tabla_frame2.grid_forget()

            self.tablas_mostradas = False


if __name__ == "__main__":
    root = ctk.CTk()
    app_frame = OperacionesAritmeticasMatrizFrame(root)
    app_frame.pack(padx=10, pady=10, fill="both", expand=True)
    root.mainloop()
