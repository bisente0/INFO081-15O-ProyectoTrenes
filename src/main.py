# Importamos los módulos necesarios
import tkinter as tk             
from tkinter import messagebox   # Para mostrar mensajes emergentes
import json                     # Para leer archivos con configuraciones (JSON)
import os             
from core.ui import *


def cargar_configuracion():

    #Abre y lee los archivos de configuración que están en la carpeta 'config'.
    #Devuelve dos diccionarios: uno para tamaño de ventana y otro para colores.

    try:
        # Abrimos y leemos el archivo settings.json
        with open(os.path.join("data" ,"config" , "settings.json"), "r", encoding="utf-8") as f:
            settings = json.load(f)

        # Abrimos y leemos el archivo colors.json
        with open(os.path.join("data", "config", "colors.json"), "r", encoding="utf-8") as f:
            colors = json.load(f)

        return settings, colors
    except FileNotFoundError as e:
        # Si falta un archivo, mostramos un error
        messagebox.showerror("Error", f"No se encontró el archivo de configuración: {e}")
        return None, None
    except json.JSONDecodeError as e:
        # Si hay un error de formato en el JSON, avisamos
        messagebox.showerror("Error", f"Error al leer el archivo JSON: {e}")
        return None, None

def crear_interfaz_principal(settings, colors):
    
    #Aquí se arma la ventana usando tkinter, usando los parámetros de configuración.
    
    # Se inicia la ventana principal de tkinter
    root = tk.Tk()
    root.title("Simulación de Trenes - EFE Chile")

    # Se define el tamaño y color de fondo
    root.geometry(f"{settings['ancho']}x{settings['alto']}")
    root.configure(bg=colors["fondo"])

    # Se crean y colocan los widgets (elementos visuales)
    # Frame principal
    frame_principal = tk.Frame(root, bg=colors["fondo"])
    frame_principal.pack(expand=True, fill="both", padx=20, pady=20)

    # Etiqueta principal (título)
    titulo = tk.Label(
        frame_principal,
        text="Sistema de Simulación de Trenes",
        font=("Arial", 24, "bold"),
        bg=colors["fondo"],
        fg=colors["principal"]
    )
    titulo.pack(pady=20)

    # Subtítulo
    subtitulo = tk.Label(
        frame_principal,
        text="Empresa de Ferrocarriles del Estado (EFE) - Chile",
        font=("Arial", 14),
        bg=colors["fondo"],
        fg=colors["secundario"]
    )
    subtitulo.pack(pady=10)

    # Información adicional
    info = tk.Label(
        frame_principal,
        text="Proyecto de Programación - INFO081\nSegunda Entrega - Sistema de Módulos",
        font=("Arial", 12),
        bg=colors["fondo"],
        fg=colors["texto"]
    )
    info.pack(pady=20)

    # Botón de ejemplo
    boton_iniciar = tk.Button(
        frame_principal,
        text="Iniciar Simulación",
        font=("Arial", 12, "bold"),
        bg=colors["principal"],
        fg="#FFFFFF",
        padx=20,
        pady=10,
        command=lambda: messagebox.showinfo("Info", "Funcionalidad en desarrollo por el equipo")
    )
    boton_iniciar.pack(pady=20)

    # Pie de página
    footer = tk.Label(
        frame_principal,
        text="© 2025 - Proyecto Colaborativo en GitHub",
        font=("Arial", 10),
        bg=colors["fondo"],
        fg=colors["secundario"]
    )
    footer.pack(side="bottom", pady=10)

    return root


def main():
    
    #Esta función es el punto de inicio del programa.
    #Lee las configuraciones e inicia la ventana principal.


    settings, colors = cargar_configuracion()


    if settings is None or colors is None:
        print("Error: No se pudieron cargar las configuraciones.")
        return
    
    root = crear_interfaz_principal(settings, colors)
    root.mainloop()


if __name__ == "__main__":
    main()  


