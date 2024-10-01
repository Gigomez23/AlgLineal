"""
Archivo: Au_Ax_calc.py 1.1.0
Descripción: diseño de frame para gui de problemas tipo de Au + Av
"""
from fractions import Fraction
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from models.clase_matriz_vectores import *


class CalculadoraDeMatrizxVectoresFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.matriz_operaciones = CreadorDeOperacionMatrizVector()

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

        self.text_matriz_A = ctk.CTkTextbox(self.frame_izquierdo, width=300, height=100)
        self.text_matriz_A.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        self.label_vector_u = ctk.CTkLabel(self.frame_izquierdo,
                                           text="Vector u (valores separados por espacios):")
        self.label_vector_u.grid(row=3, column=0, padx=10, pady=10, columnspan=2, sticky="w")

        self.text_vector_u = ctk.CTkTextbox(self.frame_izquierdo, width=300, height=50)
        self.text_vector_u.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

        self.label_vector_v = ctk.CTkLabel(self.frame_izquierdo,
                                           text="Vector v (valores separados por espacios):")
        self.label_vector_v.grid(row=5, column=0, padx=10, pady=10, columnspan=2, sticky="w")

        self.text_vector_v = ctk.CTkTextbox(self.frame_izquierdo, width=300, height=50)
        self.text_vector_v.grid(row=6, column=0, padx=10, pady=10, columnspan=2)

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
                          option_1="Entendido", button_hover_color="green")
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
                          button_hover_color="green")
            return
        except ZeroDivisionError:
            # Mensaje de error si el usuario intenta dividir por 0
            CTkMessagebox(title="Error de división", message="No se puede dividir por cero.", icon="warning",
                          option_1="Entendido", button_hover_color="green")
            return
        except Exception:
            # Mensaje de error por entradas no numéricas
            CTkMessagebox(title="Error de entrada",
                          message="Por favor, ingresa solo números válidos (sin letras ni símbolos).", icon="warning",
                          option_1="Entendido", button_hover_color="green")
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

    def clear_inputs(self):
        """Limpia los campos de entrada y salida"""
        self.text_matriz_A.delete("1.0", "end")
        self.text_vector_u.delete("1.0", "end")
        self.text_vector_v.delete("1.0", "end")
        self.text_salida.delete("1.0", "end")


# Ejemplo de uso del frame en una aplicación principal de tkinter
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x400")
    root.title("Calculadora de Ecuaciones Matriciales")

    frame = CalculadoraDeMatrizxVectoresFrame(root)
    frame.pack(fill="both", expand=True)

    root.mainloop()