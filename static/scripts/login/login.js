function showNotification(message, success) {
    const notification = document.getElementById('notification');
    notification.style.display = 'block';
    notification.style.backgroundColor = success ? 'lightgreen' : 'lightcoral';
    notification.innerText = message;
}

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