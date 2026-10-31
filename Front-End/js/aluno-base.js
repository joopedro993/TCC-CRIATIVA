// ============================================================
// base-aluno.js
//
// Código compartilhado por todas as páginas da Área do Aluno.
// Precisa ser carregado ANTES dos scripts de cada página
// (atividades-aluno.js, redacao-aluno.js e resultados-aluno.js).
//
// O que este arquivo faz:
//   1. Guarda a configuração e um atalho para achar elementos.
//   2. Descobre quem é o aluno logado (lendo o token).
//   3. Oferece funções para falar com a API.
//   4. Oferece funções pequenas para montar a tela (células, datas...).
//   5. Carrega e filtra os dados que todas as páginas usam.
//
// Rotas do app.py que este arquivo usa:
//   GET /alunos/<id>               dados do aluno (para saber a turma dele)
//   GET /turmas/<id>               nome da turma
//   GET /atividades/turma/<id>     atividades da turma do aluno
//   GET /redacoes                  todas as redações (filtradas aqui)
//   GET /correcao                  todas as correções (filtradas aqui)
// ============================================================


// ------------------------------------------------------------
// 1. CONFIGURAÇÃO E ATALHOS
// ------------------------------------------------------------

// Endereço da API Flask
const apiURL = "http://127.0.0.1:5010";

// Atalho para achar um elemento da página pelo id
const pegarPorId = (id) => document.getElementById(id);

// Escreve um texto em um elemento, se ele existir na página
// (assim, um id que falte no HTML não quebra o resto do script)
function escreverTexto(id, texto) {
    const elemento = pegarPorId(id);
    if (elemento) elemento.textContent = texto;
}


// ------------------------------------------------------------
// 2. SESSÃO: quem é o aluno logado?
// ------------------------------------------------------------

// Lê o token que o login guardou no navegador
const lerToken = () => localStorage.getItem("token");

// Encerra a sessão: apaga o token e volta para a tela de login
function sair() {
    localStorage.removeItem("token");
    location.href = "login-alunos.html";
}

// O botão "Sair" (se existir na página) encerra a sessão
pegarPorId("btnSair")?.addEventListener("click", sair);

// O token tem 3 partes separadas por ponto. A primeira guarda os dados
// do usuário (id e tipo) em base64. Aqui decodificamos essa primeira parte.
// Devolve null se não houver token ou se ele estiver ilegível.
function lerDadosDoToken() {
    try {
        const primeiraParte = lerToken().split(".")[0];
        const base64Comum = primeiraParte.replace(/-/g, "+").replace(/_/g, "/");

        return JSON.parse(atob(base64Comum));
    } catch {
        return null;
    }
}

const dadosDoToken = lerDadosDoToken();

// Só vale como aluno se o tipo do token for "aluno"
const idAluno = dadosDoToken?.tipo === "aluno" ? Number(dadosDoToken.id) : null;

// Sem aluno logado, volta para o login.
// Atenção: isto é só conveniência. Quem protege os dados de verdade é o Flask.
if (!idAluno) sair();


// ------------------------------------------------------------
// 3. COMUNICAÇÃO COM A API
// ------------------------------------------------------------

// Faz uma requisição à API e devolve o JSON da resposta.
//   caminho: parte final do endereço (ex.: "/turmas")
//   opcoes:  as opções do fetch (method, body...)
// Se a API responder com erro, lança um Error com a mensagem do servidor.
async function chamarApi(caminho, opcoes = {}) {
    const cabecalhos = { Authorization: `Bearer ${lerToken()}` };

    // Só avisa que o corpo é JSON quando existe um corpo (POST, PUT...)
    if (opcoes.body) cabecalhos["Content-Type"] = "application/json";

    const resposta = await fetch(apiURL + caminho, { ...opcoes, headers: cabecalhos });

    // 401 = sessão inválida ou expirada
    if (resposta.status === 401) sair();

    if (!resposta.ok) {
        const corpoDoErro = await resposta.json().catch(() => ({}));
        throw Error(corpoDoErro.erro || `Erro ${resposta.status}`);
    }

    // Se a resposta não for JSON, devolve um objeto vazio em vez de quebrar
    return resposta.json().catch(() => ({}));
}

// Igual ao chamarApi, mas garante que o resultado é uma lista
// (se a API devolver outra coisa, devolve uma lista vazia)
async function buscarLista(caminho) {
    const resultado = await chamarApi(caminho);
    return Array.isArray(resultado) ? resultado : [];
}


