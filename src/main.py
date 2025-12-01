import tkinter as tk
from tkinter import messagebox
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sim_global = None
label_hora = None

from data.estaciones.ent_estacion import EntEstacion
from data.rutas.ent_rutas import EntRuta
from data.trenes.ent_trenes import EntTren
from data.estados.simstate import EstadoSimulacion

# Carga los archivos de configuración (tamaño de ventana y colores de la interfaz).
def cargar_configuracion():
    with open(os.path.join("data", "config", "settings.json"), "r", encoding="utf-8") as f:
        settings = json.load(f)
    with open(os.path.join("data", "config", "colors.json"), "r", encoding="utf-8") as f:
        colors = json.load(f)
    return settings, colors

# Crea un estado de simulación inicial con una estación, una ruta y un tren base y lo guarda en JSON.
def iniciar_simulacion():
    global sim_global, label_hora
    sim = EstadoSimulacion()
    sim_global = sim

    central = EntEstacion("Estación Central", 8242459, [
        {"direccion": "N", "ocupada": False},
        {"direccion": "S", "ocupada": False}
    ], ["Rancagua", "Chillán"])
    sim.estaciones.append(central)
    ruta1 = EntRuta("Estación Central", "Rancagua", 87)
    sim.rutas.append(ruta1)
    tren1 = EntTren("BMU", 160, [236])
    sim.trenes.append(tren1)

    sim.guardar("estado_inicial.json")

    if label_hora is not None:
        label_hora.config(text=f"Hora actual: {sim.hora_actual}")

    messagebox.showinfo("Info", "Simulación inicial creada y guardada.")


