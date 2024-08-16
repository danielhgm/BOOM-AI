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

// Función para ocultar el formulario de inicio de sesión
function hideLoginForm() {
  document.getElementById('overlay_iniciar_sesion').style.display = 'none';
  document.getElementById('iniciar_sesion-frame').style.display = 'none';
}

// Manejar clics en el documento para cerrar el formulario de inicio de sesión
document.addEventListener('mousedown', function(event) {
  const loginForm = document.getElementById('iniciar_sesion-frame');
  const overlayLogin = document.getElementById('overlay_iniciar_sesion');

  // Verifica si el clic fue fuera del formulario de inicio de sesión
  if (overlayLogin.style.display === 'block' && !loginForm.contains(event.target) && !overlayLogin.contains(event.target)) {
    hideLoginForm();
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
      showNotification(data.message, data.success);
  })
  .catch(error => {
      showNotification('Error: ' + error, false);
  });
});