// ------------------------------------------------------------
// 4. FUNÇÕES PARA MONTAR A TELA
// ------------------------------------------------------------

// Mostra uma mensagem de erro em um aviso da página.
// Sem o segundo parâmetro, usa o aviso geral (id "alerta").
function mostrarErro(mensagem, idDoAviso = "alerta") {
    const aviso = pegarPorId(idDoAviso);

    if (aviso) {
        aviso.textContent = mensagem;
        aviso.classList.remove("d-none");
    }
}

// Cria uma célula (td) com o texto e a adiciona na linha da tabela.
// Texto ausente aparece como "—". Devolve a célula criada.
function adicionarCelula(linha, texto, classe = "") {
    const celula = document.createElement("td");

    celula.textContent = texto ?? "—";
    if (classe) celula.className = classe;

    linha.append(celula);
    return celula;
}

// Converte uma data "2026-10-12" para "12/10/2026"
function formatarData(valor) {
    if (!valor) return "—";

    // Usa só os 10 primeiros caracteres, caso a data venha com hora
    const [ano, mes, dia] = String(valor).slice(0, 10).split("-");

    return dia && mes && ano ? `${dia}/${mes}/${ano}` : "—";
}

// Data de hoje no formato "2026-10-12" (no horário local do computador)
function dataDeHoje() {
    return new Date().toLocaleDateString("sv-SE");
}

// Diz em que momento está uma atividade, comparando as datas com hoje:
//   "agendada"  = ainda não abriu
//   "aberta"    = está no prazo
//   "encerrada" = o prazo acabou
// Recebe um objeto no formato { abertura, prazo }.
function calcularSituacao(periodo) {
    // Sem as duas datas não dá para comparar: considera aberta
    if (!periodo.abertura || !periodo.prazo) return "aberta";

    const hoje = dataDeHoje();
    const abertura = String(periodo.abertura).slice(0, 10);
    const prazo = String(periodo.prazo).slice(0, 10);

    if (hoje < abertura) return "agendada";
    if (hoje > prazo) return "encerrada";
    return "aberta";
}


// ------------------------------------------------------------
// 5. LEITORES DE CAMPOS
// A API pode devolver a mesma informação com nomes de coluna diferentes
// (ex.: id_turma_fk, id_turma ou turma). Estas funções tentam cada nome,
// na ordem, e usam o primeiro que existir. Se algum nome for outro no seu
// banco, é só acrescentá-lo aqui, em um único lugar.
// ------------------------------------------------------------

// Id da turma a que o aluno pertence
function obterIdDaTurmaDoAluno(aluno) {
    return Number(aluno?.id_turma_fk ?? aluno?.id_turma ?? aluno?.turma);
}

// Título de uma atividade (pode estar em "titulo" ou em "tema")
function obterTituloDaAtividade(atividade) {
    return atividade?.titulo ?? atividade?.tema;
}

// Data em que a atividade abre para os alunos
function obterDataDeAbertura(atividade) {
    return atividade?.data_disponibilizacao ?? atividade?.data_abertura;
}

// Data limite da atividade
function obterDataDoPrazo(atividade) {
    return atividade?.prazo ?? atividade?.data_prazo;
}

// Id do aluno que escreveu a redação
function obterIdDoAlunoDaRedacao(redacao) {
    return Number(redacao?.id_aluno_fk ?? redacao?.id_aluno ?? redacao?.aluno);
}

// Id da atividade a que a redação pertence
function obterIdDaAtividadeDaRedacao(redacao) {
    return Number(redacao?.id_atividade_fk ?? redacao?.id_atividade ?? redacao?.atividade);
}

// Texto escrito na redação
function obterTextoDaRedacao(redacao) {
    return redacao?.texto ?? redacao?.conteudo ?? "";
}

// Data em que a redação foi enviada
function obterDataDeEnvio(redacao) {
    return redacao?.data_envio ?? redacao?.data;
}

// Id da redação a que a correção se refere
function obterIdDaRedacaoDaCorrecao(correcao) {
    return Number(correcao?.id_redacao_fk ?? correcao?.id_redacao);
}

// Nota total de uma correção: vem pronta (nota_total) ou, se não vier,
// é a soma das cinco competências
function obterNotaTotalDaCorrecao(correcao) {
    const somaDasCompetencias = [1, 2, 3, 4, 5].reduce(
        (soma, numero) => soma + (Number(correcao?.[`competencia_${numero}`]) || 0),
        0
    );

    return Number(correcao?.nota_total ?? somaDasCompetencias);
}

