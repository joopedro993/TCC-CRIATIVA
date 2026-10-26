// ============================================================
// aluno-correcao.js
//
// Script da página aluno-consulta-correcao.html.
// Precisa ser carregado DEPOIS do aluno-base.js.
//
// A página é aberta com o id da redação no endereço:
//   aluno-consulta-correcao.html?redacao=7
//
// O que este arquivo faz:
//   1. Mostra a redação que o aluno escreveu (tema, texto, datas...).
//   2. Mostra a correção do professor: nota de cada competência,
//      nota final e comentário.
//   3. Avisa se a redação ainda não foi corrigida.
//
// Esta página é só de consulta: o aluno não altera nada aqui.
// ============================================================


// ------------------------------------------------------------
// 1. DADOS DA PÁGINA
// ------------------------------------------------------------

// Id da redação, lido do endereço (?redacao=7)
const idDaRedacao = Number(new URLSearchParams(location.search).get("redacao"));


// ------------------------------------------------------------
// 2. MOSTRAR A REDAÇÃO
// ------------------------------------------------------------

// Mostra o texto do aluno (um <p> por parágrafo) e as estatísticas
function mostrarTexto(texto) {
    const paragrafos = String(texto ?? "").split(/\n+/).filter((p) => p.trim());
    const textoCompleto = paragrafos.join(" ");

    const areaDoTexto = pegarPorId("textoAluno");
    areaDoTexto.innerHTML = "";

    paragrafos.forEach((paragrafo) => {
        const elemento = document.createElement("p");
        elemento.textContent = paragrafo;
        areaDoTexto.append(elemento);
    });

    escreverTexto("paragrafos", paragrafos.length);
    escreverTexto("palavras", textoCompleto ? textoCompleto.split(/\s+/).length : 0);
    escreverTexto("caracteres", textoCompleto.length);
}


// ------------------------------------------------------------
// 3. MOSTRAR A CORREÇÃO
// ------------------------------------------------------------

// Mostra as 5 notas, a nota final e o comentário do professor.
// Recebe um objeto no formato { competencias, notaTotal, comentario, dataCorrecao }
// (o mesmo que o aluno-base.js monta em correcaoPorRedacao).
function mostrarCorrecao(correcao) {
    correcao.competencias.forEach((nota, indice) => {
        escreverTexto(`nota${indice + 1}`, nota);
    });

    escreverTexto("notaTotal", correcao.notaTotal);
    escreverTexto("dataCorrecao", formatarData(correcao.dataCorrecao));
    escreverTexto("comentario", correcao.comentario || "O professor não deixou comentário.");
}


// ------------------------------------------------------------
// 4. INICIAR A PÁGINA
// ------------------------------------------------------------

async function iniciar() {
    try {
        const dados = await carregarDadosDoAluno();

        // Só acha redações escritas por este aluno e atividades da turma dele
        const redacao = dados.redacoes.find(
            (item) => Number(item.id_redacao) === idDaRedacao
        );
        const atividade = dados.atividades.find(
            (item) => Number(item.id_atividade) === obterIdDaAtividadeDaRedacao(redacao)
        );

        if (!atividade || !redacao) {
            mostrarErro("Redação não encontrada.");
            return;
        }

        escreverTexto("tema", obterTituloDaAtividade(atividade) ?? "—");
        escreverTexto("dataEnvio", formatarData(obterDataDeEnvio(redacao)));
        mostrarTexto(obterTextoDaRedacao(redacao));

        // Se a redação ainda não tem correção, avisa e para por aqui
        const correcao = dados.correcaoPorRedacao.get(idDaRedacao);

        if (!correcao) {
            mostrarErro("Esta redação ainda não foi corrigida pelo professor.");
            return;
        }

        mostrarCorrecao(correcao);
    } catch (erro) {
        mostrarErro(erro.message);
    }
}

iniciar();