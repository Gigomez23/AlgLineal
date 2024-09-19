"""
Archivo: menu.py 1.6.2
Descripcion: Archivo que contiene el menu y sus metodos.
Crea el menu y sus opciones.
"""
from consolemenu import *
from consolemenu.items import *
from funcionesDeMenu.funcionesMenu import *
from consolemenu.menu_component import Dimension

# se crea un objeto para formatear el menu
menu_format = MenuFormatBuilder()
menu_format.set_title_align('center')
menu_format.set_subtitle_align('center')

# Se crea el menu como objeto
menuPrincipal = ConsoleMenu("Calculadora de Matrices", "Calculadora para resolver sistema "
                                                       "de ecuaciciones y operaciones entre matrices. \n"
                                                       "Digite su selección. ",

                            clear_screen=True, exit_option_text="Salir")
menuPrincipal.formatter = menu_format

# Se crea las opcoines que se van a presentar en el menu
opcion_matriz_aleatoria = FunctionItem("Resolver matriz creada de forma aleatoria.", matriz_aleatoria)
opcion_matriz_manual = FunctionItem("Resolver matriz aumentada ingresada manualmente.", matriz_manul)
opcion_sistema_ecuaciones = FunctionItem("Resolver sistema de ecuaciones "
                                         "por metodo escalonado. ", matriz_reducida)
opcion_operaciones_matrices = FunctionItem("Multiplicar Matriz por vector. "
                                           "(Ecuación Matricial)", matriz_operacion)
opcion_historial_matriz = FunctionItem("Ver historial.", imprimir_historial)

# se agregan las opciones al menu
menuPrincipal.append_item(opcion_matriz_aleatoria)
menuPrincipal.append_item(opcion_matriz_manual)
menuPrincipal.append_item(opcion_sistema_ecuaciones)
menuPrincipal.append_item(opcion_operaciones_matrices)
menuPrincipal.append_item(opcion_historial_matriz)
