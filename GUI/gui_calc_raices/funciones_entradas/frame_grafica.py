"""
Archivo: frame_grafica.py 1.2.2
Descripción: Este archivo contiene la interfáz gráfica mejorada con zoom, paneo y más puntos en la gráfica.
"""
import re
import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, sympify, lambdify
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from CTkMessagebox import CTkMessagebox


class GraficarFuncionFrame(ctk.CTkFrame):
    def __init__(self, master, textbox):
        super().__init__(master)
        self.textbox = textbox
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(pady=10, padx=10, fill="both", expand=True, side="left")

        self.botones_frame = ctk.CTkFrame(self)
        self.botones_frame.pack(pady=10, padx=10, expand=True, side="right", fill="y")

        self.boton_graficar = ctk.CTkButton(self.botones_frame, text="Graficar Función", command=self.graficar_funcion)
        self.boton_graficar.pack(pady=10)

        # Inicializar canvas, toolbar, marcador y botón
        self.canvas = None
        self.toolbar = None
        self.marcador = None
        self.boton_quitar_marcador = None

    def obtener_funcion(self):
        """Convierte la expresión ingresada en el textbox a una función entendible por Python."""
        expresion = self.textbox.get()

        # Reemplazar superíndices y operadores de potencia
        expresion = expresion.replace('²', '**2').replace('³', '**3').replace('⁴', '**4').replace('⁵', '**5') \
            .replace('⁶', '**6').replace('⁷', '**7').replace('⁸', '**8').replace('⁹', '**9') \
            .replace('⁰', '**0')   # Operador ^ por **

        # Reemplazar funciones trigonométricas en español por las equivalentes en inglés
        expresion = expresion.replace('sen', 'sin')
        expresion = expresion.replace('cos', 'cos')
        expresion = expresion.replace('tan', 'tan')
        expresion = expresion.replace('sec', 'sec')

        # Agregar multiplicación implícita donde sea necesario
        expresion = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expresion)  # Ejemplo: 2x -> 2*x, 2(x+1) -> 2*(x+1)

        x = symbols('x')  # Definir el símbolo 'x'

        try:
            # Convertir la expresión a formato simbólico
            funcion_simb = sympify(expresion)
            # Convertir la expresión simbólica a una función numérica para graficar
            funcion_numerica = lambdify(x, funcion_simb, modules=['numpy'])
            return funcion_numerica
        except Exception as e:
            raise ValueError(f"Error al interpretar la función: {e}")

    def graficar_funcion(self):
        try:
            # Obtener la función en formato numérico
            funcion = self.obtener_funcion()

            # Generar puntos para graficar en un rango amplio
            x_vals = np.linspace(-100, 100, 2000)
            y_vals = funcion(x_vals)

            # Crear la figura y personalizar la apariencia con tema oscuro
            fig, ax = plt.subplots(figsize=(8, 6), facecolor='#2e2e2e')
            ax.plot(x_vals, y_vals, label=f"f(x)={funcion}", color='#00bcd4', linewidth=2)
            ax.set_title("Gráfica de la Función", fontsize=16, fontweight='bold', color='white')
            ax.set_xlabel("x", fontsize=14, color='white')
            ax.set_ylabel("f(x)", fontsize=14, color='white')
            ax.tick_params(axis='x', colors='white', labelsize=12)
            ax.tick_params(axis='y', colors='white', labelsize=12)
            ax.set_facecolor('#121212')
            ax.grid(True, linestyle='--', color='gray', alpha=0.5)
            ax.legend(frameon=False, loc='best', fontsize=12, labelcolor='white')
            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)

            # Variables para gestionar clics y arrastres
            self.is_dragging = False

            def on_button_press(event):
                self.is_dragging = False

            def on_motion(event):
                if event.button == 1:
                    self.is_dragging = True

            def on_click(event):
                if event.inaxes != ax or self.is_dragging:
                    return
                x_click = event.xdata
                try:
                    y_click = funcion(x_click)
                    idx_cercano = np.abs(x_vals - x_click).argmin()
                    x_cercano, y_cercano = x_vals[idx_cercano], y_vals[idx_cercano]

                    # Eliminar marcador previo, si existe
                    if self.marcador:
                        self.marcador.remove()

                    # Dibujar nuevo marcador
                    self.marcador, = ax.plot(x_cercano, y_cercano, 'ro', markersize=8,
                                             label=f'({x_cercano:.2f}, {y_cercano:.2f})')
                    ax.legend(frameon=False, loc='best', fontsize=12, labelcolor='white')
                    fig.canvas.draw()
                except Exception:
                   pass

            def quitar_marcador():
                """Eliminar el marcador actual si existe."""
                if self.marcador:
                    self.marcador.remove()
                    self.marcador = None
                    fig.canvas.draw()


            # Conectar eventos del mouse
            fig.canvas.mpl_connect('button_press_event', on_button_press)
            fig.canvas.mpl_connect('motion_notify_event', on_motion)
            fig.canvas.mpl_connect('button_release_event', on_click)

            # Limpiar canvas, toolbar y marcador anteriores
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
            if self.toolbar:
                self.toolbar.destroy()
            if self.marcador:
                self.marcador.remove()
                self.marcador = None
            if self.boton_quitar_marcador:
                self.boton_quitar_marcador.destroy()
                self.boton_quitar_marcador = None

            # Mostrar nueva gráfica
            self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.canvas_frame)
            self.toolbar.update()
            self.toolbar.pack(side="top", fill="x")

            # Crear el botón de quitar marcador
            self.boton_quitar_marcador = ctk.CTkButton(self.botones_frame, text="Quitar Marcador", command=quitar_marcador)
            self.boton_quitar_marcador.pack(pady=10)

            def zoom_out():
                """Aumenta el rango visible de los ejes para hacer zoom out."""
                x_min, x_max = ax.get_xlim()
                y_min, y_max = ax.get_ylim()
                factor = 1.5  # Factor de zoom out (aumenta el rango en 50%)
                ax.set_xlim(x_min * factor, x_max * factor)
                ax.set_ylim(y_min * factor, y_max * factor)
                fig.canvas.draw()  # Actualizar la gráfica

            # Crear el botón de Zoom Out
            boton_zoom_out = ctk.CTkButton(self.botones_frame, text="Zoom Out", command=zoom_out)
            boton_zoom_out.pack(pady=5)


        except ValueError as ve:

            CTkMessagebox(title="Error", message=f"{ve}", icon="cancel")

        except Exception as e:

            CTkMessagebox(title="Error", message=f"Error al graficar la función: {e}", icon="cancel")

            print("Error al graficar la función:", e)

    def destroy(self):
        # Cancelar tareas pendientes programadas
        if hasattr(self, '_after_id') and self._after_id is not None:
            self.after_cancel(self._after_id)

        # Cerrar cualquier figura de Matplotlib para liberar recursos
        plt.close('all')

        # Asegurarse de destruir el canvas y la barra de herramientas
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        if self.toolbar:
            self.toolbar.destroy()

        super().destroy()


