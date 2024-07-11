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



