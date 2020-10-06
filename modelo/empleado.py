from .persona import Persona

class Empleado(Persona):

    def __init__(self, cargo=None,identificacion=None, nombres=None, apellidos=None, correo=None, telefono=None):
        super().__init__(identificacion,nombres,apellidos,correo,telefono)
        self.cargo=cargo

    def setIdEmpleado(self,idEmpleado):
        self.idEmpleado=idEmpleado
        

    
