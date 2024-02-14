$(document).ready(function() {
    // cargo la barra de progreso
    function actualizarBarra() {
        $.ajax({
            url: '/combustible/actualizartanques/',  // URL de la vista que devuelve los datos actualizados
            success: function(data) {
                // Actualizar el contenido de la página con los nuevos datos
                actualizarTanques(data);
            }
        });
    }

    // actualizo los tanques
    function actualizarTanques(tanques) {
        var container = $('#tanques-container');
        container.empty();  // Limpiar el contenedor antes de agregar nuevos datos

        // con esto actualizo la pagina
        $.each(tanques, function(index, tanque) {
            var progressBar = $('<progress>')
                .attr('value', tanque.cantidad_combustible)
                .attr('max', tanque.capacidad);

            var tanqueInfo = $('<div>')
                .text(tanque.nombre + ': ' + tanque.cantidad_combustible + ' / ' + tanque.capacidad)
                .append(progressBar);

            container.append(tanqueInfo);
        });
    }

    // aca modifico el tiempo de consulta
    setInterval(actualizarBarra, 2000);
});