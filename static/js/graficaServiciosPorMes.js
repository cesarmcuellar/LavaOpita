/*Se carga la visualización de la API y el paquete corechart*/
/* global google */

google.charts.load('current', { 'packages': ['corechart'] });

/* Establecer una devolución de llamada para que se ejecute 
cuando se carga la API de visualización de Google.*/
google.charts.setOnLoadCallback(dibujarGrafica);

/* Código que obtiene los datos del servidor, para lo cual haremos una 
 * petición ajax que devolverá un JSON con la información a graficar 
 * que se se almacenará en la variable datos*/
var datos;
function dibujarGrafica() {    
    $.ajax({
        url: '/ingresosPorMes',        
        dataType: "json",
        type: 'post',
        async: false,
        success: function (resultado) {
           datos = resultado.datos;
           console.log(datos); 
        },
        error: function (error) {
            console.log(error.responseText);
        }
    });
   
    //Se crea una tabla y se llena con los datos obtenidos
    var data = new google.visualization.arrayToDataTable(datos);    
   
    /* Se definen algunas opciones para el gráfico*/
    var options = {
        title: 'Ingresos por Mes',
        hAxis: { title: 'Meses', titleTextStyle: { color: 'red' } },
        vAxis: { title: 'Ingresos', titleTextStyle: { color: 'blue' } },          
        legend: { position: "none" }      
        };
  
    /* se crea un objeto de la clase google.visualization.ColumnChart  
     * ( Grafica de columna ) y se le pasa como parametro el div del 
     * HTML que contendrá a la gráfica.*/
    var grafica = new google.visualization.ColumnChart(document.getElementById('grafica'));
    /* Se llama al método draw para dibujar la gráfica*/
    grafica.draw(data, options);
}

