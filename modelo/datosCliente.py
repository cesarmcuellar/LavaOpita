from flask_mysqldb import MySQL
class DatosCliente():

    def __init__(self, mysql):
        self.mysql=mysql
        self.cursor=self.mysql.connection.cursor()

    def consultarPorIdentificacion(self, identificacion):        
        consulta= """
                    select * from personas inner join clientes 
                    on clientes.cliPersona=personas.idPersona 
                    where personas.perIdentificacion=%s
                    """
        self.cursor.execute(consulta,(identificacion,))
        resultado = self.cursor.fetchone()
        self.cursor.close()
        return resultado

    def consultarPorId(self, idCliente):        
        consulta= """
                    select * from personas inner join clientes 
                    on clientes.cliPersona=personas.idPersona 
                    where clientes.idCliente=%s
                    """
        self.cursor.execute(consulta,(idCliente,))
        resultado = self.cursor.fetchone()
        self.cursor.close()
        return resultado