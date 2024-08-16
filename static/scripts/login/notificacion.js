function showNotification(message, success) {
    const notification = document.getElementById('notification');
    notification.className = 'notification-box show';
    notification.style.backgroundColor = success ? 'lightgreen' : 'lightcoral';
    notification.innerText = message;

    // Ocultar la notificación después de un tiempo
    setTimeout(() => {
        notification.className = 'notification-box hide';
        // Opcionalmente, ocultar el elemento completamente después de la animación
        setTimeout(() => {
            notification.classList.remove('show', 'hide');
            notification.style.display = 'none';
        }, 500); // Tiempo igual al de la transición
    }, 3000); // Duración para que la notificación esté visible
}