// ============================================================
// atividades-aluno.js
//
// Página inicial da Área do Aluno (atividades-aluno.html).
// Mostra as atividades da turma do aluno como CARTÕES, cada um dentro
// de uma coluna do Bootstrap (col-12 col-md-4: um cartão por linha no
// celular e três por linha no computador).
//
// Os cartões ficam em duas linhas (row) da página:
//   1ª linha  "Para fazer": atividades abertas em que o aluno ainda
//             não enviou a redação (as de prazo mais próximo primeiro);
//   2ª linha  "Enviadas, corrigidas e encerradas": todas as outras.
//
// Depende de: base-aluno.js (carregar antes).
// Elementos da página que usa:
//   atividadesParaFazer e atividadesConcluidas -> as duas linhas (row).
//     Se não tiverem esses ids, o script usa as duas primeiras linhas
//     dentro de ".turmas-vidro.mt-4".
//   nomeAluno (ou nomeProfessor) -> nome na saudação (opcional)
//   alerta -> aviso de erro (opcional)
// Páginas para onde leva: redacao.html (escrever) e resultados.html (ver correção).
// ============================================================

// Classes da coluna de cada cartão
const CLASSES_DA_COLUNA = "col-12 col-md-4";


// ------------------------------------------------------------
// MONTAR OS CARTÕES
// ------------------------------------------------------------

// Cria um elemento com classe e texto (atalho para deixar o código mais curto)
function criarElemento(tag, classe, texto) {
    const elemento = document.createElement(tag);

    if (classe) elemento.className = classe;
    if (texto !== undefined) elemento.textContent = texto;

    return elemento;
}

// Descobre como a atividade deve aparecer para este aluno:
//   etiqueta -> texto da etiqueta colorida do cartão
//   destaque -> true para a etiqueta amarela (precisa de atenção)
//   botao    -> { texto, classe, endereco } ou null quando não há ação
function descreverAtividade(atividade, dados) {
    const idDaAtividade = Number(atividade.id_atividade);

    const situacao = calcularSituacao({
        abertura: obterDataDeAbertura(atividade),
        prazo: obterDataDoPrazo(atividade)
    });

    const redacao = encontrarRedacaoDaAtividade(dados, idDaAtividade);
    const estado = descobrirEstadoDaRedacao(redacao, dados);

    if (estado === "corrigida") {
        const correcao = dados.correcaoPorRedacao.get(Number(redacao.id_redacao));

        return {
            etiqueta: `Corrigida · nota ${correcao.notaTotal}`,
            destaque: false,
            botao: {
                texto: "Ver correção",
                classe: "btn btn-roxo",
                endereco: `aluno-consulta-correcao.html?redacao=${redacao.id_redacao}`
            }
        };
    }

    if (estado === "enviada") {
        return { etiqueta: "Enviada · aguardando correção", destaque: false, botao: null };
    }

    // Ainda não enviada
    if (situacao === "aberta") {
        return {
            etiqueta: "Para fazer",
            destaque: true,
            botao: {
                texto: "Escrever redação",
                classe: "btn btn-amarelo",
                endereco: `aluno-redacao.html?atividade=${idDaAtividade}`
            }
        };
    }

    return { etiqueta: "Prazo encerrado", destaque: false, botao: null };
}

// Monta uma coluna com o cartão de uma atividade:
//   título | datas | etiqueta de estado | botão
function criarCartaoDaAtividade(atividade, dados) {
    const descricao = descreverAtividade(atividade, dados);

    const coluna = criarElemento("div", CLASSES_DA_COLUNA);
    const cartao = criarElemento("div", "turma-card turmas-vidro");

    cartao.append(
        criarElemento("h3", "turma-nome", obterTituloDaAtividade(atividade) ?? "(sem título)"),
        criarElemento(
            "p",
            "turma-ano",
            `Abertura: ${formatarData(obterDataDeAbertura(atividade))} · Prazo: ${formatarData(obterDataDoPrazo(atividade))}`
        )
    );

    // Etiqueta: amarela quando o aluno precisa agir, cinza nos outros casos
    const dadosDoCartao = criarElemento("p", "turma-dados");
    dadosDoCartao.append(
        criarElemento("span", "turma-pendentes" + (descricao.destaque ? "" : " zerado"), descricao.etiqueta)
    );
    cartao.append(dadosDoCartao);

    // Botão (quando existir uma ação possível)
    if (descricao.botao) {
        const areaDosBotoes = criarElemento("div", "turma-acoes");
        const botao = criarElemento("a", descricao.botao.classe, descricao.botao.texto);

        botao.href = descricao.botao.endereco;

        areaDosBotoes.append(botao);
        cartao.append(areaDosBotoes);
    }

    coluna.append(cartao);
    return coluna;
}


