import customtkinter as ctk
from utils.CTkSlideView import CTkSlideView
from PIL import Image
import os


class AcercaDeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.lista_imagenes = ["GUI/archivos_adicionales/v2.2.5.png", "GUI/archivos_adicionals/v2.8.1.png"]
        self.lista_imagenes.append("GUI/archivos_adicionals/v2.8.1.png")
        self.text = ("Calinu es un proyecto que origino dela clase de Algebra Lineal. Con el proposito de crear una "
                     "calculadora para matrices, vectores, ecuaciones lineales, funciones de raices y otras funciones\n"
                     "de una calculadora de ecuaciones numericas. Incluye herramientas de historial local al igual que"
                     "una graficadora. \n"
                     "\n"
                     "Version: 4..0: La calculadora paso por varias versiones que pueden apreciar en el carusel de "
                     "imagenes. En sus inicio comenzo como un programa manejado de consola, luego se implemento la\n"
                     "interfaz gráfica que se fue mejorando en lo que se agregaban mas funcionens. ")

        self.frame_label = ctk.CTkFrame(self)
        self.frame_label.pack(padx=10, pady=10)

        self.label = ctk.CTkLabel(self.frame_label, text=self.text, font=("Arial", 17))
        self.label.pack(padx=10, pady=10, fill="both", expand=True)

        self.carrusel = CTkSlideView(self)
        self.carrusel.pack(padx=10,pady=10)

        # Obtener la ruta al directorio raíz del proyecto
        root_dir = os.path.dirname(os.path.abspath(__file__))

        # Ruta relativa desde el contenido raíz
        imagen_primera = os.path.join(root_dir, "imagenes", "v2.2.5.png")
        imagen_segunda = os.path.join(root_dir, "imagenes", "v2.8.1.png")
        imagen_tercera = os.path.join(root_dir, "imagenes", "v3.9.4.png")

        # cargar imagenes
        imagen_primera_version = ctk.CTkImage(
            light_image=Image.open(imagen_primera),
            dark_image=Image.open(imagen_primera),
            size=(800, 400)  # Adjust size as needed
        )
        imagen_segunda_version = ctk.CTkImage(
            light_image=Image.open(imagen_segunda),
            dark_image=Image.open(imagen_segunda),
            size=(800, 400)  # Adjust size as needed
        )
        imagen_tercera_version = ctk.CTkImage(
            light_image=Image.open(imagen_tercera),
            dark_image=Image.open(imagen_tercera),
            size=(800, 400)  # Adjust size as needed
        )

        # Crear las imagenes para el carrusel
        image_label_1 = ctk.CTkLabel(self.carrusel.create_tab(), image=imagen_primera_version, text="")
        image_label_1.pack(padx=10, pady=10)
        image_label_2 = ctk.CTkLabel(self.carrusel.create_tab(), image=imagen_segunda_version, text="")
        image_label_2.pack(padx=10, pady=10)
        image_label_3 = ctk.CTkLabel(self.carrusel.create_tab(), image=imagen_tercera_version, text="")
        image_label_3.pack(padx=10, pady=10)


# ejemplo de uso
class EjemploUso(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Matrices y Vectores")
        self.geometry("800x600")

        # Inicializa la frame de CalculadoraFuncionApp
        self.calculadora_frame = AcercaDeFrame(self)
        self.calculadora_frame.pack(fill="both", expand=True)


# Ejecución de la aplicación
if __name__ == "__main__":
    app = EjemploUso()
    app.mainloop()
