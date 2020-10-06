from flask_mysqldb import MySQL
class DatosEmpleado():

    def __init__(self, mysql):
        self.mysql=mysql
        self.cursor=self.mysql.connection.cursor()

    def consultarPorIdPersona(self, idPersona):        
        consulta= "select * from personas inner join empleados on empleados.empPersona=personas.idPersona where personas.idPersona=%s"
        self.cursor.execute(consulta,(idPersona,))
        resultado = self.cursor.fetchone()
        self.cursor.close()
        return resultado

    def listarEmpleadosTecnicosLavado(self):
        consulta= "select * from personas inner join empleados on empleados.empPersona=personas.idPersona where empleados.empCargo=%s"
        self.cursor.execute(consulta,("Técnico de Lavado",))
        resultado = self.cursor.fetchall()
        self.cursor.close()
        return resultado