// ------------------------------------------------------------
// MONTAR AS DUAS LINHAS
// ------------------------------------------------------------

// Garante um subtítulo logo acima da linha (cria se ainda não existir)
function garantirSubtitulo(linha, texto) {
    const anterior = linha.previousElementSibling;

    if (anterior && anterior.classList.contains("area-subtitulo")) {
        anterior.textContent = texto;
        return;
    }

    const subtitulo = criarElemento("h3", "area-subtitulo fs-4 fw-bold mt-3 mb-3 px-md-5", texto);
    linha.before(subtitulo);
}

// Coloca os cartões dentro de uma linha. Sem atividades, mostra uma mensagem.
function preencherLinha(linha, subtitulo, atividades, mensagemVazia, dados) {
    garantirSubtitulo(linha, subtitulo);
    linha.classList.add("gy-4"); // espaço entre os cartões quando quebram de linha

    if (atividades.length === 0) {
        const coluna = criarElemento("div", "col-12");
        coluna.append(criarElemento("p", "text-center mb-0", mensagemVazia));

        linha.replaceChildren(coluna);
        return;
    }

    linha.replaceChildren(...atividades.map((atividade) => criarCartaoDaAtividade(atividade, dados)));
}


// ------------------------------------------------------------
// INÍCIO DA PÁGINA
// ------------------------------------------------------------

(async () => {
    try {
        // Acha as duas linhas onde os cartões serão colocados
        const linhasDaPagina = document.querySelectorAll(".turmas-vidro.mt-4 > .row");
        const linhaParaFazer = pegarPorId("atividadesParaFazer") ?? linhasDaPagina[0];
        const linhaOutras = pegarPorId("atividadesConcluidas") ?? linhasDaPagina[1];

        if (!linhaParaFazer || !linhaOutras) {
            throw Error("A página precisa de duas linhas (row) para receber as atividades.");
        }

        const dados = await carregarDadosDoAluno();

        // Saudação
        const nome = dados.aluno.nome ?? "aluno";
        escreverTexto("nomeAluno", nome);


        // O aluno não vê atividades que ainda não abriram (situação "agendada")
        const atividadesVisiveis = dados.atividades.filter((atividade) => {
            const situacao = calcularSituacao({
                abertura: obterDataDeAbertura(atividade),
                prazo: obterDataDoPrazo(atividade)
            });

            return situacao !== "agendada";
        });

        // Separa em "para fazer" e "outras"
        const paraFazer = atividadesVisiveis.filter(
            (atividade) => descreverAtividade(atividade, dados).destaque
        );
        const outras = atividadesVisiveis.filter(
            (atividade) => !descreverAtividade(atividade, dados).destaque
        );

        // Para fazer: as de prazo mais próximo primeiro
        paraFazer.sort((a, b) =>
            String(obterDataDoPrazo(a) ?? "").localeCompare(String(obterDataDoPrazo(b) ?? ""))
        );

        // Outras: as mais recentes primeiro
        outras.sort((a, b) =>
            String(obterDataDeAbertura(b) ?? "").localeCompare(String(obterDataDeAbertura(a) ?? ""))
        );

        preencherLinha(
            linhaParaFazer,
            "Para fazer",
            paraFazer,
            "Você não tem atividades para fazer agora.",
            dados
        );

        preencherLinha(
            linhaOutras,
            "Enviadas, corrigidas e encerradas",
            outras,
            "Nenhuma atividade por aqui ainda.",
            dados
        );
    } catch (erro) {
        mostrarErro(erro.message);
    }
})();