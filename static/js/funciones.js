var primeraFila;
var idServicioLavado;
var vehiculo;
var cliente;
$(function(){  
    primeraFila = $("#fila");        
      
    $("#btnIniciarSesion").click(function(){               
        iniciarSesion();
    });  

    //Botón si del Modal de Eliminar Aprendiz
    $("#btnSiModal").click(function(){
        eliminarContacto();
    });  

    $("#txtPlaca").change(function(){
        consultarVehiculoPorPlaca();
    });

    $("#txtIdentificacionCliente").change(function(){
        consultarClientePorIdentificacion();
    });

    $("#btnRegistrarServicio").click(function(){               
        registrarServicioLavado();
    }); 

    $("#btnActualizarModal").click(function(){
        actualizarServicioLavado();
    });

    
 });


function iniciarSesion(){   
    $("#mensaje").html(""); 
    $.ajax({
        url: '/iniciarSesion',    
        data: $("#frmIniciarSesion").serialize(),
        dataType:'json',
        type: 'post',       
        cache: false,       
        success: function (resultado) {
            console.log(resultado); 
            if(resultado.estado===false){
                $("#mensaje").html(resultado.mensaje);           
            } 
        },
        error: function(ex){
          console.log(ex.responseText);
        }
    });
}

function consultarVehiculoPorPlaca(){
    $("#msjPlaca").html("");
    var parametros = {
        placa:$("#txtPlaca").val()
    }
    $.ajax({
        url: '/vehiculoPorPlaca',    
        data: parametros,
        dataType:'json',
        type: 'post',       
        cache: false,       
        success: function (resultado) {
            console.log(resultado); 
            vehiculo=resultado.datos;
            if(resultado.estado===false){
                $("#msjPlaca").html(resultado.mensaje);           
            }else{
                $("#msjPlaca").html("Datos del Vehiculo" + resultado.datos)
                $("#txtIdVehiculo").val(resultado.datos[0]);
            }
        },
        error: function(ex){
          console.log(ex.responseText);
        }
    });
}

function consultarClientePorIdentificacion(){
    var parametros = {
        identificacion:$("#txtIdentificacionCliente").val()
    }
    $.ajax({
        url: '/clientePorCedula',    
        data: parametros,
        dataType:'json',
        type: 'post',       
        cache: false,       
        success: function (resultado) {
            console.log(resultado); 
            cliente = resultado.datos;
            if(resultado.estado===false){
                $("#msjCliente").html(resultado.mensaje);           
            }else{
                $("#msjCliente").html("Datos del Cliente" + resultado.datos)
                // campos ocultos del formulario
                $("#txtIdCliente").val(resultado.datos[6]);
                $("#nombreCliente").val(resultado.datos[2] + " " + resultado.datos[3]);
                $("#correo").val(resultado.datos[4]);
            }
        },
        error: function(ex){
          console.log(ex.responseText);
        }
    });
}

function registrarServicioLavado(){    
    $.ajax({
        url: '/registrarServicio',    
        data: $("#frmServicio").serialize(),        
        dataType:'json',
        type: 'post',       
        cache: false,       
        success: function (resultado) {
            console.log(resultado); 
            if(resultado.estado){
               limpiar();
            }           
            $("#mensaje").html(resultado.mensaje);          
        },
        error: function(ex){
          console.log(ex.responseText);
        }
    });
}

function listarserviciosEnLavado(){
    $(".otraFila").remove();
    //agregar la primera fila vacía
    $("#tblServicios tbody").append(primeraFila);
    $.ajax({
        url: '/listarServiciosEnLavado',   
        dataType:'json',
        type: 'post',       
        cache: false,       
        success: function (resultado) {
            console.log(resultado); 
            servicios = resultado.datos;
            $.each(servicios, function (i, servicio) {                
                $("#sPlaca").html(servicio[1]);
                $("#sTiposervicio").html(servicio[2]);
                $("#sFechaInicio").html(servicio[3]); 
                $("#btnAccion").attr("onclick", "abrirModal(" + servicio[0] + ")");         
                $("#tblServicios tbody").append($("#fila").
                clone(true).attr("class","otraFila"));
            });
            $("#tblServicios tbody tr").first().remove(); 
        },
        error: function(ex){
          console.log(ex.responseText);
        }
    });
}

function actualizarServicioLavado(){
    var parametros={
        idServicioLavado: idServicioLavado,
        observaciones: $("#txtObservacion").val()
    };
    $.ajax({
        url: '/actualizarServicioLavado',    
        data: parametros,
        dataType:'json',
        type: 'post',       
        cache: false,       
        success: function (resultado) {
            console.log(resultado);    
            if(resultado.estado){
                listarserviciosEnLavado();
            }      
            $("#mensaje").html(resultado.mensaje);          
        },
        error: function(ex){
          console.log(ex.responseText);
        }
    });
}

function abrirModal(id){
    idServicioLavado = id;
    $("#modalActualizarServicio").modal();   
}

function limpiar(){
    $("#txtPlaca").val("");
    $("#txtIdentificacionCliente").val();
    $("#msjPlaca").html("");
    $("#msjCliente").html("");
}