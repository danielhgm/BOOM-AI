document.addEventListener('DOMContentLoaded', function() {
    var menuButton = document.getElementById('usuario');
    var dropdownMenu = document.getElementById('dropdownMenu');

    menuButton.addEventListener('click', function(event) {
        event.preventDefault();
        dropdownMenu.classList.toggle('show');
    });

    // Cerrar el menú si se hace clic fuera de él
    window.addEventListener('click', function(event) {
        if (!event.target.matches('#usuario')) {
            if (dropdownMenu.classList.contains('show')) {
                dropdownMenu.classList.remove('show');
            }
        }
    });
});