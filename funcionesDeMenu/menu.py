"""
Archivo: menu 1.3
Descripcion: Archivo que contiene el menu y sus metodos.
Crea el menu y sus opciones.
"""
from consolemenu import *
from consolemenu.items import *
from funcionesDeMenu.funcionesMenu import *
from consolemenu.menu_component import Dimension

menu_format = MenuFormatBuilder()
menu_format.set_title_align('center')                   # Center the menu title (by default it's left-aligned)
menu_format.set_subtitle_align('center')

# Se crea el menu como objeto
menuPrincipal = ConsoleMenu("Calculadora de Matrices", "Digite una opcion para crear y encontrar "
                                                       "la matriz identidad de una matriz "
                                                       "aleatoria o hecha manualmente.",
                             clear_screen=True, exit_option_text="Salir", exit_menu_char="0")
menuPrincipal.formatter = menu_format

# Se crea las opcoines que se van a presentar en el menu
opcion_matriz_aleatoria = FunctionItem("Resolver matriz creada de forma aleatoria.", matriz_aleatoria)
opcion_matriz_manual = FunctionItem("Resolver matriz aumentada ingresada manualmente.", matriz_manul)
opcion_sistema_ecuaciones = FunctionItem("Resolver sistema de ecuaciones con matriz reducida. ", matriz_reducida)
opcion_historial_matriz = FunctionItem("Escoger una matriz del historial.", imprimir_historial)

# se agregan las opciones al menu
menuPrincipal.append_item(opcion_matriz_aleatoria)
menuPrincipal.append_item(opcion_matriz_manual)
menuPrincipal.append_item(opcion_sistema_ecuaciones)
menuPrincipal.append_item(opcion_historial_matriz)

