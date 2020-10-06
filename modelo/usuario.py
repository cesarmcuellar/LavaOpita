class Usuario():

    def __init__(self, persona=None, login=None, password=None,rol=None):
        self.persona=persona
        self.login=login
        self.password=password
        self.rol=rol
        self.estado="Activo"

    def setIdUsuario(self, idUsuario):
        self.idUsuario=idUsuario