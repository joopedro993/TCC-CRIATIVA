// ============================================================
// turmas.js
//
// Página "Turmas e alunos" da Área do Professor. Permite:
//   - ver as turmas do professor, cada uma com a tabela dos seus alunos;
//   - buscar uma turma pelo nome;
//   - criar uma turma nova.
//
// Depende de: base-professor.js (carregar antes) e do Bootstrap.
// Elementos da página que usa: buscaTurma, listaTurmas, vazioTurmas,
//   modalTurma, formTurma, nomeTurma, erroModalTurma, alerta.
// ============================================================

// Dados do professor (turmas, alunos...), preenchidos ao carregar a página
let turmasDoProfessor;
const alunosPorTurma = {};

carregarAlunosDaTurma()

async function carregarTurmas() {
    turmasDoProfessor = await buscarLista(`/turmas/professores/${idProfessor}`);
    
    desenharTurmas();
}

// Janela (modal) de "Nova turma"
const modalNovaTurma = new bootstrap.Modal(pegarPorId("modalTurma"));


// ------------------------------------------------------------
// DESENHO DA TELA
// ------------------------------------------------------------

// Monta a tabela com os alunos de uma turma (colunas: Aluno e E-mail)

function criarTabelaDeAlunos(alunosDaTurma) {
    const tabela = document.createElement("table");
    tabela.className = "table area-tabela";

    // Cabeçalho da tabela
    const linhaDoCabecalho = document.createElement("tr");

    ["Aluno", "E-mail"].forEach((titulo) => {
        const celulaDoTitulo = document.createElement("th");
        celulaDoTitulo.textContent = titulo;
        linhaDoCabecalho.append(celulaDoTitulo);
    });

    const cabecalhoDaTabela = document.createElement("thead");
    cabecalhoDaTabela.append(linhaDoCabecalho);

    // Uma linha para cada aluno
    const corpoDaTabela = document.createElement("tbody");

    alunosDaTurma.forEach((aluno) => {
        const linhaDoAluno = document.createElement("tr");

        adicionarCelula(linhaDoAluno, aluno.nome);
        adicionarCelula(linhaDoAluno, aluno.email);

        corpoDaTabela.append(linhaDoAluno);
    });

    tabela.append(cabecalhoDaTabela, corpoDaTabela);
    return tabela;
}

// Monta uma turma da lista (um "accordion" do Bootstrap):
// um botão com o nome e a quantidade de alunos e, ao clicar,
// a área que abre mostrando a tabela de alunos.
function criarItemDaTurma(turma) {

    // O botão e a área que abre precisam se ligar pelo id (turma1, turma2...)
    const idDaAreaRecolhivel = `turma${turma.id_turma}`;

    const itemDaTurma = document.createElement("div");
    itemDaTurma.className = "accordion-item";

    // Cabeçalho com o botão
    const cabecalho = document.createElement("h2");
    cabecalho.className = "accordion-header";

    const botaoDaTurma = document.createElement("button");
    botaoDaTurma.className = "accordion-button collapsed";
    botaoDaTurma.type = "button";
    botaoDaTurma.textContent = `${turma.nome} · ${turma.length} aluno(s)`;
    botaoDaTurma.dataset.bsToggle = "collapse";
    botaoDaTurma.dataset.bsTarget = `#${idDaAreaRecolhivel}`;

    cabecalho.append(botaoDaTurma);

    // Área que abre e fecha
    const areaRecolhivel = document.createElement("div");
    areaRecolhivel.id = idDaAreaRecolhivel;
    areaRecolhivel.className = "accordion-collapse collapse";

    const corpoDaTurma = document.createElement("div");
    corpoDaTurma.className = "accordion-body";

    corpoDaTurma.textContent = "Carregando alunos...";

    areaRecolhivel.addEventListener("show.bs.collapse", () =>
        carregarAlunosDaTurma(turma, botaoDaTurma, corpoDaTurma)
    );

    areaRecolhivel.append(corpoDaTurma);
    itemDaTurma.append(cabecalho, areaRecolhivel);

    return itemDaTurma;
}

// Redesenha a lista de turmas, respeitando o texto digitado na busca
function desenharTurmas() {
    const textoDaBusca = pegarPorId("buscaTurma").value.toLowerCase();

    const turmasFiltradas = turmasDoProfessor.turmas.filter((turma) =>
        (turma.nome || "").toLowerCase().includes(textoDaBusca)
    );

    pegarPorId("listaTurmas").replaceChildren(...turmasFiltradas.map(criarItemDaTurma));

    // Mostra a mensagem de "lista vazia" quando não sobrou nenhuma turma
    pegarPorId("vazioTurmas").classList.toggle("d-none", turmasFiltradas.length > 0);
}


// ------------------------------------------------------------
// INÍCIO DA PÁGINA
// ------------------------------------------------------------

// Ao abrir a página: carrega os dados e desenha as turmas
(async () => {
    try {
        turmasDoProfessor = await carregarDadosDoProfessor();
        desenharTurmas();
    } catch (erro) {
        mostrarErro(erro.message);
    }
})();

// A cada letra digitada na busca, redesenha a lista
// (só depois que os dados já tiverem sido carregados)
pegarPorId("buscaTurma").addEventListener("input", () => {
    if (turmasDoProfessor) desenharTurmas();
});


// ------------------------------------------------------------
// CRIAR TURMA
// ------------------------------------------------------------

pegarPorId("formTurma").addEventListener("submit", async (evento) => {
    // Impede o envio padrão do formulário (que recarregaria a página)
    evento.preventDefault();

    try {
        // O POST /turmas da API lê os campos "nome" e "professor"
        await chamarApi("/turmas", {
            method: "POST",
            body: JSON.stringify({
                nome: pegarPorId("nomeTurma").value.trim(),
                professor: idProfessor
            })
        });

        modalNovaTurma.hide();
        pegarPorId("formTurma").reset();

        // Recarrega os dados para a nova turma aparecer na lista
        turmasDoProfessor = await carregarDadosDoProfessor();
        desenharTurmas();
    } catch (erro) {
        // Mostra o erro dentro da janela, para o professor poder corrigir
        mostrarErro(erro.message, "erroModalTurma");
    }
});

async function carregarAlunosDaTurma(turma, botaoDaTurma, corpoDaTurma) {
    try {
        // Se já buscou antes, reaproveita; senão, pergunta à API
        let alunos = alunosPorTurma[turma.id_turma];

        if (!alunos) {
            alunos = await buscarLista(`/alunos/turmas/${turma.id_turma}`);
            alunosPorTurma[turma.id_turma] = alunos;
        }

        botaoDaTurma.textContent = `${turma.nome} · ${alunos.length} aluno(s)`;

        corpoDaTurma.replaceChildren(
            alunos.length > 0 ? criarTabelaDeAlunos(alunos) : "Nenhum aluno cadastrado."
        );
    } catch (erro) {
        corpoDaTurma.textContent = "Não foi possível carregar os alunos: " + erro.message;
    }
}