 // Exponer la función para que pueda ser llamada desde HTML
 window.cerrarLogin = cerrarLogin;

function cerrarLogin() {
    document.querySelector('.form').style.display = 'none';
    document.querySelector('.overlay_crear_cuenta').style.display = 'none';
  }