# Muestra en una ventana la lista de eventos registrados en la simulación (hora + descripción).
def ver_eventos():
    try:
        with open("estado_inicial.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
        eventos = datos.get("eventos", [])

        if not eventos:
            messagebox.showinfo("Eventos", "No hay eventos registrados.")
            return

        texto = ""
        for ev in eventos:
            texto += f"- {ev.get('hora', '')}: {ev.get('descripcion', '')}\n"

        messagebox.showinfo("Eventos de la Simulación", texto)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron leer los eventos: {e}")


# Lee el archivo de estado y muestra un resumen con cantidad de estaciones, rutas, trenes y capacidad total.
def mostrar_resumen():
    try:
        with open("estado_inicial.json", "r", encoding="utf-8") as f:
            datos = json.load(f)

        estaciones = datos.get("estaciones", [])
        rutas = datos.get("rutas", [])
        trenes = datos.get("trenes", [])

        capacidad_total = 0
        for t in trenes:
            capacidad_total += sum(t.get("vagones", []))

        mensaje = (
            f"Estaciones: {len(estaciones)}\n"
            f"Rutas: {len(rutas)}\n"
            f"Trenes: {len(trenes)}\n"
            f"Capacidad total de trenes: {capacidad_total} personas"
        )
        messagebox.showinfo("Resumen de Simulación", mensaje)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar el resumen: {e}")

# Avanza la hora de la simulación una cantidad de minutos, registra un evento y actualiza el JSON y la etiqueta de hora.
def avanzar_tiempo_gui(minutos):
    global sim_global, label_hora

    if sim_global is None:
        try:
            with open("estado_inicial.json", "r", encoding="utf-8") as f:
                datos = json.load(f)
            sim = EstadoSimulacion()
            sim.hora_actual = datos["hora_actual"]
            sim.estaciones = datos["estaciones"]
            sim.rutas = datos["rutas"]
            sim.trenes = datos["trenes"]
            sim.eventos = datos["eventos"]
            sim_global = sim
        except Exception as e:
            messagebox.showerror("Error", f"No hay simulación cargada: {e}")
            return

    # Avanzar tiempo y registrar evento
    sim_global.avanzar_tiempo(minutos)
    sim_global.registrar_evento(f"Tiempo avanzado {minutos} minutos.")
    sim_global.guardar("estado_inicial.json")

    if label_hora is not None:
        label_hora.config(text=f"Hora actual: {sim_global.hora_actual}")


# Abre una ventana para crear una nueva ruta, valida los datos y la agrega al archivo de estado.
def agregar_ruta():
    ventana = tk.Toplevel()
    ventana.title("Agregar Ruta")
    ventana.geometry("300x200")

    tk.Label(ventana, text="Origen:").pack()
    entrada_origen = tk.Entry(ventana)
    entrada_origen.pack()

    tk.Label(ventana, text="Destino:").pack()
    entrada_destino = tk.Entry(ventana)
    entrada_destino.pack()

    tk.Label(ventana, text="Longitud (km):").pack()
    entrada_long = tk.Entry(ventana)
    entrada_long.pack()

    def guardar_ruta():
        origen = entrada_origen.get().strip()
        destino = entrada_destino.get().strip()
        try:
            longitud = int(entrada_long.get().strip())
        except:
            messagebox.showerror("Error", "La longitud debe ser un número.")
            return
        if not origen or not destino:
            messagebox.showerror("Error", "Llena todos los campos.")
            return

        # -------- VALIDAR QUE ORIGEN Y DESTINO EXISTAN --------
        try:
            with open("estado_inicial.json", "r", encoding="utf-8") as f:
                datos = json.load(f)
            nombres_est = [e["nombre"] for e in datos.get("estaciones", [])]
            if origen not in nombres_est or destino not in nombres_est:
                messagebox.showerror(
                    "Error",
                    "Origen y destino deben ser estaciones existentes."
                )
                return
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo validar estaciones: {e}")
            return
        # -------------------------------------------------------

        nueva_ruta = EntRuta(origen, destino, longitud)
        try:
            datos["rutas"].append(vars(nueva_ruta))
            with open("estado_inicial.json", "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Éxito", "Ruta agregada exitosamente!")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    tk.Button(ventana, text="Guardar", command=guardar_ruta).pack(pady=8)

# Abre una ventana para eliminar una ruta existente a partir de su origen y destino.
def eliminar_ruta():
    ventana = tk.Toplevel()
    ventana.title("Eliminar Ruta")
    ventana.geometry("300x130")

    tk.Label(ventana, text="Origen de la ruta:").pack()
    entrada_origen = tk.Entry(ventana)
    entrada_origen.pack()
    tk.Label(ventana, text="Destino de la ruta:").pack()
    entrada_destino = tk.Entry(ventana)
    entrada_destino.pack()

    def eliminar():
        origen = entrada_origen.get().strip()
        destino = entrada_destino.get().strip()
        if not origen or not destino:
            messagebox.showerror("Error", "Llena ambos campos.")
            return
        try:
            with open("estado_inicial.json", "r", encoding="utf-8") as f:
                datos = json.load(f)
            rutas = datos["rutas"]
            nuevas_rutas = [r for r in rutas if not (r["origen"] == origen and r["destino"] == destino)]
            if len(rutas) == len(nuevas_rutas):
                messagebox.showinfo("Advertencia", "No se encontró la ruta.")
                ventana.destroy()
                return
            datos["rutas"] = nuevas_rutas
            with open("estado_inicial.json", "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Éxito", "Ruta eliminada.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    tk.Button(ventana, text="Eliminar", command=eliminar).pack(pady=8)

# Abre una ventana para modificar la longitud de una ruta ya registrada.
def editar_ruta():
    ventana = tk.Toplevel()
    ventana.title("Editar Ruta")
    ventana.geometry("300x200")

    tk.Label(ventana, text="Origen actual:").pack()
    entrada_origen = tk.Entry(ventana)
    entrada_origen.pack()
    tk.Label(ventana, text="Destino actual:").pack()
    entrada_destino = tk.Entry(ventana)
    entrada_destino.pack()
    tk.Label(ventana, text="Nueva longitud:").pack()
    entrada_long = tk.Entry(ventana)
    entrada_long.pack()

    def editar():
        origen = entrada_origen.get().strip()
        destino = entrada_destino.get().strip()
        try:
            longitud = int(entrada_long.get().strip())
        except:
            messagebox.showerror("Error", "La longitud debe ser un número.")
            return
        if not origen or not destino:
            messagebox.showerror("Error", "Llena todos los campos.")
            return
        try:
            with open("estado_inicial.json", "r", encoding="utf-8") as f:
                datos = json.load(f)
            editado = False
            for r in datos["rutas"]:
                if r["origen"] == origen and r["destino"] == destino:
                    r["longitud"] = longitud
                    editado = True
            if not editado:
                messagebox.showinfo("Advertencia", "No se encontró la ruta.")
                ventana.destroy()
                return
            with open("estado_inicial.json", "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Éxito", "Ruta editada correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar: {e}")

    tk.Button(ventana, text="Editar", command=editar).pack(pady=8)

# Permite buscar y mostrar todas las rutas que pasan por una estación dada (como origen o destino).
def ver_rutas_por_estacion():
    ventana = tk.Toplevel()
    ventana.title("Rutas por Estación")
    ventana.geometry("300x250")

    tk.Label(ventana, text="Nombre de la estación:").pack(pady=5)
    entrada_nombre = tk.Entry(ventana)
    entrada_nombre.pack(pady=5)

    def buscar():
        nombre = entrada_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Debe ingresar un nombre de estación.")
            return
        try:
            with open("estado_inicial.json", "r", encoding="utf-8") as f:
                datos = json.load(f)
            rutas = datos.get("rutas", [])
            relacionadas = [
                r for r in rutas
                if r["origen"] == nombre or r["destino"] == nombre
            ]
            if not relacionadas:
                messagebox.showinfo("Rutas", "La estación no tiene rutas asociadas.")
                return
            texto = ""
            for r in relacionadas:
                texto += f"{r['origen']} -> {r['destino']} ({r['longitud']} km)\n"
            messagebox.showinfo("Rutas asociadas", texto)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron leer las rutas: {e}")

    tk.Button(ventana, text="Buscar", command=buscar).pack(pady=10)

# Abre una ventana para crear un nuevo tren con nombre, velocidad y capacidades de vagones y lo guarda en el estado.
def agregar_tren():
    ventana = tk.Toplevel()
    ventana.title("Agregar Tren")
    ventana.geometry("300x220")

    tk.Label(ventana, text="Nombre:").pack()
    entrada_nombre = tk.Entry(ventana)
    entrada_nombre.pack()
    tk.Label(ventana, text="Velocidad (km/h):").pack()
    entrada_vel = tk.Entry(ventana)
    entrada_vel.pack()
    tk.Label(ventana, text="Capacidad de cada vagón (separadas por coma):").pack()
    entrada_vagones = tk.Entry(ventana)
    entrada_vagones.pack()

    def guardar_tren():
        nombre = entrada_nombre.get().strip()
        try:
            vel = int(entrada_vel.get().strip())
        except:
            messagebox.showerror("Error", "La velocidad debe ser un número.")
            return
        try:
            vag = [int(x) for x in entrada_vagones.get().split(",") if x.strip()]
        except:
            messagebox.showerror("Error", "Las capacidades deben ser números separados por coma.")
            return
        if not nombre or not vag:
            messagebox.showerror("Error", "Llena todos los campos.")
            return
        nuevo_tren = EntTren(nombre, vel, vag)
        try:
            with open("estado_inicial.json", "r", encoding="utf-8") as f:
                datos = json.load(f)
            datos["trenes"].append(vars(nuevo_tren))
            with open("estado_inicial.json", "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Éxito", "Tren agregado exitosamente!")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    tk.Button(ventana, text="Guardar", command=guardar_tren).pack(pady=8)

# Abre una ventana para eliminar un tren existente a partir de su nombre.
def eliminar_tren():
    ventana = tk.Toplevel()
    ventana.title("Eliminar Tren")
    ventana.geometry("300x120")

    tk.Label(ventana, text="Nombre del tren a eliminar:").pack()
    entrada_nombre = tk.Entry(ventana)
    entrada_nombre.pack()

    def eliminar():
        nombre = entrada_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Debe ingresar un nombre.")
            return
        try:
            with open("estado_inicial.json", "r", encoding="utf-8") as f:
                datos = json.load(f)
            trenes = datos["trenes"]
            nuevos_trenes = [t for t in trenes if t["nombre"] != nombre]
            if len(trenes) == len(nuevos_trenes):
                messagebox.showinfo("Advertencia", "No se encontró el tren.")
                ventana.destroy()
                return
            datos["trenes"] = nuevos_trenes
            with open("estado_inicial.json", "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Éxito", "Tren eliminado.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    tk.Button(ventana, text="Eliminar", command=eliminar).pack(pady=8)

# Abre una ventana para cambiar el nombre y la velocidad de un tren registrado.
def editar_tren():
    ventana = tk.Toplevel()
    ventana.title("Editar Tren")
    ventana.geometry("300x200")

    tk.Label(ventana, text="Nombre del tren a editar:").pack()
    entrada_nombre = tk.Entry(ventana)
    entrada_nombre.pack()
    tk.Label(ventana, text="Nuevo nombre:").pack()
    entrada_nuevo = tk.Entry(ventana)
    entrada_nuevo.pack()
    tk.Label(ventana, text="Nueva velocidad:").pack()
    entrada_vel = tk.Entry(ventana)
    entrada_vel.pack()

    def editar():
        nombre = entrada_nombre.get().strip()
        nuevo = entrada_nuevo.get().strip()
        try:
            vel = int(entrada_vel.get().strip())
        except:
            messagebox.showerror("Error", "La velocidad debe ser un número.")
            return
        if not nombre or not nuevo:
            messagebox.showerror("Error", "Llena todos los campos.")
            return
        try:
            with open("estado_inicial.json", "r", encoding="utf-8") as f:
                datos = json.load(f)
            editado = False
            for t in datos["trenes"]:
                if t["nombre"] == nombre:
                    t["nombre"] = nuevo
                    t["velocidad"] = vel
                    editado = True
            if not editado:
                messagebox.showinfo("Advertencia", "No se encontró el tren.")
                ventana.destroy()
                return
            with open("estado_inicial.json", "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Éxito", "Tren editado correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar: {e}")

    tk.Button(ventana, text="Editar", command=editar).pack(pady=8)

# Lee todos los trenes guardados y muestra sus datos principales y capacidad total en una ventana de información.
def ver_trenes():
    try:
        with open("estado_inicial.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
        trenes = datos.get("trenes", [])

        if not trenes:
            messagebox.showinfo("Trenes", "No hay trenes registrados.")
            return

        texto = ""
        for t in trenes:
            nombre = t.get("nombre", "")
            vel = t.get("velocidad", 0)
            vagones = t.get("vagones", [])
            capacidad = sum(vagones)
            texto += (
                f"Nombre: {nombre}\n"
                f"  Velocidad: {vel} km/h\n"
                f"  Vagones: {vagones}\n"
                f"  Capacidad total: {capacidad}\n\n"
            )

        messagebox.showinfo("Detalles de Trenes", texto)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron leer los trenes: {e}")

# Abre una ventana para crear una nueva estación con nombre, población, vías y conexiones, y la guarda en el estado.
def agregar_estacion():
    ventana = tk.Toplevel()
    ventana.title("Agregar Estación")
    ventana.geometry("300x250")

    tk.Label(ventana, text="Nombre:").pack()
    entrada_nombre = tk.Entry(ventana)
    entrada_nombre.pack()

    tk.Label(ventana, text="Población:").pack()
    entrada_pob = tk.Entry(ventana)
    entrada_pob.pack()

    tk.Label(ventana, text="Conexiones (separadas por coma):").pack()
    entrada_conx = tk.Entry(ventana)
    entrada_conx.pack()

    def guardar_est():
        nombre = entrada_nombre.get().strip()
        try:
            pob = int(entrada_pob.get().strip())
        except:
            messagebox.showerror("Error", "La población debe ser un número.")
            return
        conx = [conn.strip() for conn in entrada_conx.get().split(",") if conn.strip()]
        if not nombre or not conx:
            messagebox.showerror("Error", "Llena todos los campos.")
            return
        nuevas_vias = [{"direccion": "N", "ocupada": False}, {"direccion": "S", "ocupada": False}]
        nueva_est = EntEstacion(nombre, pob, nuevas_vias, conx)
        try:
            with open("estado_inicial.json", "r", encoding="utf-8") as f:
                datos = json.load(f)
            datos["estaciones"].append(vars(nueva_est))
            with open("estado_inicial.json", "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Éxito", "Estación agregada exitosamente!")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    tk.Button(ventana, text="Guardar", command=guardar_est).pack(pady=8)

# Abre una ventana para eliminar una estación, impidiendo borrarla si tiene rutas asociadas.
def eliminar_estacion():
    ventana = tk.Toplevel()
    ventana.title("Eliminar Estación")
    ventana.geometry("300x130")

    tk.Label(ventana, text="Nombre de la estación a eliminar:").pack()
    entrada_nombre = tk.Entry(ventana)
    entrada_nombre.pack()

    def eliminar():
        nombre = entrada_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Debe ingresar un nombre.")
            return
        try:
            with open("estado_inicial.json", "r", encoding="utf-8") as f:
                datos = json.load(f)

            # -------- VALIDAR RUTAS ASOCIADAS A ESA ESTACIÓN --------
            rutas = datos.get("rutas", [])
            asociada = any(
                r["origen"] == nombre or r["destino"] == nombre
                for r in rutas
            )
            if asociada:
                messagebox.showerror(
                    "Error",
                    "No se puede eliminar la estación porque tiene rutas asociadas."
                )
                ventana.destroy()
                return
            # ---------------------------------------------------------

            estaciones = datos["estaciones"]
            nuevas_est = [e for e in estaciones if e["nombre"] != nombre]
            if len(estaciones) == len(nuevas_est):
                messagebox.showinfo("Advertencia", "No se encontró la estación.")
                ventana.destroy()
                return
            datos["estaciones"] = nuevas_est
            with open("estado_inicial.json", "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Éxito", "Estación eliminada.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    tk.Button(ventana, text="Eliminar", command=eliminar).pack(pady=8)

# Abre una ventana para cambiar el nombre y la población de una estación existente.
def editar_estacion():
    ventana = tk.Toplevel()
    ventana.title("Editar Estación")
    ventana.geometry("300x200")

    tk.Label(ventana, text="Nombre de la estación a editar:").pack()
    entrada_nombre = tk.Entry(ventana)
    entrada_nombre.pack()

    tk.Label(ventana, text="Nuevo nombre:").pack()
    entrada_nuevo = tk.Entry(ventana)
    entrada_nuevo.pack()

    tk.Label(ventana, text="Nueva población:").pack()
    entrada_pob = tk.Entry(ventana)
    entrada_pob.pack()

    def editar():
        nombre = entrada_nombre.get().strip()
        nuevo = entrada_nuevo.get().strip()
        try:
            pob = int(entrada_pob.get().strip())
        except:
            messagebox.showerror("Error", "La población debe ser un número.")
            return
        if not nombre or not nuevo:
            messagebox.showerror("Error", "Llena todos los campos.")
            return
        try:
            with open("estado_inicial.json", "r", encoding="utf-8") as f:
                datos = json.load(f)
            editado = False
            for e in datos["estaciones"]:
                if e["nombre"] == nombre:
                    e["nombre"] = nuevo
                    e["poblacion"] = pob
                    editado = True
            if not editado:
                messagebox.showinfo("Advertencia", "No se encontró la estación.")
                ventana.destroy()
                return
            with open("estado_inicial.json", "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Éxito", "Estación editada correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar: {e}")

    tk.Button(ventana, text="Editar", command=editar).pack(pady=8)

# Muestra en una ventana un listado resumen con los nombres de estaciones, rutas y trenes guardados.
def mostrar_entidades():
    try:
        with open("estado_inicial.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
        estaciones = datos["estaciones"]
        rutas = datos["rutas"]
        trenes = datos["trenes"]
        mensaje = "Estaciones:\n"
        for e in estaciones:
            mensaje += f"Nombre: {e['nombre']}, Población: {e['poblacion']}, Conexiones: {', '.join(e['conexiones'])}, Vías: {e['vias']}\n"
        mensaje += "\nRutas:\n"
        for r in rutas:
            mensaje += f"Origen: {r['origen']}, Destino: {r['destino']}, Longitud: {r['longitud']}km\n"
        mensaje += "\nTrenes:\n"
        for t in trenes:
            mensaje += f"Nombre: {t['nombre']}, Velocidad: {t['velocidad']}, Vagones: {t['vagones']}, Acción: {t['accion']}\n"
        messagebox.showinfo("Entidades Guardadas", mensaje)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar entidades: {e}")


# Muestra el estado general actual de la simulación: hora, cantidad de estaciones, rutas y trenes.
def cargar_simulacion():
    try:
        with open("estado_inicial.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
        info = f"Hora: {datos['hora_actual']}\n"
        info += f"Estaciones: {len(datos['estaciones'])}\n"
        info += f"Rutas: {len(datos['rutas'])}\n"
        info += f"Trenes: {len(datos['trenes'])}\n"
        messagebox.showinfo("Estado Actual", info)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el estado: {e}")

# Construye la ventana principal del programa con los títulos, secciones de botones y área de consultas.
def crear_interfaz_principal(settings, colors):
    root = tk.Tk()
    root.title("Simulación de Trenes - EFE Chile")
    root.geometry(f"{settings['ancho']}x{settings['alto']}")
    root.configure(bg=colors["fondo"])

    frame_principal = tk.Frame(root, bg=colors["fondo"])
    frame_principal.pack(expand=True, fill="both", padx=20, pady=20)

    # ---- Títulos arriba ----
    titulo = tk.Label(frame_principal, text="Sistema de Simulación de Trenes",
                      font=("Arial", 24, "bold"), bg=colors["fondo"], fg=colors["principal"])
    titulo.pack(pady=(15, 5))
    subtitulo = tk.Label(frame_principal, text="Empresa de Ferrocarriles del Estado (EFE) - Chile",
                         font=("Arial", 14), bg=colors["fondo"], fg=colors["secundario"])
    subtitulo.pack(pady=3)
    info = tk.Label(frame_principal, text="Proyecto de Programación - INFO081\nSistema de Módulos",
                    font=("Arial", 11), bg=colors["fondo"], fg=colors["texto"])
    info.pack(pady=(3, 10))

    # ---- Hora de simulación (debajo del título) ----
    global label_hora
    hora_texto = "Hora actual: (sin iniciar)"
    try:
        with open("estado_inicial.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
        hora_texto = f"Hora actual: {datos['hora_actual']}"
    except:
        pass

    label_hora = tk.Label(
        frame_principal,
        text=hora_texto,
        font=("Arial", 12),
        bg=colors["fondo"],
        fg=colors["texto"]
    )
    label_hora.pack(pady=(0, 15))

    # ---- Secciones Estaciones / Rutas / Trenes ----
    sections = [
        ("Estaciones", [
            ("Agregar Estación", agregar_estacion),
            ("Eliminar Estación", eliminar_estacion),
            ("Editar Estación", editar_estacion)
        ]),
        ("Rutas", [
            ("Agregar Ruta", agregar_ruta),
            ("Eliminar Ruta", eliminar_ruta),
            ("Editar Ruta", editar_ruta)
        ]),
        ("Trenes", [
            ("Agregar Tren", agregar_tren),
            ("Eliminar Tren", eliminar_tren),
            ("Editar Tren", editar_tren)
        ])
    ]

    for nombre, botones in sections:
        frame = tk.LabelFrame(
            frame_principal,
            text=nombre,
            bg=colors["fondo"],
            fg=colors["principal"],
            font=("Arial", 13, "bold"),
            padx=15,
            pady=15,
            relief=tk.GROOVE,
            bd=3
        )
        frame.pack(pady=8)
        for label, cmd in botones:
            tk.Button(
                frame, text=label, font=("Arial", 12),
                width=22, bg=colors["secundario"], fg="#FFFFFF", command=cmd
            ).pack(pady=4)

    # ---- Sección de Consultas / Reportes (compacta) ----
    frame_consultas = tk.LabelFrame(
        frame_principal,
        text="Consultas y Reportes",
        bg=colors["fondo"],
        fg=colors["principal"],
        font=("Arial", 11, "bold"),
        padx=8,
        pady=8,
        relief=tk.GROOVE,
        bd=2
    )
    frame_consultas.pack(pady=8)

    boton_width = 24

    tk.Button(
        frame_consultas, text="Mostrar Entidades Guardadas",
        font=("Arial", 11), width=boton_width,
        bg=colors["principal"], fg="#FFFFFF",
        command=mostrar_entidades
    ).pack(pady=2)

    tk.Button(
        frame_consultas, text="Cargar Estado de Simulación",
        font=("Arial", 11), width=boton_width,
        bg=colors["principal"], fg="#FFFFFF",
        command=cargar_simulacion
    ).pack(pady=2)

    tk.Button(
        frame_consultas, text="Ver Detalles de Trenes",
        font=("Arial", 11), width=boton_width,
        bg=colors["principal"], fg="#FFFFFF",
        command=ver_trenes
    ).pack(pady=2)

    tk.Button(
        frame_consultas, text="Ver Rutas por Estación",
        font=("Arial", 11), width=boton_width,
        bg=colors["principal"], fg="#FFFFFF",
        command=ver_rutas_por_estacion
    ).pack(pady=2)

    tk.Button(
        frame_consultas, text="Ver Eventos",
        font=("Arial", 11), width=boton_width,
        bg=colors["principal"], fg="#FFFFFF",
        command=ver_eventos
    ).pack(pady=2)

    tk.Button(
        frame_consultas, text="Ver Resumen",
        font=("Arial", 11), width=boton_width,
        bg=colors["principal"], fg="#FFFFFF",
        command=mostrar_resumen
    ).pack(pady=2)

    tk.Button(
        frame_consultas, text="Avanzar 10 minutos",
        font=("Arial", 11), width=boton_width,
        bg=colors["principal"], fg="#FFFFFF",
        command=lambda: avanzar_tiempo_gui(10)
    ).pack(pady=2)

    # ---- Footer ----
    footer = tk.Label(
        frame_principal,
        text="© 2025 - Proyecto Colaborativo en GitHub",
        font=("Arial", 10),
        bg=colors["fondo"],
        fg=colors["secundario"]
    )
    footer.pack(side="bottom", pady=(10, 0))

    return root

# Punto de entrada del programa: carga la configuración, crea la interfaz principal y arranca el bucle de la GUI.

def main():
    settings, colors = cargar_configuracion()
    root = crear_interfaz_principal(settings, colors)
    root.mainloop()

if __name__ == "__main__":
    main()