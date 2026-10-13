// ============================================================
// pendentes.js
//
// Página "Correções pendentes" da Área do Professor.
// Mostra a lista das redações que ainda não foram corrigidas,
// com um botão "Corrigir" que leva para a tela de correção.
//
// Depende de: base-professor.js (carregar antes).
// Elementos da página que usa: corpoPendentes, vazioPendentes, alerta.
// ============================================================

// Monta a linha da tabela de uma redação pendente, com as colunas:
// Aluno | Turma | Tema | Enviada em | Prazo | botão Corrigir
function criarLinhaDaPendente(redacao, dados) {
    const linha = document.createElement("tr");

    // Descobre quem escreveu, para qual atividade e de qual turma
    const aluno = dados.alunos.find(
        (item) => Number(item.id_aluno) === obterIdDoAlunoDaRedacao(redacao)
    );

    const atividade = dados.atividades.find(
        (item) => Number(item.id_atividade) === obterIdDaAtividadeDaRedacao(redacao)
    );

    const turma = dados.turmas.find(
        (item) => Number(item.id_turma) === obterIdDaTurmaDaAtividade(atividade)
    );

    // Quando alguma informação não for encontrada, a célula mostra "—"
    adicionarCelula(linha, aluno?.nome ?? "—", "fw-semibold");
    adicionarCelula(linha, turma?.nome ?? "—");
    adicionarCelula(linha, obterTituloDaAtividade(atividade) ?? "—");
    adicionarCelula(linha, formatarData(obterDataDeEnvio(redacao)));
    adicionarCelula(linha, formatarData(obterDataDoPrazo(atividade)));

    // Última coluna: botão que abre a tela de correção desta redação
    const celulaDoBotao = adicionarCelula(linha, "");

    const botaoCorrigir = document.createElement("a");
    botaoCorrigir.className = "btn btn-amarelo btn-sm";
    botaoCorrigir.textContent = "Corrigir";
    botaoCorrigir.href = `correcao.html?id=${redacao.id_redacao}`;

    celulaDoBotao.append(botaoCorrigir);

    return linha;
}

// Ao abrir a página: carrega os dados e desenha a lista de pendentes
(async () => {
    try {
        const dados = await carregarDadosDoProfessor();

        // Pendente = redação que NÃO tem nota no mapa de notas (ainda sem correção)
        const redacoesPendentes = dados.redacoes.filter(
            (redacao) => !dados.notaPorRedacao.has(Number(redacao.id_redacao))
        );

        pegarPorId("corpoPendentes").replaceChildren(
            ...redacoesPendentes.map((redacao) => criarLinhaDaPendente(redacao, dados))
        );

        // Mostra a mensagem de "lista vazia" quando não há pendências
        pegarPorId("vazioPendentes").classList.toggle("d-none", redacoesPendentes.length > 0);
    } catch (erro) {
        mostrarErro(erro.message);
    }
})();