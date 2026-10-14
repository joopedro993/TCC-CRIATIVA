// ============================================================
// atividades.js
//
// Página "Atividades" da Área do Professor. Permite:
//   - ver as atividades das turmas do professor, com a situação
//     (agendada, aberta ou encerrada) e quantas redações chegaram;
//   - filtrar as atividades por situação;
//   - criar uma atividade nova a partir de um tema e de uma turma.
//
// Depende de: base-professor.js (carregar antes) e do Bootstrap.
// Elementos da página que usa: filtroSituacao, corpoAtividades,
//   vazioAtividades, btnNovaAtividade, modalAtividade, formAtividade,
//   selTema, selTurmaAtv, dataAbertura, dataPrazo, erroModalAtividade, alerta.
// ============================================================

// Dados do professor (turmas, alunos, atividades...), preenchidos ao carregar a página
let dadosDoProfessor;

// Janela (modal) de "Nova atividade"
const modalNovaAtividade = new bootstrap.Modal(pegarPorId("modalAtividade"));


// ------------------------------------------------------------
// DESENHO DA TELA
// ------------------------------------------------------------

// Monta a linha da tabela de uma atividade, com as colunas:
// Tema | Turma | Abertura | Prazo | Situação | Enviadas/Total de alunos | Corrigidas
function criarLinhaDaAtividade(atividade) {
    const linha = document.createElement("tr");

    const titulo = obterTituloDaAtividade(atividade) ?? "(sem título)";
    const idDaTurma = obterIdDaTurmaDaAtividade(atividade);
    const idDaAtividade = Number(atividade.id_atividade);

    const turma = dadosDoProfessor.turmas.find(
        (item) => Number(item.id_turma) === idDaTurma
    );

    // Redações já enviadas para esta atividade
    const redacoesDaAtividade = dadosDoProfessor.redacoes.filter(
        (redacao) => obterIdDaAtividadeDaRedacao(redacao) === idDaAtividade
    );

    // Dessas, quantas já foram corrigidas (têm nota no mapa de notas)
    const quantidadeCorrigidas = redacoesDaAtividade.filter((redacao) =>
        dadosDoProfessor.notaPorRedacao.has(Number(redacao.id_redacao))
    ).length;

    // Total de alunos da turma (para mostrar "enviadas/total")
    const totalDeAlunosDaTurma = dadosDoProfessor.alunos.filter(
        (aluno) => obterIdDaTurmaDoAluno(aluno) === idDaTurma
    ).length;

    const situacao = calcularSituacao({
        abertura: obterDataDeAbertura(atividade),
        prazo: obterDataDoPrazo(atividade)
    });

    adicionarCelula(linha, titulo, "fw-semibold");
    adicionarCelula(linha, turma?.nome ?? "—");
    adicionarCelula(linha, formatarData(obterDataDeAbertura(atividade)));
    adicionarCelula(linha, formatarData(obterDataDoPrazo(atividade)));
    adicionarCelula(linha, situacao);
    adicionarCelula(linha, `${redacoesDaAtividade.length}/${totalDeAlunosDaTurma}`);
    adicionarCelula(linha, quantidadeCorrigidas);

    return linha;
}

// Redesenha a tabela de atividades, respeitando o filtro de situação
function desenharAtividades() {
    // Filtro escolhido pelo professor ("" significa "todas")
    const situacaoEscolhida = pegarPorId("filtroSituacao").value;

    const atividadesFiltradas = dadosDoProfessor.atividades.filter((atividade) => {
        if (!situacaoEscolhida) return true;

        const situacaoDaAtividade = calcularSituacao({
            abertura: obterDataDeAbertura(atividade),
            prazo: obterDataDoPrazo(atividade)
        });

        return situacaoDaAtividade === situacaoEscolhida;
    });

    pegarPorId("corpoAtividades").replaceChildren(
        ...atividadesFiltradas.map(criarLinhaDaAtividade)
    );

    // Mostra a mensagem de "lista vazia" quando não sobrou nenhuma atividade
    pegarPorId("vazioAtividades").classList.toggle("d-none", atividadesFiltradas.length > 0);
}


