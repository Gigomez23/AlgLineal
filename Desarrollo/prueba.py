import customtkinter as ctk

# Clase principal de la aplicación
class Aplicacion(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("App con Evento Personalizado")
        self.geometry("400x300")

        # Botón que genera el evento personalizado
        self.boton_evento = ctk.CTkButton(self, text="Generar Evento Personalizado", command=self.generar_evento_personalizado)
        self.boton_evento.pack(pady=20)

        # Etiqueta para mostrar mensajes
        self.label_mensaje = ctk.CTkLabel(self, text="Esperando el evento...")
        self.label_mensaje.pack(pady=20)

        # Botón para activar el evento personalizado manualmente
        self.boton_activar = ctk.CTkButton(self, text="Activar Evento", command=self.activar_evento)
        self.boton_activar.pack(pady=20)

        # Enlaza el evento personalizado con una función manejadora
        self.bind("<<EventoPersonalizado>>", self.manejador_evento_personalizado)

    def generar_evento_personalizado(self):
        """Genera un evento personalizado que puede ser manejado."""
        print("Generando evento personalizado...")
        # Genera un evento personalizado con nombre "<<EventoPersonalizado>>"
        self.event_generate("<<EventoPersonalizado>>")

    def manejador_evento_personalizado(self, event):
        """Función que maneja el evento personalizado."""
        print("Evento personalizado activado!")
        self.label_mensaje.configure(text="¡Evento personalizado activado!")

    def activar_evento(self):
        """Otra forma de manejar el evento sin usar el botón."""
        print("Activando el evento manualmente...")
        self.manejador_evento_personalizado(None)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Opcional, modo de apariencia
    ctk.set_default_color_theme("blue")  # Opcional, tema de color
    app = Aplicacion()
    app.mainloop()
