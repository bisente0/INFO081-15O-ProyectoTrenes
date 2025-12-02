from ..logic.state.save_syst import file_syst
from ..logic.state.sim_state import estado
from ..utils.funciones_relacionadas import datos_corruptos

class model:
    '''
        La clase model permite reunir la lógica, conectar con el
        controlador y el almacenamiento, interactuando con el sim en
        un alto nivel.
    '''

    def __init__(self):
        self.file_syst = file_syst()
        self.estado_sim = estado()

    def cargar_estado(self) -> None:
        if self.estado_sim.verificar_integridad():
            self.file_syst.cargar_sim()
        else:
            raise datos_corruptos(self.file_syst.estado)
    
    def tick(self, dt: int) -> None:
        self.estado_sim.update(dt)
        
    def guardar_estado(self) -> None:
        self.file_syst.guardar_sim()

    def reset(self) -> None:
        self.estado_sim.reset()

    def reportar_estado(self, error) -> None:
        self.estado_sim.reporte_estado(error)
    