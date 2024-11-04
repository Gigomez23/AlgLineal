"""
Programa Versión:  4.0.0 beta
Descripcion: archivo main
Clase: Algebra Lineal
Integrantes: Gabriel Gómez, Gessler Herrera, Gabriel Lacayo, Oliver Espinoza
"""
from main_gui import PantallaInicio


if __name__ == "__main__":
    root = PantallaInicio()
    root.geometry("1200x800")
    root.title("Calculadora de Álgebra Lineal")
    root.mainloop()
