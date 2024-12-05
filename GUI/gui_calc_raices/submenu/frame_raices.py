"""
Archivo: frame_raices.py 1.1.1
Descripción: Este archivo contiene la interfáz gráfica para los metodos de resolucion de raices.
"""
from CTkToolTip import *
from ctkcomponents import *
from utils.ctk_xyframe import *
from GUI.gui_calc_raices.funciones_entradas.frame_entrada_funcion import CalculadoraCientificaFrame
from GUI.gui_calc_raices.funciones_entradas.frame_grafica import *
from GUI.gui_calc_raices.calculadoras.secante_resolve import *
from GUI.gui_calc_raices.calculadoras.newton_raphston_resolve import *
from GUI.gui_calc_raices.calculadoras.falsa_possicion_bissecio_resolve import *


class FrameRaices(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.frame_general = CTkXYFrame(master=self)
        self.frame_general.pack(fill="both", expand=True, padx=10, pady=10)

        self.frame_superior = ctk.CTkFrame(self.frame_general)
        self.frame_superior.pack(padx=10, pady=10, expand=True, fill="both")

        self.frame_inferior = ctk.CTkFrame(self.frame_general)
        self.frame_inferior.pack(padx=10, pady=10, expand=True, fill="both")

        # se crean frames para estructura general del programa
        self.frame_de_entradas = ctk.CTkFrame(self.frame_superior)
        self.frame_de_entradas.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self.frame_de_botones = ctk.CTkFrame(self.frame_inferior)
        self.frame_de_botones.grid(row=1, columnspan=3, sticky="nsew")

        # entries y botones de entrada
        ctk.CTkLabel(self.frame_de_entradas, text="Funcion f(x):", font=("Arial", 17)).grid(row=0, column=0, padx=10,
                                                                                            pady=10, sticky='n')
        self.entrada_de_funcion = ctk.CTkEntry(self.frame_de_entradas, width=200, font=("Arial", 15))
        self.entrada_de_funcion.grid(row=0, column=1, padx=10, pady=10, sticky='n')
        self.tooltip_entry_funcion = CTkToolTip(self.entrada_de_funcion,
                                                message="Presione shift para salir del modo exponencial. ",
                                                follow=False)

        self.btn_recomendacion = ctk.CTkButton(self.frame_de_entradas, text="I", command=self.recomendar_metodo,
                                               font=("Georgia", 17), width=50)
        self.btn_recomendacion.grid(row=0, column=2, pady=10, padx=10, sticky='n')
        self.tooltip_recomendacion = CTkToolTip(self.btn_recomendacion, message="Presione para recibir una "
                                                                                "recomendación de que metodo "
                                                                                "utilizar para resolver.", follow=False)

        ctk.CTkLabel(self.frame_de_entradas, text="Intervalo inferior (Xi):", font=("Arial", 17)).grid(row=1, column=0,
                                                                                                       padx=10, pady=10)

        self.entry_xi = ctk.CTkEntry(self.frame_de_entradas, width=200, font=("Arial", 15))
        self.entry_xi.grid(row=1, column=1, padx=10, pady=10)
        self.tooltip_valor_inicial = CTkToolTip(self.entry_xi, message="Valor Inicial", follow=False)

        ctk.CTkLabel(self.frame_de_entradas, text="Intervalo superior (Xu):", font=("Arial", 17)).grid(row=2, column=0,
                                                                                                       padx=10, pady=10)

        self.entry_xu = ctk.CTkEntry(self.frame_de_entradas, width=200, font=("Arial", 15))
        self.entry_xu.grid(row=2, column=1, padx=10, pady=10)
        self.tooltip_valor_opcional = CTkToolTip(self.entry_xu, message="Esta entrada es opcional si va a resolver"
                                                                        "por metodo de Newton-Raphston", follow=False)

        ctk.CTkLabel(self.frame_de_entradas, text="Error de tolerancia:", font=("Arial", 17)).grid(row=3, column=0,
                                                                                                   padx=10, pady=10)
        self.entry_error_tol = ctk.CTkEntry(self.frame_de_entradas, width=200, font=("Arial", 15))
        self.entry_error_tol.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.frame_de_entradas, text="Máximo de iteraciones (opcional):", font=("Arial", 17)).grid(row=4,
                                                                                            column=0, padx=10, pady=10)
        self.entry_max_iter = ctk.CTkEntry(self.frame_de_entradas, width=200)
        self.entry_max_iter.grid(row=4, column=1, padx=10, pady=10)

        # Menú de selección del tipo de calculadora
        self.menu_metodo_res = ctk.CTkOptionMenu(
            master=self.frame_de_entradas,
            values=['Método de Falsa Posición', 'Método de Bisección', 'Método de Newton Raphson', 'Método de Secante'],
            anchor="w",
            width=250,
            hover=True
        )
        self.menu_metodo_res.grid(row=5, column=0, padx=10, pady=20)
        self.tooltip_seleccion = CTkToolTip(self.menu_metodo_res,
                                            message="Seleccione el método con el que desea resolver",
                                            follow=False)

        # botón para limpiar entradas
        self.boton_limpiar = ctk.CTkButton(self.frame_de_entradas, text="Limpiar", command=self.limpiar_entradas,
                                           font=("Georgia", 15))
        self.boton_limpiar.grid(row=5, column=1, pady=20)

        self.btn_resolver = ctk.CTkButton(self.frame_de_entradas, text="Resolver", command=self.resolver,
                                           font=("Georgia", 15))
        self.btn_resolver.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

        self.frame_de_grafica = GraficarFuncionFrame(self.frame_superior, self.entrada_de_funcion)
        self.frame_de_grafica.grid(row=0, column=1, columnspan=2, sticky='nse', padx=10, pady=10)

        # Crear el frame de la calculadora científica
        self.calculadora_cientifica_frame = CalculadoraCientificaFrame(self.frame_de_botones, self.entrada_de_funcion)
        self.calculadora_cientifica_frame.pack(pady=10, fill="both", expand=True)

    def recomendar_metodo(self):
        """
        Método que analiza la función ingresada y recomienda el método más eficiente para resolverla.
        """
        try:
            # Obtener la función desde el cuadro de texto
            funcion_texto = self.calculadora_cientifica_frame.obtener_funcion()
            funcion = sp.sympify(funcion_texto)  # Convertir texto a función simbólica

            # Leer entradas del intervalo y parámetros
            xi = float(self.entry_xi.get())
            xu = float(self.entry_xu.get())

            # Verificar que Xi y Xu sean válidos
            if xi >= xu:
                raise ValueError("El intervalo inferior debe ser menor que el superior.")

            # Evaluar la función en los extremos del intervalo
            f_xi = funcion.evalf(subs={sp.symbols('x'): xi})
            f_xu = funcion.evalf(subs={sp.symbols('x'): xu})

            # Verificar cambio de signo
            if f_xi * f_xu < 0:
                # Cambio de signo → Recomendación Bisección/Falsa Posición
                metodo = "Método de Bisección o Falsa Posición"
            else:
                # Verificar derivada para métodos basados en derivadas
                derivada = sp.diff(funcion, sp.symbols('x'))
                derivada_xi = derivada.evalf(subs={sp.symbols('x'): xi})
                derivada_xu = derivada.evalf(subs={sp.symbols('x'): xu})

                if derivada_xi != 0 and derivada_xu != 0:
                    # Si la derivada no es cero → Recomendación Newton-Raphson
                    metodo = "Método de Newton-Raphson"
                else:
                    # Último recurso → Método de Secante
                    metodo = "Método de Secante"

            # Mostrar recomendación
            CTkNotification(master=self, state="info",
                            message=f"El método más eficiente para \nresolver este problema sería: {metodo}",
                            side="right_bottom")

        except ValueError as ve:
            CTkMessagebox(title="Error", message=str(ve), icon="warning")
        except Exception as e:
            CTkMessagebox(title="Error inesperado",
                          message=f"Ocurrió un error al analizar la función: {str(e)}",
                          icon="warning")

    def resolver(self):
        seleccion = self.menu_metodo_res.get()
        if seleccion == "Método de Falsa Posición":
            print("Metodo de falsa posicion")
            self.calcular_por_falsa_pos()
        elif seleccion == "Método de Bisección":
            self.calcular_por_bissecion()
        elif seleccion == "Método de Newton Raphson":
            self.calcular_por_newt_raphston()
        elif seleccion == "Método de Secante":
            self.calcular_por_secante()

    def calcular_por_falsa_pos(self):
        try:
            expr_latex = self.calculadora_cientifica_frame.obtener_funcion()
            xi = float(self.entry_xi.get())
            xu = float(self.entry_xu.get())
            error_tol = float(self.entry_error_tol.get())
            max_iter = int(self.entry_max_iter.get()) if self.entry_max_iter.get() else 100

            # Llamar a la función externa para calcular el método de Falsa Posición
            iteraciones, xr, converged = calcular_falsa_posicion(expr_latex, xi, xu, error_tol, max_iter)

            # Mostrar los resultados usando la función externa
            mostrar_resultados(iteraciones, xr, converged, "Falsa Posición")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Ocurrió un error: {str(e)}", icon="warning", fade_in_duration=2)

    def calcular_por_bissecion(self):
        try:
            expr_latex = self.calculadora_cientifica_frame.obtener_funcion()
            xi = float(self.entry_xi.get())
            xu = float(self.entry_xu.get())
            error_tol = float(self.entry_error_tol.get())
            max_iter = int(self.entry_max_iter.get()) if self.entry_max_iter.get() else 100

            # Llamar a la función externa para calcular el método de Bisección
            iteraciones, xr, converged = calcular_biseccion(expr_latex, xi, xu, error_tol, max_iter)

            # Mostrar los resultados usando la función externa
            mostrar_resultados(iteraciones, xr, converged, "Bisección")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Ocurrió un error: {str(e)}", icon="warning", fade_in_duration=2)

    def calcular_por_newt_raphston(self):
        try:
            expr_texto = self.calculadora_cientifica_frame.obtener_funcion()
            x0 = float(self.entry_xi.get())
            error_tol = float(self.entry_error_tol.get())
            max_iter = int(self.entry_max_iter.get()) if self.entry_max_iter.get() else 100

            # Llamar a la función externa para calcular el método de Newton-Raphson
            iteraciones, raiz, converged = calcular_newton_raphson(expr_texto, x0, error_tol, max_iter)

            # Mostrar los resultados usando la función externa
            mostrar_resultados_newton(iteraciones, raiz, converged, self)

        except ValueError as e:
            CTkMessagebox(title="Error", message=f"Ocurrió un error: {str(e)}", icon="warning", fade_in_duration=2)

    def calcular_por_secante(self):
        # Llamamos a la función calcular_secante
        funcion_str = self.calculadora_cientifica_frame.obtener_funcion()
        x0 = self.entry_xi.get()
        x1 = self.entry_xu.get()
        tolerancia = self.entry_error_tol.get()
        max_iter = self.entry_max_iter.get()

        iteraciones, raiz, convergencia = calcular_secante(funcion_str, x0, x1, tolerancia, max_iter)
        if iteraciones:  # Si el cálculo fue exitoso
            mostrar_resultados_secante(iteraciones, raiz, convergencia)

    def limpiar_entradas(self):
        self.entrada_de_funcion.delete(0, END)
        self.entry_xi.delete(0, END)
        self.entry_xu.delete(0, END)
        self.entry_max_iter.delete(0, END)
        self.entry_error_tol.delete(0, END)


# ejemplo de uso
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("900x600")
    app.title("Métodos de Raíces")
    FrameRaices(app).pack(fill="both", expand=True)
    app.mainloop()


