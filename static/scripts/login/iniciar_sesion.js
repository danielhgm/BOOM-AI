function cerrarIniciarSesion() {
  document.getElementById('overlay_iniciar_sesion').style.display = 'none';
  document.getElementById('iniciar_sesion-frame').style.display = 'none';
}

// Asocia la función al evento de clic en el enlace "Iniciar sesión"
document.getElementById('showLoginForm').addEventListener('click', function(event) {
  event.preventDefault(); // Evitar que el enlace navegue
  showLoginForm();
});

// Función para mostrar el formulario de inicio de sesión
function showLoginForm() {
  document.getElementById('overlay_iniciar_sesion').style.display = 'block';
  document.getElementById('iniciar_sesion-frame').style.display = 'block';
}

// Manejar clics en el documento para cerrar el formulario de inicio de sesión
document.addEventListener('click', function(event) {
  // Verifica si el clic ocurrió fuera del formulario y del overlay
  if (iniciar_sesion-frame && overlay_iniciar_sesion && !iniciar_sesion-frame.contains(event.target) && !overlay_iniciar_sesion.contains(event.target)) {
    // Cierra el formulario de inicio de sesión y el overlay
    loginForm.style.display = 'none';
    overlayLogin.style.display = 'none';
  }
});

// Asocia la función al evento de clic en el enlace "Iniciar sesión"
document.getElementById('showLoginForm').addEventListener('click', function(event) {
  event.preventDefault(); // Evitar que el enlace navegue
  showLoginForm();
});

// Esto es para iniciar sesion|ingresar
document.getElementById('loginForm').addEventListener('submit', function(event) {
  event.preventDefault();

  const email = document.getElementById('loginEmail').value;
  const password = document.getElementById('loginPassword').value;

  fetch('/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          email: email,
          password: password
      })
  })
  .then(response => response.json())
.then(data => {
    //se documentaron las 2 opciones ya que es mejor para que sea instantaneo
    //alert(data.message); // Mostrar la alerta con el mensaje recibido
    //showNotification(data.message, data.success);  // Mostrar la notificacion con el mensaje recibido

    if (data.success && data.redirect_url) {
        // Redirigir a la URL proporcionada en el JSON
        window.location.href = data.redirect_url;
    }
}).catch(error => console.error('Error:', error));
})