class EntTren:
    def __init__(self, nombre, velocidad, vagones):
        self.nombre = nombre
        self.velocidad = velocidad  # en km/h
        self.vagones = vagones  # lista de capacidades
        self.flujo_personas = 0
        self.accion = "esperando"
