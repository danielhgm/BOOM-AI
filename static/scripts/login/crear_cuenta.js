// Asocia la función al evento de clic en el enlace "Crear cuenta"
document.getElementById('showRegisterForm').addEventListener('click', function(event) {
  event.preventDefault(); // Evitar que el enlace navegue
  showRegisterForm();
});

// Llama a showRegisterForm() para mostrar el formulario de registro
function showRegisterForm() {
  document.getElementById('overlay_crear_cuenta').style.display = 'block';
  document.getElementById('crear_cuenta-frame').style.display = 'block';
}

// Función para ocultar el formulario de inicio de sesión
function hideRegisterForm() {
  document.getElementById('overlay_crear_cuenta').style.display = 'none';
  document.getElementById('crear_cuenta-frame').style.display = 'none';
}

// Manejar clics en el documento para cerrar el formulario de inicio de sesión
document.addEventListener('mousedown', function(event) {
  const registerForm = document.getElementById('crear_cuenta-frame');
  const overlayregister = document.getElementById('overlay_crear_cuenta');

  // Verifica si el clic fue fuera del formulario de inicio de sesión
  if (overlayregister.style.display === 'block' && !registerForm.contains(event.target) && !overlayregister.contains(event.target)) {
    hideregisterForm();
  }
});

// Esto es para registrarse|crear cuenta, se envia a app.py con POST
document.getElementById('registerForm').addEventListener('submit', function(event) {
  event.preventDefault();

  const username = document.getElementById('username').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  fetch('/register', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          username: username,
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

