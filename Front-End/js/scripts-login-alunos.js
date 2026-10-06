const form = document.getElementById('formLogin');
const email = document.getElementById('email');
const senha = document.getElementById('senha');
const alerta = document.getElementById('alerta');
const toggle = document.getElementById('toggleSenha');
const apiProfessoresUrl = "http://127.0.0.1:5001"

toggle.addEventListener('click', () => {
    const visivel = senha.type === 'text';
    senha.type = visivel ? 'password' : 'text';
    toggle.textContent = visivel ? 'Mostrar' : 'Ocultar';
    toggle.setAttribute('aria-pressed', String(!visivel));
});


form.addEventListener('submit', (event) => {
    event.preventDefault();
    alerta.classList.add('d-none');

    const emailOk = email.checkValidity();
    const senhaOk = senha.checkValidity();
    email.classList.toggle('is-invalid', !emailOk);
    senha.classList.toggle('is-invalid', !senhaOk);
    if (!emailOk || !senhaOk) return;

    efetuarLogin()

    console.log('Login enviado:', email.value);
});

async function efetuarLogin() {
    const emailLancar = document.getElementById('email').value;
    const senhaLancar = document.getElementById('senha').value;
    const resposta = await fetch(
        `${apiProfessoresUrl}/alunos/login`,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({emailLancar, senhaLancar })
        }
    );

    const body = await resposta.json();

    if (resposta.ok){
        localStorage.setItem("token", body.token);
        window.location.replace("professor-turmas.html");
    } else{
        window.alert(body.erro)
    }
}


[email, senha].forEach((campo) =>
    campo.addEventListener('input', () => campo.classList.remove('is-invalid')));

function mostrarErro(msg) {
    alerta.textContent = msg;
    alerta.classList.remove('d-none');
}