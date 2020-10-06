

class Conexion():
    
    def __init__(self,app): 
        self.app=app
        self.app.config['MYSQL_HOST'] = 'localhost' 
        self.app.config['MYSQL_USER'] = 'root'
        self.app.config['MYSQL_PASSWORD'] = ''
        self.app.config['MYSQL_DB'] = 'lavaopita'           
        
    def getConexion(self):
        return self.app
