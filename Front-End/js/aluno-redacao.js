// ============================================================
// redacao-aluno.js
//
// Página onde o aluno escreve e envia a redação de uma atividade.
// A atividade vem no endereço da página: redacao.html?atividade=ID
//
// O que faz:
//   - mostra o tema, os textos motivadores e o prazo da atividade;
//   - conta os caracteres (limite de 1862) com uma barra de progresso;
//   - guarda um rascunho no navegador (a API ainda não tem rota de rascunho);
//   - envia a redação final para a API (POST /redacoes).
//   - bloqueia a escrita quando a atividade ainda não abriu, já foi
//     enviada ou o prazo acabou.
//
// Depende de: base-aluno.js (carregar antes).
// Elementos da página que usa (os que faltarem são ignorados):
//   tema, textosMotivadores, prazoDaAtividade, editor, contador, barra,
//   palavras, btnSalvar, btnEnviar, status, alerta.
// ============================================================

const LIMITE_DE_CARACTERES = 1862;
const PAGINA_INICIAL_DO_ALUNO = "atividades-aluno.html";

// Número da atividade, lido do endereço da página (?atividade=3)
const idDaAtividade = Number(new URLSearchParams(location.search).get("atividade"));

const editor = pegarPorId("editor");
const botaoEnviar = pegarPorId("btnEnviar");
const botaoSalvar = pegarPorId("btnSalvar");

// A atividade em que o aluno está escrevendo (preenchida ao carregar)
let atividadeAtual = null;


// ------------------------------------------------------------
// CONTADOR DE CARACTERES
// ------------------------------------------------------------

// Atualiza o contador, a barra de progresso e a contagem de palavras
function atualizarContador() {
    const total = editor.value.length;

    escreverTexto("contador", `${total} / ${LIMITE_DE_CARACTERES} caracteres`);

    const texto = editor.value.trim();
    escreverTexto("palavras", texto ? texto.split(/\s+/).length : 0);

    const barra = pegarPorId("barra");

    if (barra) {
        barra.style.width = `${Math.min(100, (total / LIMITE_DE_CARACTERES) * 100)}%`;

        // Cor da barra: normal, amarela a partir de 90% e vermelha no limite
        let estado = "";
        if (total >= LIMITE_DE_CARACTERES) estado = "limite";
        else if (total >= LIMITE_DE_CARACTERES * 0.9) estado = "aviso";

        barra.className = `progress-bar ${estado}`;
    }
}


// ------------------------------------------------------------
// RASCUNHO (guardado só neste navegador)
// ------------------------------------------------------------

// Cada aluno e cada atividade têm o seu próprio rascunho
const chaveDoRascunho = () => `rascunho:${idAluno}:${idDaAtividade}`;

function salvarRascunho() {
    try {
        localStorage.setItem(chaveDoRascunho(), editor.value);
        return true;
    } catch {
        return false;
    }
}

function carregarRascunho() {
    try {
        const rascunho = localStorage.getItem(chaveDoRascunho());
        if (rascunho) editor.value = rascunho.slice(0, LIMITE_DE_CARACTERES);
    } catch {
        // sem acesso ao armazenamento: começa com o editor vazio
    }
}


// ------------------------------------------------------------
// MOSTRAR A ATIVIDADE E BLOQUEAR QUANDO NÃO DÁ PARA ESCREVER
// ------------------------------------------------------------

// Escreve o tema, os textos motivadores e o prazo na página
function mostrarAtividade(atividade) {
    escreverTexto("tema", obterTituloDaAtividade(atividade) ?? "(sem título)");
    escreverTexto("prazoDaAtividade", `Prazo: ${formatarData(obterDataDoPrazo(atividade))}`);

    const areaDosTextos = pegarPorId("textosMotivadores");

    if (areaDosTextos) {
        // A descrição da atividade guarda os textos motivadores do tema
        const textos = lerTextosMotivadores(atividade.descricao);

        areaDosTextos.replaceChildren(
            ...textos.map((texto) => {
                const paragrafo = document.createElement("p");
                paragrafo.textContent = texto;
                return paragrafo;
            })
        );
    }
}

// Impede a escrita e explica o motivo
function bloquearEscrita(motivo) {
    editor.disabled = true;
    if (botaoEnviar) botaoEnviar.disabled = true;
    if (botaoSalvar) botaoSalvar.disabled = true;

    mostrarErro(motivo);
}


// ------------------------------------------------------------
// INÍCIO DA PÁGINA
// ------------------------------------------------------------

(async () => {
    try {
        if (!idDaAtividade) throw Error("Atividade não informada.");

        const dados = await carregarDadosDoAluno();

        atividadeAtual = dados.atividades.find(
            (atividade) => Number(atividade.id_atividade) === idDaAtividade
        );

        if (!atividadeAtual) throw Error("Atividade não encontrada para a sua turma.");

        mostrarAtividade(atividadeAtual);

        const situacao = calcularSituacao({
            abertura: obterDataDeAbertura(atividadeAtual),
            prazo: obterDataDoPrazo(atividadeAtual)
        });

        const redacaoJaEnviada = encontrarRedacaoDaAtividade(dados, idDaAtividade);

        if (redacaoJaEnviada) {
            // Mostra o que o aluno já enviou, sem permitir mudanças
            editor.value = obterTextoDaRedacao(redacaoJaEnviada);
            bloquearEscrita("Você já enviou a redação desta atividade.");
        } else if (situacao === "agendada") {
            bloquearEscrita("Esta atividade ainda não está aberta.");
        } else if (situacao === "encerrada") {
            bloquearEscrita("O prazo desta atividade já terminou.");
        } else {
            carregarRascunho();
        }

        atualizarContador();
    } catch (erro) {
        bloquearEscrita(erro.message);
    }
})();


// ------------------------------------------------------------
// AÇÕES DO ALUNO
// ------------------------------------------------------------

// A cada letra digitada: atualiza o contador e guarda o rascunho
editor.addEventListener("input", () => {
    if (editor.value.length > LIMITE_DE_CARACTERES) {
        editor.value = editor.value.slice(0, LIMITE_DE_CARACTERES);
    }

    atualizarContador();
    salvarRascunho();
});

// Botão "Salvar rascunho": avisa que o rascunho foi guardado
botaoSalvar?.addEventListener("click", () => {
    const hora = new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });

    escreverTexto(
        "status",
        salvarRascunho()
            ? `Rascunho salvo às ${hora}.`
            : "Não foi possível salvar o rascunho neste navegador."
    );
});

// Botão "Enviar": manda a redação final para a API
botaoEnviar?.addEventListener("click", async () => {
    const texto = editor.value.trim();

    if (!texto) {
        mostrarErro("Escreva sua redação antes de enviar.");
        editor.focus();
        return;
    }

    if (!confirm("Depois de enviada, a redação não poderá ser alterada. Enviar agora?")) return;

    botaoEnviar.disabled = true;

    try {
        // O POST /redacoes da API lê estes quatro campos
        await chamarApi("/redacoes", {
            method: "POST",
            body: JSON.stringify({
                tema: obterTituloDaAtividade(atividadeAtual),
                texto: texto,
                id_aluno: idAluno,
                id_atividade: idDaAtividade,
                data_envio: dataDeHoje()
            })
        });

        // Enviada: o rascunho não é mais necessário
        localStorage.removeItem(chaveDoRascunho());
        location.href = PAGINA_INICIAL_DO_ALUNO;
    } catch (erro) {
        mostrarErro(erro.message);
        botaoEnviar.disabled = false;
    }
});