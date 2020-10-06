class Persona():

    def __init__(self, identificacion=None, nombres=None, apellidos=None, correo=None, telefono=None):
        self.identificacion=identificacion
        self.nombres=nombres
        self.apellidos=apellidos
        self.correo=correo
        self.telefono=telefono

    def setIdPersona(self,idPersona):
        self.idPersona=idPersona

    