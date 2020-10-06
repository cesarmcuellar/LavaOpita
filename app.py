from flask import Flask, request, render_template,jsonify,redirect,url_for,session
from modelo import DatosUsuario, DatosEmpleado, DatosServicioLavado, DatosVehiculo, DatosCliente
from datetime import datetime
from flask_mysqldb import MySQL
import yagmail
import os


# Crear un objeto de tipo Flask
app = Flask(__name__)

# Datos para la conexión a mysql
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lavaopita'

'''
Crear un objeto de tipo MySQL y se pasa como parametro el objeto
de tipo Flask con la configuración
'''
mysql = MySQL(app)

#secret key para poder registrar variables de sesión
app.secret_key = 'miKeySecret'

#Raiz del sitio
@app.route('/')
def inicio():    
    return render_template('principal.html')

@app.route("/Mision")
def mision():
    return render_template('mision.html')

@app.route("/Vision")
def vision():
    return render_template('vision.html')

@app.route("/Servicios")
def servicios():
    return render_template('servicios.html')

@app.route("/iniciar")
def iniciar():
    return render_template('frmIniciarSesion.html')

@app.route("/Administrador")
def inicioAdministrador():    
    if "rol" in session:
        if session["rol"]=="Administrador":
            return render_template('Administrador/principal.html')
        else:
            respuesta=(False,None,"No tiene permso para acceder")
            return render_template('frmIniciarSesion.html',respuesta=respuesta)
    else:
        respuesta=(False,None,"Debe  primero iniciar Sesión")
        return render_template('frmIniciarSesion.html',respuesta=respuesta)
   
@app.route("/Asistente")
def inicioAsistente():    
    if "rol" in session:
        if session["rol"]=="Asistente":
            return render_template('Asistente/principal.html')
        else:
            respuesta=(False,None,"No tiene permiso para acceder")
            return render_template('frmIniciarSesion.html',respuesta=respuesta)
    else:
        respuesta=(False,None,"Debe  primero iniciar Sesión")
        return render_template('frmIniciarSesion.html',respuesta=respuesta)

@app.route("/Cliente")
def inicioCliente():    
    if "rol" in session:
        if session["rol"]=="Cliente":
            return render_template('Cliente/principal.html')
        else:
            respuesta=(False,None,"Debe  primero iniciar Sesión")
            return render_template('frmIniciarSesion.html',respuesta=respuesta)
    else:
        respuesta=(False,None,"Debe  primero iniciar Sesión")
        return render_template('frmIniciarSesion.html',respuesta=respuesta)

@app.route("/reportesGraficos")
def reportesGraficos():
    return render_template('Administrador/graficas.html')

@app.route("/serviciosEnLavado")
def serviciosEnLavado():
    """[summary]
       Muestra la interfaz para listar los Sericios en estado En Lavado
    Returns:
        [html]: [Interfaz html]
    """
    return render_template('Asistente/listarServiciosEnLavado.html')

@app.route("/salir")
def salir():
    """[summary]
        Cierra la sesión de la Aplicación y elimina las variables de
        sesión creadas
    Returns:
        [html]: [Nos envía a la página principal de la aplicación]
    """
    session.clear()
    respuesta=(False,None,"Ha cerrado la Sesión")
    return render_template('frmIniciarSesion.html',respuesta=respuesta)  

