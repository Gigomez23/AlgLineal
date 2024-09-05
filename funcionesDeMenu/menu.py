"""
Archivo: menu 1.3
Descripcion: Archivo que contiene el menu y sus metodos.
Crea el menu y sus opciones.
"""
from consolemenu import *
from consolemenu.items import *
from funcionesDeMenu.funcionesMenu import *

# Se crea el menu como objeto
menuPrincipal = ConsoleMenu("Calculadora de Matrices", "Digite una opcion para crear y encontrar "
                                                       "la matriz identidad de una matriz "
                                                       "aleatoria o hecha manualmente.",
                             exit_option_text="Salir", exit_menu_char="0")

# Se crea las opcoines que se van a presentar en el menu
opcion_matriz_aleatoria = FunctionItem("Crear matriz de forma aleatoria.", matriz_aleatoria)
opcion_matriz_manual = FunctionItem("Crear matriz manualmente.", matriz_manul)
opcion_historial_matriz = FunctionItem("Escoger una matriz del historial.", imprimir_historial)

# se agregan las opciones al menu
menuPrincipal.append_item(opcion_matriz_aleatoria)
menuPrincipal.append_item(opcion_matriz_manual)
menuPrincipal.append_item(opcion_historial_matriz)

