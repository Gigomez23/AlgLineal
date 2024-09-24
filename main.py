"""
Programa Versión:  3.1.0
Descripcion: archivo main
Clase: Algebra Lineal
Integrantes: Gabriel Gómez, Gessler Herrera, Gabriel Lacayo, Oliver Espinoza
"""

#todo: verificar todas las instrucciones
from main_gui import App

if __name__ == "__main__":
    root = App()
    root.geometry("1000x800")
    root.title("Calculadora Algebra Lineal")
    root.configure(fg_color=['gray92', 'gray14'])
    root.mainloop()

    #just a test