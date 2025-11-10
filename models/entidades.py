class Estacion:
    def _init_(self,Nombre,Poblacion,Flujo):
        
        self.Nombre = Nombre
        self,Poblacion = Poblacion
        self.Vias = dict()
        self.Flujo = Flujo

    def CambioPoblacion():
        pass

    def AnadirVia():
        pass
    
    def QuitarVia():
        pass
        
class Ruta:
    def _init_(self,Origen,Destino,Distancia):

        self.Origen = Origen
        self.Destino = Destino
        self.Distancia = Distancia

    def CambioRuta():
        pass

class Tren:
    def _init_(self,Nombre,Velocidad,Flujo):
        self.Nombre = Nombre
        self.Velocidad = Velocidad
        self.Flujo = Flujo
        self.Estado = "PAUSA"
        self.Bagones = dict()

    def AnadirBagon():
        pass
    
    def QuitarBagon():
        pass
    
    def CambiarEstado():
        pass
    
    def CambioFlujo():
        pass