  //Recargar pagina automaticamente

  document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io();
    socket.on('connect', function() {
        socket.send('User has connected!');
    });

    socket.on('message', function(data) {
        console.log(data);
        // Actualiza la página sin recargarla
    });
});