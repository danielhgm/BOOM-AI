//esto es para la notificacion de cuando avisa si, si accedio, creo la cuenta etc.

function showNotification(message, success) {
    const notification = document.getElementById('notification');
    notification.style.display = 'block';
    notification.style.backgroundColor = success ? 'lightgreen' : 'lightcoral';
    notification.innerText = message;
}