// ------------------------------------------------------------
// INÍCIO DA PÁGINA
// ------------------------------------------------------------

// Ao abrir a página: carrega os dados e desenha as atividades
(async () => {
    try {
        dadosDoProfessor = await carregarDadosDoProfessor();
        desenharAtividades();
    } catch (erro) {
        mostrarErro(erro.message);
    }
})();

// Ao trocar o filtro de situação, redesenha a tabela
// (só depois que os dados já tiverem sido carregados)
pegarPorId("filtroSituacao").addEventListener("change", () => {
    if (dadosDoProfessor) desenharAtividades();
});


// ------------------------------------------------------------
// CRIAR ATIVIDADE
// ------------------------------------------------------------

// Prepara e abre a janela "Nova atividade"
async function abrirModalNovaAtividade() {
    try {
        // Recarrega os dados para as listas de temas e turmas estarem atualizadas
        dadosDoProfessor = await carregarDadosDoProfessor();

        // Lista de temas (a primeira opção é só um aviso, sem valor)
        pegarPorId("selTema").replaceChildren(
            new Option("Selecione um tema", ""),
            ...dadosDoProfessor.temas.map(
                (tema) => new Option(tema.titulo ?? tema.nome ?? tema.tema, tema.id_tema)
            )
        );

        // Lista de turmas do professor
        pegarPorId("selTurmaAtv").replaceChildren(
            new Option("Selecione uma turma", ""),
            ...dadosDoProfessor.turmas.map((turma) => new Option(turma.nome, turma.id_turma))
        );

        // As duas datas começam em hoje
        pegarPorId("dataAbertura").value = dataDeHoje();
        pegarPorId("dataPrazo").value = dataDeHoje();

        modalNovaAtividade.show();
    } catch (erro) {
        mostrarErro(erro.message);
    }
}

pegarPorId("btnNovaAtividade").addEventListener("click", abrirModalNovaAtividade);

pegarPorId("formAtividade").addEventListener("submit", async (evento) => {
    // Impede o envio padrão do formulário (que recarregaria a página)
    evento.preventDefault();

    try {
        const temaEscolhido = dadosDoProfessor.temas.find(
            (tema) => Number(tema.id_tema) === Number(pegarPorId("selTema").value)
        );

        const dataDeAbertura = pegarPorId("dataAbertura").value;
        const dataLimite = pegarPorId("dataPrazo").value;

        if (dataLimite < dataDeAbertura) {
            throw Error("O prazo não pode ser anterior à abertura.");
        }

        // O título e a descrição da atividade vêm do tema escolhido
        const tituloDoTema = temaEscolhido?.titulo ?? temaEscolhido?.nome;
        let descricaoDoTema = temaEscolhido?.textos_motivadores ?? temaEscolhido?.descricao ?? tituloDoTema;
        if (Array.isArray(descricaoDoTema)) {
            descricaoDoTema = descricaoDoTema.join("\n\n");
        } else if (typeof descricaoDoTema === 'string' && descricaoDoTema.startsWith('[')) {
            try {
                const parsed = JSON.parse(descricaoDoTema);
                if (Array.isArray(parsed)) descricaoDoTema = parsed.join("\n\n");
            } catch (e) {}
        }

        const idTemaValor = Number(pegarPorId("selTema").value);
        if (!idTemaValor) {
            throw Error("Por favor, selecione um tema válido.");
        }

        // O POST /atividades da API exige estes seis campos
        await chamarApi("/atividades", {
            method: "POST",
            body: JSON.stringify({
                titulo: tituloDoTema,
                tema: tituloDoTema,
                descricao: descricaoDoTema,
                data_disponibilizacao: dataDeAbertura,
                prazo: dataLimite,
                id_turma: Number(pegarPorId("selTurmaAtv").value),
                id_tema: temaEscolhido.id_tema
            })
        });

        modalNovaAtividade.hide();

        // Recarrega os dados para a nova atividade aparecer na tabela
        dadosDoProfessor = await carregarDadosDoProfessor();
        desenharAtividades();
    } catch (erro) {
        // Mostra o erro dentro da janela, para o professor poder corrigir
        mostrarErro(erro.message, "erroModalAtividade");
    }
});