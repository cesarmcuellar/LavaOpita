from .persona import Persona

class Cliente(Persona):

    def __init__(self,identificacion=None, nombres=None, apellidos=None, correo=None, telefono=None):
        super().__init__(identificacion,nombres,apellidos,correo,telefono)

    def setIdCliente(self,idCliente):
        self.idCliente=idCliente