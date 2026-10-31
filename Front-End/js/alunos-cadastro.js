const apiURL = "http://127.0.0.1:5010";

const email = document.getElementById('input-email');
const senha = document.getElementById('input-senha');
const nome = document.getElementById("input-nome");
const escola = document.getElementById("select-escola");
const professor = document.getElementById("select-professor")
const turma = document.getElementById("select-turma");
const alerta = document.getElementById('alerta');
const toggle = document.getElementById('toggleSenha');
const btnCadastrar = document.getElementById('btnCadastrar')

const formulario = document.getElementById("form-cadastro");

carregarEscolas();

formulario.addEventListener('submit', (event) => {
    event.preventDefault();
    alerta.classList.add("d-none");

    const emailOk = email.checkValidity();
    const senhaOk = senha.checkValidity();
    const nomeOk = !!nome.value.trim();
    const escolaOk = !!escola.value.trim();
    const turmaOk = !!turma.value.trim();
    const professorOk = !!professor.value.trim();

    email.classList.toggle("is-invalid", !emailOk);
    senha.classList.toggle('is-invalid', !senhaOk);
    nome.classList.toggle('is-invalid', !nomeOk);
    escola.classList.toggle('is-invalid', !escolaOk);
    turma.classList.toggle('is-invalid', !turmaOk);
    professor.classList.toggle('is-invalid', !professorOk);

    if (!emailOk || !senhaOk || !nomeOk || !escolaOk || !turmaOk || !professorOk) return;

    [email, senha, nome, escola, turma, professor].forEach((campo) =>
        campo.addEventListener("input", () => campo.classList.remove("is-invalid")));

    efetuarCadastro(event);


});

document.getElementById("select-escola").addEventListener("change", function () {
    const id_escola = this.value;

    carregarProfessores(id_escola);
});

document.getElementById("select-professor").addEventListener("change", function () {
    const id_professor = this.value;

    carregarTurmas(id_professor);
});

// Mantém só a primeira opção ("Selecione...") do HTML e preenche o resto
function preencherSelect(select, itens, campoId) {
    select.length = 1;
    select.selectedIndex = 0;
    itens.forEach((item) => select.append(new Option(item.nome, item[campoId])));
}


async function carregarEscolas() {
    const resposta = await fetch(`${apiURL}/escolas`);
    preencherSelect(escola, await resposta.json(), "id_escola")
  
};

async function carregarProfessores(id_escola) {
    preencherSelect(turma, [], "id_turma");
    const resposta = await fetch(`${apiURL}/professores/escola/${id_escola}`);
    preencherSelect(professor, await resposta.json(), "id_professor");

}

async function carregarTurmas(id_professor) {
    const resposta = await fetch(`${apiURL}/turmas/professores/${id_professor}`);
    preencherSelect(turma, await resposta.json(), "id_turma")
    
};

async function efetuarCadastro(event) {
    if (event) event.preventDefault();

    const emailAluno = email.value.toLowerCase().trim();
    const nomeAluno = nome.value.trim();
    const turmaAluno = document.getElementById("select-turma").value;
    const senhaAluno = senha.value.trim();

    if (emailAluno !== "" && nomeAluno !== "" && turmaAluno !== "" && senhaAluno !== "") {
        const aluno = {
            email: emailAluno,
            nome: nomeAluno,
            senha: senhaAluno,
            turma: Number(turmaAluno)
        }
        btnCadastrar.disabled = true;
        try {
            const resposta = await fetch(
                `${apiURL}/alunos`,
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(aluno)
                });

            const novoAluno = await resposta.json().catch(() => ({}));

            if (resposta.ok) {
                window.alert("Cadastro efetuado, faça seu Login!");
                formulario.reset();
                
                window.location.replace("login-alunos.html");
                return;

            }

            mostrarErro(novoAluno.erro || "Não foi possível concluir o cadastro.");

        } catch {
            mostrarErro("Não foi possível conectar ao servidor.")

        }
        btnCadastrar.disabled = false;

    };
};


toggle.addEventListener('click', () => {
    const visivel = senha.type === 'text';
    senha.type = visivel ? 'password' : 'text';
    toggle.textContent = visivel ? 'Mostrar' : 'Ocultar';
    toggle.setAttribute('aria-pressed', String(!visivel));
});