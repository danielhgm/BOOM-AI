function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

function toggleContrast() {
    var rightSide = document.getElementById('right-side');
    if (rightSide.classList.contains('dark-mode')) {
        rightSide.classList.remove('dark-mode');
        rightSide.classList.add('light-mode');
    } else {
        rightSide.classList.remove('light-mode');
        rightSide.classList.add('dark-mode');
    }
}