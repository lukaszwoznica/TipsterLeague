const passwordInput = document.getElementById('id_password');
const eye_icon = document.getElementById('passwordIcon');

eye_icon.addEventListener('click', togglePass);

function togglePass() {
    eye_icon.classList.toggle('active');
    (passwordInput.type === 'password') ? passwordInput.type = 'text' : passwordInput.type = 'password';
}