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

  //Desvanecimiento de .quehacemos al momento de scroll hacia abajo
