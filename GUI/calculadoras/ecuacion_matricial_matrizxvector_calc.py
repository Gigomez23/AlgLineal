"""
Archivo: ecuacion_matricial_matrizxvector_calc.py 1.1.1
Descripción: Archivo contiene la interfaz grafica para la ecuacion matricial
"""
import customtkinter as ctk
from models.clase_matriz_operaciones import *
from CTkMessagebox import CTkMessagebox


class MultiplicacionMatricesFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.matriz_operaciones = CreadorDeOperaciones()

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
        # self.label_nombre = ctk.CTkLabel(self.frame_izquierdo, text="Nombre del problema:")
        # self.label_nombre.grid(row=0, column=0, padx=10, pady=10)
        #
        # self.entry_nombre = ctk.CTkEntry(self.frame_izquierdo)
        # self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        self.label_matriz_A = ctk.CTkLabel(self.frame_izquierdo,
                                           text="Matriz A (filas separadas por enter, "
                                                "valores separados por espacios):")
        self.label_matriz_A.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.text_matriz_A = ctk.CTkTextbox(self.frame_izquierdo, width=300, height=100)
        self.text_matriz_A.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        # Entradas para la matriz b
        self.label_matriz_b = ctk.CTkLabel(self.frame_izquierdo,
                                           text="Vector/matriz b (valores separados por espacios):")
        self.label_matriz_b.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        self.text_matriz_b = ctk.CTkTextbox(self.frame_izquierdo, width=300, height=50)
        self.text_matriz_b.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

        # Botones debajo de las entradas
        self.btn_calcular = ctk.CTkButton(self.frame_izquierdo, text="Calcular Ax = b",
                                          command=self.calcular_multiplicacion)
        self.btn_calcular.grid(row=5, column=0, padx=10, pady=10)

        self.btn_mostrar_pasos = ctk.CTkButton(self.frame_izquierdo, text="Mostrar Resultado con Pasos",
                                               command=self.mostrar_resultado_con_pasos)
        self.btn_mostrar_pasos.grid(row=5, column=1, padx=10, pady=10)

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

    def calcular_multiplicacion(self):
        """Calcula la multiplicación Ax = b y muestra el resultado sin pasos"""
        # Obtener el contenido de las entradas de texto
        matriz_A_text = self.text_matriz_A.get("1.0", "end-1c").strip()
        matriz_b_text = self.text_matriz_b.get("1.0", "end-1c").strip()

        # Verificar si alguno de los campos de entrada está vacío
        if not matriz_A_text or not matriz_b_text:
            CTkMessagebox(title="Error de entrada", message="Todos los campos deben estar llenos.", icon="warning",
                          option_1="Entendido", button_hover_color="green")
            return

        try:
            # Obtener la matriz A y calcular filas y columnas automáticamente
            matriz_A_text = matriz_A_text.split("\n")
            matriz_A = [[Fraction(x) for x in fila.split()] for fila in matriz_A_text if fila.strip()]

            filas_A = len(matriz_A)
            columnas_A = len(matriz_A[0]) if filas_A > 0 else 0

            matriz_b_text = matriz_b_text.split()
            matriz_b = [Fraction(x) for x in matriz_b_text]
            filas_b = len(matriz_b)

            if columnas_A != filas_b:
                CTkMessagebox(title="Error de formato", message=f"No se puede multiplicar A de tamaño "
                                                                f"({filas_A}x{columnas_A}) con b de tamaño ({filas_b})."
                                                                f"\nEl número de columnas de A debe ser igual al número "
                                                                f"de filas de b.",
                              icon="warning", option_1="Entendido", button_hover_color="green")
                return

        except ValueError as e:
            # Error si se intenta ingresar letras en lugar de números
            CTkMessagebox(title="Error de formato", message="Por favor, ingresa solo números válidos (sin letras).",
                          icon="warning", option_1="Entendido", button_hover_color="green")
            return

        except ZeroDivisionError:
            # Error si se intenta dividir por 0
            CTkMessagebox(title="Error de división", message="No se puede dividir por cero.", icon="warning",
                          option_1="Entendido", button_hover_color="green")
            return

        # Si todo está correcto, proceder con la operación
        self.matriz_operaciones.A = matriz_A
        self.matriz_operaciones.b = matriz_b
        self.matriz_operaciones.filas_A = filas_A
        self.matriz_operaciones.columnas_A = columnas_A
        self.matriz_operaciones.filas_b = filas_b

        self.text_salida.delete("1.0", "end")
        self.matriz_operaciones.imprimir_matrices(self.text_salida)
        self.matriz_operaciones.imprimir_solucion(self.text_salida, mostrar_pasos=False)

    def mostrar_resultado_con_pasos(self):
        """Muestra el resultado de la multiplicación y los pasos"""
        # Obtener el contenido de las entradas de texto
        matriz_A_text = self.text_matriz_A.get("1.0", "end-1c").strip()
        matriz_b_text = self.text_matriz_b.get("1.0", "end-1c").strip()

        # Verificar si alguno de los campos de entrada está vacío
        if not matriz_A_text or not matriz_b_text:
            CTkMessagebox(title="Error de entrada", message="Todos los campos deben estar llenos.", icon="warning",
                          option_1="Entendido", button_hover_color="green")
            return

        try:
            # Obtener la matriz A y calcular filas y columnas automáticamente
            matriz_A_text = matriz_A_text.split("\n")
            matriz_A = [[Fraction(x) for x in fila.split()] for fila in matriz_A_text if fila.strip()]

            filas_A = len(matriz_A)
            columnas_A = len(matriz_A[0]) if filas_A > 0 else 0

            matriz_b_text = matriz_b_text.split()
            matriz_b = [Fraction(x) for x in matriz_b_text]
            filas_b = len(matriz_b)

            if columnas_A != filas_b:
                CTkMessagebox(title="Error de Dimensiones", message=f"No se puede multiplicar A de tamaño "
                                                                    f"({filas_A}x{columnas_A}) con b de tamaño ({filas_b})."
                                                                    f"\nEl número de columnas de A debe ser "
                                                                    f"igual al número de filas de b.",
                              icon="warning", option_1="Entendido", button_hover_color="green")
                return

        except ValueError as e:
            # Error si se intenta ingresar letras en lugar de números
            CTkMessagebox(title="Error de formato", message="Por favor, ingresa solo números válidos (sin letras).",
                          icon="warning", option_1="Entendido", button_hover_color="green")
            return

        except ZeroDivisionError:
            # Error si se intenta dividir por 0
            CTkMessagebox(title="Error de división", message="No se puede dividir por cero.", icon="warning",
                          option_1="Entendido", button_hover_color="green")
            return

        # Si todo está correcto, proceder con la operación
        self.matriz_operaciones.A = matriz_A
        self.matriz_operaciones.b = matriz_b
        self.matriz_operaciones.filas_A = filas_A
        self.matriz_operaciones.columnas_A = columnas_A
        self.matriz_operaciones.filas_b = filas_b

        self.text_salida.delete("1.0", "end")
        self.matriz_operaciones.imprimir_matrices(self.text_salida)
        self.matriz_operaciones.imprimir_solucion(self.text_salida, mostrar_pasos=True)

    def clear_inputs(self):
        """Limpia todas las entradas y la salida"""
        # self.entry_nombre.delete(0, 'end')
        self.text_matriz_A.delete("1.0", "end")
        self.text_matriz_b.delete("1.0", "end")
        self.text_salida.delete("1.0", "end")


if __name__ == "__main__":
    root = ctk.CTk()
    app_frame = MultiplicacionMatricesFrame(root)
    app_frame.pack(padx=10, pady=10, fill="both", expand=True)
    root.mainloop()