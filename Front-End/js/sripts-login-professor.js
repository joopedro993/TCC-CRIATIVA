const form = document.getElementById('formLogin');
const email = document.getElementById('email');
const senha = document.getElementById('senha');
const alerta = document.getElementById('alerta');
const toggle = document.getElementById('toggleSenha');


toggle.addEventListener('click', () => {
    const visivel = senha.type === 'text';
    senha.type = visivel ? 'password' : 'text';
    toggle.textContent = visivel ? 'Mostrar' : 'Ocultar';
    toggle.setAttribute('aria-pressed', String(!visivel));
});


form.addEventListener('submit', (e) => {
    e.preventDefault();
    alerta.classList.add('d-none');

    const emailOk = email.checkValidity();
    const senhaOk = senha.checkValidity();
    email.classList.toggle('is-invalid', !emailOk);
    senha.classList.toggle('is-invalid', !senhaOk);
    if (!emailOk || !senhaOk) return;


    console.log('Login enviado:', email.value);
});


[email, senha].forEach((campo) =>
    campo.addEventListener('input', () => campo.classList.remove('is-invalid')));

function mostrarErro(msg) {
    alerta.textContent = msg;
    alerta.classList.remove('d-none');
}