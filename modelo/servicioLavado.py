class ServicioLavado():

    def __init__(self,vehiculo=None, cliente=None, empleado=None,tipoServicio=None,fechaHoraInicio=None, fechaHoraFin=None,observaciones=None):
        self.vehiculo=vehiculo
        self.cliente=cliente
        self.empleado=empleado
        self.tipoServicio=tipoServicio
        self.fechaHoraInicio=fechaHoraInicio
        self.fechaHoraFin=fechaHoraFin
        self.observaciones=observaciones
        self.estado="En Lavado"

    def setIdServicioLavado(self, idServicioLavado):
        self.idServicioLavado=idServicioLavado