@app.route("/iniciarSesion", methods=['POST', 'GET'])
def iniciarSesion():
    """[summary]
        Valida el ingreso a la aplicación de acuerdo a las
        credenciales de ingreso
    Returns:
        [type]: [Dependiendo del usuario lo redirecciona a la vista y si las
                credenciales no son validas retorna a la vista de inicio de sesión]
    """
    if request.method == 'POST':
        login = request.form['txtLogin']
        password = request.form['txtPassword']        
        if(login and password):
            #crear un objeto de tipo DatosUsuario y se le pasa el objeto mysql
            dUsuario = DatosUsuario(mysql)
            user = dUsuario.iniciarSesion(login,password)
            if(user):
                if(user[5]=="Activo"):
                    if(user[4]=="Administrador" or user[4]=="Asistente"):
                        dEmpleado = DatosEmpleado(mysql)                       
                        perEmpleado = dEmpleado.consultarPorIdPersona(user[1])                       
                        if(user[4]=="Administrador"):            
                            #Crea una variable de sesión
                            session["user"]=user
                            session["idEmpleado"]=perEmpleado[6]
                            session["rol"]="Administrador"
                            return redirect(url_for('inicioAdministrador'))
                        elif(user[4]=="Asistente"):
                            #Crea una variable de sesión
                            session["user"]=user
                            session["idEmpleado"]=perEmpleado[6]
                            session["rol"]="Asistente"
                            return redirect(url_for('inicioAsistente'))                                                   
                    elif(user[4]=="Cliente"):
                        #Crea una variable de sesión
                        session["user"]=user
                        session["rol"]="Cliente"
                        return redirect(url_for('inicioCliente'))                        
                else:                   
                    respuesta=(False,None,"Usuario Inactivo")
                    return render_template("frmIniciarSesion.html",respuesta=respuesta)                   
            else:                
                respuesta=(False,None,"Credenciales de ingreso no validas")
                return render_template("frmIniciarSesion.html",respuesta=respuesta)              

#tareas del Asistente
@app.route("/servicioLavado")
def servicioLavado():
    """[summary]
        obtiene un lista de los tipos de servicio y de los empleados
        para que al cargar la vista se muestren en el formulario
    Returns:
        [tuplas]: [Lista de Tipos de Servicio y Lista de Empleados]
    """
    dServicio = DatosServicioLavado(mysql)
    tiposServicio = dServicio.listarTiposServicio()
    dEmpleado = DatosEmpleado(mysql)
    empleados = dEmpleado.listarEmpleadosTecnicosLavado()
    return render_template('/Asistente/frmServicioLavado.html', 
                        tipos=tiposServicio, empleados=empleados)

@app.route("/vehiculoPorPlaca", methods=['POST', 'GET'] )
def consultarVehiculoPorPlaca():
    """[summary]
        Consulta la existencia de un vehiculo por su placa
    Returns:
        [json]: [Si el vehculo existe retorna datos del Vehiculo]
    """
    if request.method == 'POST':
        placa = request.form["placa"]
        if(placa):
            dVehiculo = DatosVehiculo(mysql)
            resultado = dVehiculo.consultarPorPlaca(placa)
            if(resultado):
                return jsonify({"estado":True, "datos":resultado, "mensaje":"Datos del Vehiculo"}) 
            else:
                return jsonify({"estado":False, "datos":resultado, "mensaje":"Vehiculo no Registrado"}) 

@app.route("/clientePorCedula",methods=['POST', 'GET'])
def clientePorCedula():
    """[summary]
        Consulta clientes por su identificación
    Returns:
        [json]: [Si exsite el cliete retorna los datos del cliente]
    """
    if request.method == 'POST':
        identificacion = request.form["identificacion"]
        dCliente = DatosCliente(mysql)
        resultado = dCliente.consultarPorIdentificacion(identificacion)
        if(resultado):
            return jsonify({"estado":True, "datos":resultado, "mensaje":"Datos del Cliente"}) 
        else:
            return jsonify({"estado":False, "datos":resultado, "mensaje":"Cliente no registrado con esa identificación"}) 
            
