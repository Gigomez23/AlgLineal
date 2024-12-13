import customtkinter as ctk
from GUI.acerca_de.acerca_de_frame import AcercaDeFrame
from GUI.acerca_de.sobre_autores import SobreAutoresFrame


class AcercaDeApp(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Acerca De")
        self.geometry("800x600")

        # Configuración del marco principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Tabs laterales
        self.tab_frame = ctk.CTkFrame(self, width=200)
        self.tab_frame.grid(row=0, column=0, sticky="ns")

        # Crear el contenedor de contenido
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Crear frames de contenido
        self.frames = {
            "Acerca De": AcercaDeFrame(self.content_frame),
            "Sobre Autores": SobreAutoresFrame(self.content_frame)
        }

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        # Tabs y acciones
        for index, tab_name in enumerate(self.frames.keys()):
            tab_button = ctk.CTkButton(
                self.tab_frame, text=tab_name, command=lambda name=tab_name: self.cambiar_frame(name)
            )
            tab_button.grid(row=index, column=0, pady=10, padx=10, sticky="ew")

        # Mostrar contenido inicial
        self.cambiar_frame("Acerca De")

    def cambiar_frame(self, frame_name):
        """Cambia el contenido visible en el área de contenido."""
        for frame in self.frames.values():
            frame.grid_remove()
        self.frames[frame_name].grid()


class ManualDeUsoFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Manual de Uso:\n\n1. Navega por las opciones.\n"
                                        "2. Realiza operaciones según las instrucciones.")
        label.pack(padx=10, pady=10, fill="both", expand=True)


if __name__ == "__main__":
    app = AcercaDeApp()
    app.mainloop()
