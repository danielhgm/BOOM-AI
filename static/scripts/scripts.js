//abrir y cerrar menu lateral

function openNav() {
    var links = document.getElementById("mySidenav").querySelectorAll("a");
    links.forEach(function(link) {
        link.classList.add("visible");
    });
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
    var links = document.getElementById("mySidenav").querySelectorAll("a");
    links.forEach(function(link) {
        link.classList.remove("visible");
    });
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
}

//Nav var al deslizar hacia abajo

window.addEventListener('scroll', function() {
    document.body.classList.toggle('scrolled', window.scrollY > 50);
    });

window.addEventListener('scroll', function() {
    var nav = document.querySelector('nav');
    if (window.scrollY > 0) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
  });

// Esto es para registrarse|crear cuenta

function showNotification(message, success) {
    const notification = document.getElementById('notification');
    notification.style.display = 'block';
    notification.style.backgroundColor = success ? 'lightgreen' : 'lightcoral';
    notification.innerText = message;
  }

  document.getElementById('registerForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const username = document.getElementById('registerUsario').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

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

// Esto es para iniciar sesion|ingresar


  document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const username = document.getElementById('loginUsuario').value;
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




  