@app.route("/registrarServicio",methods=['POST', 'GET'])
def registrarServicioLavado():
    """[summary]
        Registra el servicio de lavado de un vehiculo, recibe
        de la vista el id del cliente, el id del empleado,
        el id dele vehiculo y el tipo de servicio
    Returns:
        [json]: [Confirmación si se pudo o no registar el servicio]
    """
    if request.method == 'POST':        
        idCliente = request.form["txtIdCliente"]
        idEmpleado = request.form["cbEmpleado"]
        idVehiculo = request.form["txtIdVehiculo"]
        tipoServicio = request.form["cbTipoServicio"]
        placa = request.form["txtPlaca"]
        nombreCliente = request.form["nombreCliente"]
        correo = request.form["correo"]
        fechaServicio = datetime.now()        
        estado="En Lavado"
        servicio = (idVehiculo,idCliente,tipoServicio,idEmpleado,fechaServicio,None,None,estado)
        dServicio = DatosServicioLavado(mysql)
        resultado = dServicio.agregar(servicio)
        if(resultado):
            #consultar datos de cliente para enviar correo
            mensaje= f"""Cordial saludo <b>{nombreCliente}</b> nos permitimos informarle 
                        que se ha Registrado un servicio de lavado a su vehiculo
                        con placa <b>{placa}</b>.<br>
                        <br><br>Atentamente,<br><br>César Marino Cuéllar<br>Administrador                        
                    """
            asunto="Registro Lavado"
            print(mensaje)
            try:
                email = yagmail.SMTP("ccuellar@misena.edu.co",open("password").read())
                email.send(to=correo, subject=asunto,contents=mensaje)
            except:
                print("Correo no enviado")  
            return jsonify({"estado":True, "datos":resultado, 
            "mensaje":"Servicio Registrado"}) 
        else:
            return jsonify({"estado":False, "datos":resultado, 
            "mensaje":"Porblemas al Registrar el Servicio"}) 

@app.route("/listarServiciosEnLavado" ,methods=['POST', 'GET'])
def listarServiciosLavado():
    """[summary]
        Consulta los servicicos que están en estado En Lavado y los retorna a
        la vista
    Returns:
        [json]: [Lista de servicios en estado En Lavado]
    """
    if request.method == 'POST':
        dServicioLavado = DatosServicioLavado(mysql)
        year = datetime.now().year
        print(year)
        servicios = dServicioLavado.listarServiciosEnLavado(year)        
        if(servicios):        
            return jsonify({"estado":True, "datos":servicios, "mensaje":"Listado de Servicios"}) 
        else:
            return jsonify({"estado":False, "datos":None, "mensaje":"Problemas al Listar los Servicios"}) 

@app.route("/actualizarServicioLavado",methods=['POST', 'GET'])
def actualizarServicioLavado():
    """[summary]
        Registra la terminación del lavado del carro o moto y 
        actualiza en la base de datos la fecha y hora de salida, el
        estado y observaciones si es necesario
    Returns:
        [json]: [Confirmación de la actualización]
    """
    if request.method == 'POST':
        dServicioLavado = DatosServicioLavado(mysql)
        idServicioLavado = int(request.form["idServicioLavado"])
        fechaActual = datetime.now()
        observaciones = request.form["observaciones"]
        resultado = dServicioLavado.actualizarServicio(fechaActual,observaciones,"Terminado",idServicioLavado)
        if(resultado):
            return jsonify({"estado":True, "datos":None, "mensaje":"Se ha registrado la terminación del Servicio"}) 
        else:
            return jsonify({"estado":False, "datos":None, "mensaje":"Problemas al actualizar el servicio de lavado"}) 

#funciones con decoradores del Administrador 
@app.route("/ingresosPorMes",methods=['POST', 'GET'])
def ingresosPorMes():
    """[summary]
        Consulta los ingresos obtenidos en el lavadero por los servicios de 
        lavado prestados por cada uno de los meses.
    Returns:
        [json]: [Datos con los ingresos por cada mes]
    """
    if request.method == 'POST':
        dServicioLavado = DatosServicioLavado(mysql)
        meses = ("Enero","Febrero","Marzo","Abril","Mayo","Junio",
        "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre")
        resultado = dServicioLavado.ingresosPorMes()
        #convierto el resultado que es una tupla a una lista
        resultado = list(resultado)
        # se crea una lista como requiere la api que lleguen los datos la lista su primer 
        # elemento es una lista con los encabezados de los datos y los demas valores son 
        # listas con el nombre del mes y el valor de los ingresos del mes ejemplo ["Octubre",50000.0]
        datos = [["Mes","Valor"]]
        for d in range(len(resultado)):
            resultado[d]=list(resultado[d])
            resultado[d][0]=meses[resultado[d][0]-1]
            datos.append(resultado[d])        
        if(datos):
            return jsonify({"estado":True, "datos":datos, "mensaje":"Ingresos por Mes"}) 
        else:
            return jsonify({"estado":False, "datos":None, "mensaje":"Problemas al obtener los datos"}) 



# Iniciar la aplicación
if __name__ == "__main__":
    app.run(port=3000, debug=True)   