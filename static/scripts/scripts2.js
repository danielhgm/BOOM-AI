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

function toggleContrast() {
    var elementsToToggle = document.querySelectorAll('body, .right-side'); // Añadir aquí otros selectores si es necesario
    elementsToToggle.forEach(function(element) {
        if (element.classList.contains('dark-mode')) {
            element.classList.remove('dark-mode');
            element.classList.add('light-mode');
        } else {
            element.classList.remove('light-mode');
            element.classList.add('dark-mode');
        }
    });
}



// Highlight the top nav as scrolling occurs
$('body').scrollspy({
    target: '.navbar-fixed-top'
})