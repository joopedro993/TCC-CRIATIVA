// ============================================================
// resultados-aluno.js
//
// Página "Meus resultados" da Área do Aluno. Mostra as redações
// já corrigidas, com a nota de cada uma das cinco competências,
// a nota total e o comentário do professor. Também mostra a média
// e a melhor nota.
//
// Se o endereço tiver ?redacao=ID, essa correção fica destacada.
//
// Depende de: base-aluno.js (carregar antes).
// Elementos da página que usa (os que faltarem são ignorados):
//   corpoResultados, vazioResultados, mediaGeral, melhorNota, alerta.
// ============================================================

// Redação que deve ficar destacada (vem do botão "Ver correção")
const idDaRedacaoEmDestaque = Number(new URLSearchParams(location.search).get("redacao"));

// Monta as duas linhas de uma correção na tabela:
//   1ª linha: Atividade | Enviada em | C1 | C2 | C3 | C4 | C5 | Total
//   2ª linha: o comentário do professor
function criarLinhasDaCorrecao(redacao, dados) {
    const correcao = dados.correcaoPorRedacao.get(Number(redacao.id_redacao));

    const atividade = dados.atividades.find(
        (item) => Number(item.id_atividade) === obterIdDaAtividadeDaRedacao(redacao)
    );

    // Primeira linha: as notas
    const linhaDasNotas = document.createElement("tr");

    adicionarCelula(linhaDasNotas, obterTituloDaAtividade(atividade) ?? redacao.tema ?? "—", "fw-semibold");
    adicionarCelula(linhaDasNotas, formatarData(obterDataDeEnvio(redacao)));

    correcao.competencias.forEach((nota) => adicionarCelula(linhaDasNotas, nota));

    adicionarCelula(linhaDasNotas, correcao.notaTotal, "fw-bold");

    // Segunda linha: o comentário, ocupando a largura toda da tabela
    const linhaDoComentario = document.createElement("tr");

    const celulaDoComentario = adicionarCelula(
        linhaDoComentario,
        correcao.comentario ? `Comentário do professor: ${correcao.comentario}` : "Sem comentário."
    );
    celulaDoComentario.colSpan = 8;

    // Destaca a correção que o aluno abriu pelo botão "Ver correção"
    if (Number(redacao.id_redacao) === idDaRedacaoEmDestaque) {
        linhaDasNotas.classList.add("table-warning");
        linhaDoComentario.classList.add("table-warning");
    }

    return [linhaDasNotas, linhaDoComentario];
}

// Ao abrir a página: carrega os dados e desenha os resultados
(async () => {
    try {
        const dados = await carregarDadosDoAluno();

        // Só as redações que já têm correção, da mais recente para a mais antiga
        const redacoesCorrigidas = dados.redacoes
            .filter((redacao) => dados.correcaoPorRedacao.has(Number(redacao.id_redacao)))
            .sort((a, b) => Number(b.id_redacao) - Number(a.id_redacao));

        pegarPorId("corpoResultados").replaceChildren(
            ...redacoesCorrigidas.flatMap((redacao) => criarLinhasDaCorrecao(redacao, dados))
        );

        // Mostra a mensagem de "lista vazia" quando ainda não há correções
        pegarPorId("vazioResultados")?.classList.toggle("d-none", redacoesCorrigidas.length > 0);

        // Média e melhor nota
        const notas = redacoesCorrigidas.map(
            (redacao) => dados.correcaoPorRedacao.get(Number(redacao.id_redacao)).notaTotal
        );

        escreverTexto(
            "mediaGeral",
            notas.length ? Math.round(notas.reduce((soma, nota) => soma + nota, 0) / notas.length) : "—"
        );
        escreverTexto("melhorNota", notas.length ? Math.max(...notas) : "—");
    } catch (erro) {
        mostrarErro(erro.message);
    }
})();