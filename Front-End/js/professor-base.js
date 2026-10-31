// ============================================================
// base-professor.js
//
// Código compartilhado por todas as páginas da Área do Professor.
// Precisa ser carregado ANTES dos scripts de cada página
// (visao-geral.js, turmas.js, atividades.js e pendentes.js).
//
// O que este arquivo faz:
//   1. Guarda a configuração e um atalho para achar elementos.
//   2. Descobre quem é o professor logado (lendo o token).
//   3. Oferece funções para falar com a API.
//   4. Oferece funções pequenas para montar a tela (células, datas...).
//   5. Carrega e filtra os dados que todas as páginas usam.
// ============================================================


// ------------------------------------------------------------
// 1. CONFIGURAÇÃO E ATALHOS
// ------------------------------------------------------------

// Endereço da API Flask
const apiURL = "http://127.0.0.1:5010";

// Atalho para achar um elemento da página pelo id
// (é o mesmo que document.getElementById)
const pegarPorId = (id) => document.getElementById(id);


// ------------------------------------------------------------
// 2. SESSÃO: quem é o professor logado?
// ------------------------------------------------------------

// Lê o token que o login guardou no navegador
const lerToken = () => localStorage.getItem("token");

// Encerra a sessão: apaga o token e volta para a tela de login
function sair() {
    localStorage.removeItem("token");
    location.href = "login-professor.html";
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

// Só vale como professor se o tipo do token for "professor"
const idProfessor = dadosDoToken?.tipo === "professor" ? dadosDoToken.id : null;

// Sem professor logado, volta para o login.
// Atenção: isto é só conveniência. Quem protege os dados de verdade é o Flask.
if (!idProfessor) sair();


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
// Texto vazio ou ausente aparece como "—". Devolve a célula criada.
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

// Id da turma a que um aluno pertence
function obterIdDaTurmaDoAluno(aluno) {
    return Number(aluno?.id_turma_fk ?? aluno?.id_turma ?? aluno?.turma);
}

// Id da turma para a qual uma atividade foi criada
function obterIdDaTurmaDaAtividade(atividade) {
    return Number(atividade?.id_turma_fk ?? atividade?.id_turma ?? atividade?.turma);
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

// Data em que a redação foi enviada
function obterDataDeEnvio(redacao) {
    return redacao?.data_envio ?? redacao?.data;
}


// ------------------------------------------------------------
// 6. CARREGAR OS DADOS DO PROFESSOR
// ------------------------------------------------------------

// Busca na API tudo o que as páginas precisam e já separa só o que
// pertence a este professor. Devolve um objeto com:
//   turmas             -> as turmas do professor
//   alunos             -> alunos dessas turmas
//   atividades         -> atividades dessas turmas
//   redacoes           -> redações dessas atividades
//   notaPorRedacao     -> Map: id da redação -> nota total (só as já corrigidas)
//   temas              -> lista de temas
//   obterTituloDoTema  -> função: recebe o id de um tema e devolve o título
async function carregarDadosDoProfessor() {
    // Seis consultas ao mesmo tempo (mais rápido do que uma depois da outra)
    const [
        minhasTurmas,
        todosOsAlunos,
        todasAsAtividades,
        todasAsRedacoes,
        todasAsCorrecoes,
        todosOsTemas
    ] = await Promise.all([
        buscarLista(`/turmas/professores/${idProfessor}`),
        buscarLista("/alunos"),
        buscarLista("/atividades"),
        buscarLista("/redacoes"),
        buscarLista("/correcao"),
        buscarLista("/temas")
    ]);

    // Ids das turmas deste professor, usados como filtro nas listas abaixo
    const idsDasMinhasTurmas = new Set(minhasTurmas.map((turma) => Number(turma.id_turma)));

    // A API devolve alunos e atividades de todos os professores;
    // aqui ficamos só com os das turmas deste professor
    const alunosDasMinhasTurmas = todosOsAlunos.filter((aluno) =>
        idsDasMinhasTurmas.has(obterIdDaTurmaDoAluno(aluno))
    );

    const atividadesDasMinhasTurmas = todasAsAtividades.filter((atividade) =>
        idsDasMinhasTurmas.has(obterIdDaTurmaDaAtividade(atividade))
    );

    // Redações que pertencem às atividades deste professor.
    // (Redações de rascunho não são separadas aqui: toda redação ligada
    // a uma atividade do professor entra na lista.)
    const redacoesDasMinhasAtividades = todasAsRedacoes.filter((redacao) => {
        const idDaAtividade = obterIdDaAtividadeDaRedacao(redacao);

        return atividadesDasMinhasTurmas.some(
            (atividade) => Number(atividade.id_atividade) === idDaAtividade
        );
    });

    // Mapa "id da redação -> nota total". Uma redação que aparece neste mapa
    // já foi corrigida. A nota total vem pronta (nota_total) ou, se não vier,
    // é a soma das cinco competências.
    const notaPorRedacao = new Map(
        todasAsCorrecoes.map((correcao) => {
            const idDaRedacao = Number(correcao.id_redacao_fk ?? correcao.id_redacao);

            const somaDasCompetencias = [1, 2, 3, 4, 5].reduce(
                (soma, numero) => soma + (Number(correcao[`competencia_${numero}`]) || 0),
                0
            );

            const notaTotal = Number(correcao.nota_total ?? somaDasCompetencias);

            return [idDaRedacao, notaTotal];
        })
    );

    // Recebe o id de um tema e devolve o título dele.
    // Se não achar o tema, devolve o próprio valor recebido.
    const obterTituloDoTema = (idDoTema) => {
        const tema = todosOsTemas.find((item) => String(item.id_tema) === String(idDoTema));

        return tema?.titulo ?? tema?.nome ?? idDoTema ?? "(sem tema)";
    };

    return {
        turmas: minhasTurmas,
        alunos: alunosDasMinhasTurmas,
        atividades: atividadesDasMinhasTurmas,
        redacoes: redacoesDasMinhasAtividades,
        notaPorRedacao,
        temas: todosOsTemas,
        obterTituloDoTema
    };
}