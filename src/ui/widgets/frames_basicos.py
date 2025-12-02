import tkinter as tk
from tkinter import ttk

#Se define y posiciona un frame master como raiz para cada frame de estaciones
def frame_master_estaciones(parent):
    frame = ttk.LabelFrame(parent, text="ESTACIONES:")
    frame.grid(row=4,column=3)
    
    return frame

#Se define un label frame con los datos necesarios para mostrar "n" estaciones
def frame_estacion(parent,estacion, flujo_acum, estado, via_rotacion,n):
    
    frame_estacion = ttk.LabelFrame(parent,text=estacion)
    frame_estacion.pack(side=tk.TOP)
    #Datos de la estacion
    label_texto_FA=tk.Label(frame_estacion, text="FLUJO ACUMULADO:",font=("Arial",10)).grid(row=n,column=0)
    label_FA= tk.Label(frame_estacion, text=flujo_acum, font=("Arial", 10)).grid(row=n,column=1)

    label_texto_E= tk.Label(frame_estacion, text="ESTADO:",font=("Arial",10)).grid(row=n+1,column=0)
    label_E= tk.Label(frame_estacion,text=estado, font=("Arial", 10)).grid(row=n+1,column=1)
   
    label_texto_VR=tk.Label(frame_estacion, text="VÍA DE ROTACIÓN:", font=("Arial",10)).grid(row=n+2,column=0)
    label_VR=tk.Label(frame_estacion,text=via_rotacion, font=("Arial", 10)).grid(row=n+2,column=1)
    
    return frame_estacion
#Se define y posiciona un frame master como raiz para cada frame de trenes 
def frame_master_trenes(parent):
    frame = ttk.LabelFrame(parent, text="TRENES:")
    frame.grid(row=4,column=6)
    return frame
#Se define un label frame con los datos necesarios para mostrar "n" trenes
def frame_tren(parent,tren,flujo_acum,estado,tiempo,n):
    
    frame_tren = ttk.LabelFrame(parent,text=tren)
    frame_tren.pack(side=tk.TOP)
    #Datos de el tren
    label_texto_FA=tk.Label(frame_tren, text="FLUJO ACUMULADO:",font=("Arial",10)).grid(row=n,column=0)
    label_FA= tk.Label(frame_tren, text=flujo_acum, font=("Arial", 10)).grid(row=n,column=1)

    label_texto_E= tk.Label(frame_tren, text="ESTADO:",font=("Arial",10)).grid(row=n+1,column=0)
    label_E= tk.Label(frame_tren,text=estado, font=("Arial", 10)).grid(row=n+1,column=1)

    label_texto_TR= tk.Label(frame_tren, text="TIEMPO RESTANTE:", font=("Arial", 10)).grid(row=n+2,column=0)
    label_TR = tk.Label(frame_tren, text = tiempo, font=("Arial", 10)).grid(row=n+2,column=1)

    return frame_tren

#Se define y posiciona un frame como raiz para cada frame de "n" rutas
def frame_master_rutas(parent):
    
    frame = ttk.LabelFrame(parent, text="RUTAS:")
    frame.grid(row=4,column=9)
    
    return frame
       
def frame_ruta(parent,estacion1,estacion2,direccion,estado,n):
    
    frame_ruta = ttk.LabelFrame(parent)
    
    label_estacion1 = tk.Label(frame_ruta,text=estacion1,font=("Arial",10)).grid(row=n,column=0)
    label_direccion = tk.Label(frame_ruta,text=direccion, font=("Arial",10)).grid(row=n,column=1)
    label_estacion2 = tk.Label(frame_ruta,text=estacion2,font=("Arial",10)).grid(row=n,column=2)  
    
    label_texto_E = tk.Label(frame_ruta,text="ESTADO:", font=("Arial",10)).grid(row=n+1,column=0)
    label_E = tk.Label(frame_ruta,text=estado,font=("Arial",10)).grid(row=n+1,column=1)

    frame_ruta.pack(side=tk.TOP)
    return frame_ruta




if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pruebas")
    root.geometry("1200x800")
    primer_frame=frame_master_estaciones(root)
    estacion1=frame_estacion(primer_frame,"SANTIAGO",5,"TREN UNO","LIBRE",0)
    estacion2=frame_estacion(primer_frame,"PERU",12,"LIBRE","TREN TRES",1)
    segundo_frame=frame_master_trenes(root)
    tren1=frame_tren(segundo_frame,"BMU",210,"EN ESTACION","02:12",0)
    tren2=frame_tren(segundo_frame,"EMU",120,"EN RUTA","11:20",1)
    tercer_frame=frame_master_rutas(root)
    ruta1=frame_ruta(tercer_frame,"coquimbo", "antofagasta","--->","LIBRE",0)
    ruta2=frame_ruta(tercer_frame,"antofagasta", "coquimbo","<---","TREN UNO",1)
    root.mainloop() 
    