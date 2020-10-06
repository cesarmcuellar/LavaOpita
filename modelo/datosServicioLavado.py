from flask_mysqldb import MySQL

class DatosServicioLavado():

    def __init__(self,mysql):  
        self.mysql=mysql
        self.cursor=self.mysql.connection.cursor()        
    
    def listarTiposServicio(self):
        consulta="select * from tiposservicio"
        self.cursor.execute(consulta)
        resultado = self.cursor.fetchall()
        self.cursor.close()
        return resultado

    def agregar(self,servicio):
        """[summary]
        Registra el servicio de lavado de un vehiculo, recibe los
        datos en una tupla
        Returns:
        [True o False]: [Retorna el estado de la consulta]
        """             
        consulta="insert into servicioslavado values(null, %s, %s, %s, %s, %s, %s, %s, %s)"
        resultado = self.cursor.execute(consulta,servicio)
        self.mysql.connection.commit()
        self.cursor.close()
        return resultado
        
    def listarServiciosEnLavado(self,year):
        consulta="""
                    select idServicioLavado, vehPlaca, tipNombre, serFechaHoraInicio 
                    from servicioslavado inner join vehiculos
                    on servicioslavado.serVehiculo = vehiculos.idVehiculo
                    inner join tiposServicio on
                    servicioslavado.serTipoServicio=tiposservicio.idTipoServicio
                    where serEstado='En Lavado' and (Year(serFechaHoraInicio))=%s
                """
        self.cursor.execute(consulta,(year,))
        resultado = self.cursor.fetchall()       
        self.cursor.close()
        return resultado

    def actualizarServicio(self,fechaFin,observaciones,estado, idServicioLavado):
        datosActualizar=(fechaFin, observaciones, estado,idServicioLavado)
        consulta="""
                    update servicioslavado set serFechaHoraFin=%s, serObservaciones=%s,
                    serEstado=%s where idServicioLavado=%s
                """
        resultado = self.cursor.execute(consulta,datosActualizar)
        self.mysql.connection.commit()
        self.cursor.close()
        return resultado

    def ingresosPorMes(self):
        consulta="""
                    select month(serFechaHoraFin),sum(tipCosto)  from servicioslavado
                    inner join tiposservicio on
                    servicioslavado.serTipoServicio=tiposservicio.idTipoServicio
                    where serEstado='Terminado'
                    group by month(serFechaHoraFin) order by month(serFechaHoraFin) asc
                """
        self.cursor.execute(consulta)
        resultado = self.cursor.fetchall()       
        self.cursor.close()
        return resultado