// Os textos motivadores de um tema são guardados como um objeto estruturado ou JSON.
// Esta função devolve uma lista de objetos contendo o título e o conteúdo de cada texto.
function lerTextosMotivadores(valor) {
    if (!valor) return [];

    let lido = valor;
    if (typeof valor === "string") {
        try {
            lido = JSON.parse(valor);
        } catch {
            return [{ titulo: "", conteudo: String(valor) }];
        }
    }

    const arrayDeTextos = 
        lido?.textos_motivadores?.textos || 
        lido?.textos || 
        (Array.isArray(lido) ? lido : null);

    if (Array.isArray(arrayDeTextos)) {
        return arrayDeTextos.map((item) => {
            if (typeof item === "object" && item !== null) {
                return {
                    titulo: item.titulo ?? "",
                    conteudo: item.conteudo ?? item.texto ?? ""
                };
            }
            return { titulo: "", conteudo: String(item) };
        });
    }

    return [{ titulo: "", conteudo: String(lido) }];
}


// ------------------------------------------------------------
// 6. CARREGAR OS DADOS DO ALUNO
// ------------------------------------------------------------

// Busca na API tudo o que as páginas precisam e já separa só o que
// pertence a este aluno. Devolve um objeto com:
//   aluno               -> dados do aluno (nome, e-mail, turma...)
//   turma               -> dados da turma (ou null se não foi possível buscar)
//   atividades          -> atividades da turma do aluno
//   redacoes            -> redações escritas por este aluno
//   correcaoPorRedacao  -> Map: id da redação -> { competencias, notaTotal,
//                          comentario, dataCorrecao } (só as já corrigidas)
async function carregarDadosDoAluno() {
    // Primeiro: os dados do aluno, porque o token só traz o id e precisamos
    // saber a turma dele para pedir as atividades certas
    const aluno = await chamarApi(`/alunos/${idAluno}`);
    const idDaTurma = obterIdDaTurmaDoAluno(aluno);

    if (!idDaTurma) {
        throw Error("Não foi possível descobrir a turma deste aluno.");
    }

    // Depois: o resto, em consultas simultâneas (mais rápido)
    const [atividadesDaTurma, todasAsRedacoes, todasAsCorrecoes, turma] = await Promise.all([
        buscarLista(`/atividades/turma/${idDaTurma}`),
        buscarLista("/redacoes"),
        buscarLista("/correcao"),
        chamarApi(`/turmas/${idDaTurma}`).catch(() => null) // o nome da turma é só um extra
    ]);

    // A API devolve redações de todos os alunos; ficamos só com as deste aluno
    const minhasRedacoes = todasAsRedacoes.filter(
        (redacao) => obterIdDoAlunoDaRedacao(redacao) === idAluno
    );
    const idsDasMinhasRedacoes = new Set(minhasRedacoes.map((redacao) => Number(redacao.id_redacao)));

    // Correções das minhas redações. Uma redação que aparece neste mapa já foi corrigida.
    const correcaoPorRedacao = new Map();

    todasAsCorrecoes.forEach((correcao) => {
        const idDaRedacao = obterIdDaRedacaoDaCorrecao(correcao);

        if (!idsDasMinhasRedacoes.has(idDaRedacao)) return;

        correcaoPorRedacao.set(idDaRedacao, {
            competencias: [1, 2, 3, 4, 5].map((numero) => Number(correcao[`competencia_${numero}`]) || 0),
            notaTotal: obterNotaTotalDaCorrecao(correcao),
            comentario: correcao.comentario ?? correcao.feedback ?? "",
            dataCorrecao: correcao.data_correcao
        });
    });

    return {
        aluno,
        turma,
        atividades: atividadesDaTurma,
        redacoes: minhasRedacoes,
        correcaoPorRedacao
    };
}

// Procura a redação que o aluno escreveu para uma atividade
// (devolve undefined se ele ainda não escreveu)
function encontrarRedacaoDaAtividade(dados, idDaAtividade) {
    return dados.redacoes.find(
        (redacao) => obterIdDaAtividadeDaRedacao(redacao) === Number(idDaAtividade)
    );
}

// Diz em que ponto está a redação de uma atividade:
//   "nao_enviada" = o aluno ainda não escreveu
//   "enviada"     = escreveu e está esperando o professor corrigir
//   "corrigida"   = o professor já corrigiu
function descobrirEstadoDaRedacao(redacao, dados) {
    if (!redacao) return "nao_enviada";

    return dados.correcaoPorRedacao.has(Number(redacao.id_redacao)) ? "corrigida" : "enviada";
}