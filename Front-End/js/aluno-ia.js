// ============================================================
// aluno-ia.js
//
// Modal "Consulte a IA" da página de redação do aluno.
// O aluno escreve uma pergunta (ou clica em uma sugestão) e a resposta
// aparece em formato de conversa dentro do modal.
//
// Depende de: aluno-base.js e aluno-redacao.js (carregar nessa ordem,
// antes deste arquivo). Daqui usamos o que o aluno-redacao.js já criou:
//   editor          -> o texto que o aluno está escrevendo
//   atividadeAtual  -> a atividade (tema e textos motivadores)
//
// Elementos da página que usa:
//   modalIA, conversaIA, avisoIA, formularioIA, perguntaIA,
//   btnEnviarIA, btnLimparIA e os botões com a classe "ia-sugestao".
//
// ATENÇÃO: por enquanto a API ainda não tem rota de IA. A resposta vem
// de pedirRespostaDaIA(), que devolve um texto de teste. Quando a rota
// existir, só essa função precisa ser trocada.
// ============================================================

const MENSAGEM_DE_BOAS_VINDAS =
    "Olá! Posso ajudar você a pensar na sua redação: tese, argumentos, repertório " +
    "e proposta de intervenção. Eu não escrevo o texto por você. Qual é a sua dúvida?";

const modalIA = pegarPorId("modalIA");
const conversaIA = pegarPorId("conversaIA");
const formularioIA = pegarPorId("formularioIA");
const campoPerguntaIA = pegarPorId("perguntaIA");
const botaoEnviarIA = pegarPorId("btnEnviarIA");

// Mensagens da conversa, no formato { autor: "aluno" | "ia", texto }
const historicoIA = [];

// Enquanto espera a resposta, não deixa enviar outra pergunta
let aguardandoIA = false;


// ------------------------------------------------------------
// 1. CONVERSA NA TELA
// ------------------------------------------------------------

// Acrescenta uma mensagem no fim da conversa e devolve o elemento criado.
//   autor: "aluno" ou "ia"
function adicionarMensagem(autor, texto, classeExtra = "") {
    const mensagem = document.createElement("div");

    mensagem.className = `ia-mensagem ${autor === "aluno" ? "ia-aluno" : "ia-resposta"} ${classeExtra}`.trim();
    mensagem.textContent = texto;

    conversaIA.append(mensagem);
    conversaIA.scrollTop = conversaIA.scrollHeight;

    return mensagem;
}

// Apaga a conversa e volta para a mensagem de boas-vindas
function iniciarConversa() {
    conversaIA.replaceChildren();
    historicoIA.length = 0;

    esconderAvisoIA();
    adicionarMensagem("ia", MENSAGEM_DE_BOAS_VINDAS);
}

function esconderAvisoIA() {
    pegarPorId("avisoIA")?.classList.add("d-none");
}

// Bloqueia (ou libera) o envio enquanto a IA responde
function definirAguardando(estado) {
    aguardandoIA = estado;
    botaoEnviarIA.disabled = estado;
    campoPerguntaIA.disabled = estado;
}


// ------------------------------------------------------------
// 2. PEDIDO À IA
// ------------------------------------------------------------

// Reúne o que a IA precisa saber para responder bem:
// a pergunta, o tema, os textos motivadores, o rascunho e a conversa até aqui
function montarPedidoParaIA(pergunta) {
    return {
        pergunta,
        tema: obterTituloDaAtividade(atividadeAtual),
        textos_motivadores: lerTextosMotivadores(atividadeAtual?.descricao),
        rascunho: editor.value,
        historico: [...historicoIA]
    };
}

// Devolve a resposta da IA (um texto) para o pedido montado acima.
// TROCAR quando a rota existir, por exemplo:
//
//   const resposta = await chamarApi("/ia/sugestao", {
//       method: "POST",
//       body: JSON.stringify(pedido)
//   });
//   return resposta.resposta;
//
async function pedirRespostaDaIA(pedido) {
    // Simula o tempo de resposta da IA
    await new Promise((resolver) => setTimeout(resolver, 800));

    return `(Resposta de teste) Você perguntou: "${pedido.pergunta}". ` +
        "Quando a API estiver ligada, a resposta da IA aparecerá aqui.";
}


// ------------------------------------------------------------
// 3. ENVIAR UMA PERGUNTA
// ------------------------------------------------------------

async function perguntarIA(textoDaPergunta) {
    const pergunta = textoDaPergunta.trim();

    if (aguardandoIA || !pergunta) return;

    // A atividade é carregada pelo aluno-redacao.js; sem ela não há tema para a IA
    if (!atividadeAtual) {
        mostrarErro("Aguarde a atividade carregar para consultar a IA.", "avisoIA");
        return;
    }

    esconderAvisoIA();

    // O pedido é montado antes de a pergunta entrar no histórico
    const pedido = montarPedidoParaIA(pergunta);

    adicionarMensagem("aluno", pergunta);
    historicoIA.push({ autor: "aluno", texto: pergunta });
    campoPerguntaIA.value = "";

    definirAguardando(true);
    const mensagemDaIA = adicionarMensagem("ia", "Pensando...", "ia-pensando");

    try {
        const resposta = await pedirRespostaDaIA(pedido);

        mensagemDaIA.textContent = resposta;
        mensagemDaIA.classList.remove("ia-pensando");
        historicoIA.push({ autor: "ia", texto: resposta });
    } catch (erro) {
        // Falhou: tira o "Pensando...", devolve a pergunta ao campo e avisa
        mensagemDaIA.remove();
        historicoIA.pop();
        campoPerguntaIA.value = pergunta;

        mostrarErro(erro.message || "Não foi possível consultar a IA agora.", "avisoIA");
    } finally {
        definirAguardando(false);
        campoPerguntaIA.focus();
        conversaIA.scrollTop = conversaIA.scrollHeight;
    }
}


// ------------------------------------------------------------
// 4. AÇÕES DO ALUNO
// ------------------------------------------------------------

// Botão "Enviar" (ou Enter dentro do formulário)
formularioIA.addEventListener("submit", (evento) => {
    evento.preventDefault();
    perguntarIA(campoPerguntaIA.value);
});

// Enter envia; Shift + Enter pula de linha
campoPerguntaIA.addEventListener("keydown", (evento) => {
    if (evento.key === "Enter" && !evento.shiftKey && !evento.isComposing) {
        evento.preventDefault();
        formularioIA.requestSubmit();
    }
});

// Botões com perguntas prontas (o texto fica no atributo data-pergunta)
document.querySelectorAll(".ia-sugestao").forEach((botao) => {
    botao.addEventListener("click", () => perguntarIA(botao.dataset.pergunta));
});

// Botão "Limpar conversa"
pegarPorId("btnLimparIA")?.addEventListener("click", iniciarConversa);

// Ao abrir o modal, o cursor já vai para o campo da pergunta
modalIA.addEventListener("shown.bs.modal", () => campoPerguntaIA.focus());

iniciarConversa();