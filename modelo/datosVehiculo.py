from flask_mysqldb import MySQL
class DatosVehiculo():

    def __init__(self, mysql):
        self.mysql=mysql
        self.cursor=self.mysql.connection.cursor()

    def consultarPorPlaca(self, placa):        
        consulta="select * from vehiculos where vehPlaca= %s"
        self.cursor.execute(consulta,(placa,))
        resultado = self.cursor.fetchone()
        self.cursor.close()
        return resultado