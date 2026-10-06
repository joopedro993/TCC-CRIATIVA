const api_escola_url = "http://127.0.0.1:5003";
const api_turma_url = "http://127.0.0.1:5004";
const api_aluno_url = "http://127.0.0.1:5000";

const email = document.getElementById('input-email');
const senha = document.getElementById('input-senha');
const nome = document.getElementById("input-nome");
const escola = document.getElementById("select-escola");
const turma = document.getElementById("select-turma");
const alerta = document.getElementById('alerta');
const toggle = document.getElementById('toggleSenha');


const formulario = document.getElementById("form-cadastro");

carregarEscolas();

formulario.addEventListener('submit', (event) =>{
    event.preventDefault();
    alerta.classList.add("d-none");

    const emailOk = email.checkValidity();
    const senhaOk = senha.checkValidity();
    const nomeOk = !!nome.value.trim();
    const escolaOk = !!escola.value.trim(); 
    const turmaOk = !!turma.value.trim(); 

    email.classList.toggle("is-invalid", !emailOk);
    senha.classList.toggle('is-invalid', !senhaOk);
    nome.classList.toggle('is-invalid', !nomeOk);
    escola.classList.toggle('is-invalid', !escolaOk);
    turma.classList.toggle('is-invalid', !turmaOk);

    if (!emailOk || !senhaOk || !nomeOk || escolaOk || turmaOk) return;

    [email, senha, nome].forEach((campo) =>
    campo.addEventListener("input", () => campo.classList.remove("is-invalid")));

    efetuarCadastro();

    console.log('Cadastro enviado: ', email.value)

});

async function carregarEscolas() {
    const resposta = await fetch(`${api_escola_url}/escolas`);
    const escolas = await resposta.json();

    const selectEscolas = document.getElementById("select-escola");

    escolas.forEach(escola => {
        selectEscolas.innerHTML += `
        <option value="${escola.id_escola}">
            ${escola.nome}
        </option>
        `

    });
};

async function carregarTurmas() {
    const resposta = await fetch(`${api_turma_url}/turmas`);
    const turmas = await resposta.json();

    const selectCursos = document.getElementById("select-turma");

    turmas.forEach(turma => {
        selectCursos.innerHTML += `
        <option value="${turma.id_turma}">
            ${turma.nome}
        </option>
        `
    });
};

async function efetuarCadastro() {

    const emailAluno = email.value;
    const nomeAluno = nome.value.trim();
    const turmaAluno = document.getElementById("select-turma").value;
    const senhaAluno = senha.value;

    if (emailAluno !== "" && nomeAluno !== "" && turmaAluno !== "" && senhaAluno !== "") {
        const aluno = {
            email: emailAluno,
            nome: nomeAluno,
            senha: senhaAluno
        }

        const resposta = await fetch(
            `${api_aluno_url}/alunos`,
            {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(aluno)
            });

        const novoAluno = await resposta.json();
        console.log(novoAluno);

        window.alert("Cadastro efetuado, faça seu Login!")

        if (resposta.ok){
            window.location.replace("login-alunos.html");
        }

        formulario.reset();
    };
};


toggle.addEventListener('click', () => {
    const visivel = senha.type === 'text';
    senha.type = visivel ? 'password' : 'text';
    toggle.textContent = visivel ? 'Mostrar' : 'Ocultar';
    toggle.setAttribute('aria-pressed', String(!visivel));
});