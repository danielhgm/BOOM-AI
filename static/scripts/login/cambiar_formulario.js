// Función para mostrar un formulario y ocultar el otro
function switchForm(showForm) {
    const loginForm = document.getElementById('iniciar_sesion-frame');
    const registerForm = document.getElementById('crear_cuenta-frame');
    const overlayLogin = document.getElementById('overlay_iniciar_sesion');
    const overlayRegister = document.getElementById('overlay_crear_cuenta');
  
    if (showForm === 'login') {
      loginForm.style.display = 'block';
      overlayLogin.style.display = 'block';
      registerForm.style.display = 'none';
      overlayRegister.style.display = 'none';
    } else if (showForm === 'register') {
      loginForm.style.display = 'none';
      overlayLogin.style.display = 'none';
      registerForm.style.display = 'block';
      overlayRegister.style.display = 'block';
    }
  }
  
  // Exponer la función para que pueda ser llamada desde HTML
  window.switchForm = switchForm;