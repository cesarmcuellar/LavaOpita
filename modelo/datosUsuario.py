from flask_mysqldb import MySQL
class DatosUsuario():

    def __init__(self, mysql):       
        self.mysql=mysql
        self.cursor=self.mysql.connection.cursor()

    def iniciarSesion(self, login, password):                     
        consulta="select * from usuarios where usuLogin= %s and usuPassword = %s"
        self.cursor.execute(consulta,(login,password))
        resultado = self.cursor.fetchone()
        self.cursor.close()
        return resultado