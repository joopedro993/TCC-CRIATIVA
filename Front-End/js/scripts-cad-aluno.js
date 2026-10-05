const api_escola_url = "http://127.0.0.1:5003";
const api_turma_url = "http://127.0.0.1:5004";
const api_aluno_url = "http://127.0.0.1:5000";

const formulario = document.getElementById("form-cadastro");

carregarEscolas()

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
}

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
    })
}

formulario.addEventListener("submit", async function (event) {
    event.preventDefault();

    const emailAluno = document.getElementById("input-email").value;
    const nomeAluno = document.getElementById("input-nome").value.trim();
    const turmaAluno = document.getElementById("select-turma").value;
    const senhaAluno = document.getElementById("input-senha").value;

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

        formulario.reset();
    };
});