$(document).ready(function() {
    // Función para cargar la barra de progreso
    function actualizarLaBarra() {
        $.ajax({
            url: '/aceites/actualizaaceites/',  // URL de la vista que devuelve los datos actualizados
            success: function(data) {
                // Actualizar el contenido de la página con los nuevos datos
                actualizarAceites(data);
            }
        });
    }

    // Función para actualizar los tanques
    function actualizarAceites(aceites) {
        var container = $('#aceites-container');
        container.empty();  // Limpiar el contenedor antes de agregar nuevos datos

        // Iterar sobre los tanques y agregarlos al contenedor
        $.each(aceites, function(index, aceite) {
            var porcentaje = (aceite.cantidad_aceite * 100) / aceite.capacidad_aceite;

            var progressBar = $('<div class="barra-progreso">').append(
                $('<div class="barra-progreso-fill">').css('width', porcentaje + '%')
            );

            var aceiteInfo = $('<div class="aceite">').append(
                $('<div class="nombre">').text(aceite.nombre),
                $('<div class="tipo">').text(aceite['tipo de aceite']),
                $('<div class="capacidad">').text('Capacidad: ' + aceite.capacidad_aceite + ' litros'),
                $('<div class="cantidad">').text('Cantidad de aceite: ' + aceite.cantidad_aceite + ' litros'),
                progressBar
            );

            container.append(aceiteInfo);
        });
    }

    // Configurar intervalo de actualización
    setInterval(actualizarLaBarra, 2000);
});
