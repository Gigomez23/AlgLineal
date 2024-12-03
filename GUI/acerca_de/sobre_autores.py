import customtkinter as ctk
from utils.CTkSlideView import CTkSlideView
from PIL import Image
import os

class SobreAutoresFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.lista_imagenes = ["GUI/archivos_adicionales/v2.2.5.png", "GUI/archivos_adicionals/v2.8.1.png"]
        self.lista_imagenes.append("GUI/archivos_adicionals/v2.8.1.png")
        self.text = ("Este programa fue desarrollado por un grupo de estudiante de la clase de Algebra Linea. \n"
                     "Gabriel Gómez, Gabriel Lacayo, Gessler Herrera, Oliver Espinoza.\n"
                     "Apoyo: ChatGPT (Alias el Mata burro)\n"
                     "Retroalimentacion y guía del proyecto: Prof. Ivan Arguello")

        self.frame_label = ctk.CTkFrame(self)
        self.frame_label.pack(padx=10, pady=10)

        self.label = ctk.CTkLabel(self.frame_label, text=self.text, font=("Arial", 17))
        self.label.pack(padx=10, pady=10, fill="both", expand=True)

        self.carrusel = CTkSlideView(self)
        self.carrusel.pack(padx=10, pady=10)

        # Obtener la ruta al directorio raíz del proyecto
        root_dir = os.path.dirname(os.path.abspath(__file__))

        # Ruta relativa desde el contenido raíz
        imagen_gabriel = os.path.join(root_dir, "imagenes", "gomez.jpg")
        imagen_gessler = os.path.join(root_dir, "imagenes", "Gessler.jpg")
        imagen_lacayo = os.path.join(root_dir, "imagenes", "Lacayo.jpg")
        imagen_oliver = os.path.join(root_dir, "imagenes", "Oliver.jpg")
        imagen_gpt = os.path.join(root_dir, "imagenes", "gpt.png")
        imagen_profe_ivan = os.path.join(root_dir, "imagenes", "profe.jpg")

        # cargar imagenes
        imagen_de_gabriel = ctk.CTkImage(
            light_image=Image.open(imagen_gabriel),
            dark_image=Image.open(imagen_gabriel),
            size=(800, 400)  # Adjust size as needed
        )
        imagen_de_gessler = ctk.CTkImage(
            light_image=Image.open(imagen_gessler),
            dark_image=Image.open(imagen_gessler),
            size=(800, 400)  # Adjust size as needed
        )
        imagen_de_lacayo = ctk.CTkImage(
            light_image=Image.open(imagen_lacayo),
            dark_image=Image.open(imagen_lacayo),
            size=(800, 400)  # Adjust size as needed
        )
        imagen_de_oliver = ctk.CTkImage(
            light_image=Image.open(imagen_oliver),
            dark_image=Image.open(imagen_oliver),
            size=(800, 400)  # Adjust size as needed
        )
        imagen_de_gpt = ctk.CTkImage(
            light_image=Image.open(imagen_gpt),
            dark_image=Image.open(imagen_gpt),
            size=(800, 400)  # Adjust size as needed
        )
        imagen_de_profe = ctk.CTkImage(
            light_image=Image.open(imagen_profe_ivan),
            dark_image=Image.open(imagen_profe_ivan),
            size=(800, 400)  # Adjust size as needed
        )

        # Crear las imagenes para el carrusel
        image_label_1 = ctk.CTkLabel(self.carrusel.create_tab(), image=imagen_de_gabriel, text="")
        image_label_1.pack(padx=10, pady=10)
        image_label_2 = ctk.CTkLabel(self.carrusel.create_tab(), image=imagen_de_lacayo, text="")
        image_label_2.pack(padx=10, pady=10)
        image_label_3 = ctk.CTkLabel(self.carrusel.create_tab(), image=imagen_de_gessler, text="")
        image_label_3.pack(padx=10, pady=10)
        image_label_4 = ctk.CTkLabel(self.carrusel.create_tab(), image=imagen_de_oliver, text="")
        image_label_4.pack(padx=10, pady=10)
        image_label_5 = ctk.CTkLabel(self.carrusel.create_tab(), image=imagen_de_gpt, text="")
        image_label_5.pack(padx=10, pady=10)
        image_label_6 = ctk.CTkLabel(self.carrusel.create_tab(), image=imagen_de_profe, text="")
        image_label_6.pack(padx=10, pady=10)

# ejemplo de uso
class EjemploUso(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Matrices y Vectores")
        self.geometry("800x600")

        # Inicializa la frame de CalculadoraFuncionApp
        self.calculadora_frame = SobreAutoresFrame(self)
        self.calculadora_frame.pack(fill="both", expand=True)


# Ejecución de la aplicación
if __name__ == "__main__":
    app = EjemploUso()
    app.mainloop()
