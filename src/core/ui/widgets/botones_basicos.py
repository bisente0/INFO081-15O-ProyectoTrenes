import tkinter as tk
from ..eventos_basicos import *
 #Se crea cada boton para la interfaz
def crear_botones(parent):

   boton_CE = tk.Button(parent, text="[COLA DE EVENTOS]", command=cola_eventos)
   boton_CE.pack(padx=5, pady=5)

   boton_IE = tk.Button(parent,text="[INFO. ESTACIONES]", command=informacion_estaciones)
   boton_IE.pack(padx=5, pady=5)

   boton_IT = tk.Button(parent,text="[INFO. TRENES]", command=informacion_trenes)
   boton_IT.pack(padx=5, pady=5)

   boton_IR = tk.Button(parent,text="[INFO. RUTAS]", command=informacion_rutas)
   boton_IR.pack(padx=5, pady=5)

   boton_RT = tk.Button(parent,text="[REGRESAR TURNO]", command=regresar_turno)
   boton_RT.pack(padx=5, pady=5)

   boton_AT = tk.Button(parent,text="[AVANZAR TURNO]", command=avanzar_turno)
   boton_AT.pack(padx=5, pady=5)

   boton_AR = tk.Button(parent,text="[ACCION RECOMENDADA]", command=accion_recomendada)
   boton_AR.pack(padx=5, pady=5)

   boton_GC = tk.Button(parent,text="[GUARDAR Y CONTINUAR]", command=guardar_continuar)
   boton_GC.pack(padx=5, pady=5)

   boton_GA = tk.Button(parent,text="[GUARDAR Y SALIR]", command=avanzar_turno)
   boton_GA.pack(padx=5, pady=5)

   boton_SA = tk.Button(parent,text="[SALIR]", command=salir)
   boton_SA.pack(padx=5, pady=5)

   boton_IN = tk.Button(parent,text="[INGRESAR]", command=ingresar)
   boton_IN.pack(padx=5, pady=5)

   boton_MO = tk.Button(parent,text="[MODIFICAR]", command=modificar)
   boton_MO.pack(padx=5, pady=5)


