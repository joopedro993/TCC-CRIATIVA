// ============================================================
// professor-correcao.js
//
// Script da página professor-correcao.html.
// Precisa ser carregado DEPOIS do professor-base.js.
//
// A página é aberta com o id da redação no endereço:
//   professor-correcao.html?id=7
//
// O que este arquivo faz:
//   1. Mostra a redação do aluno (tema, texto, nome, turma...).
//   2. Soma as notas das 5 competências enquanto o professor avalia.
//   3. Salva a correção na API (POST se for nova, PUT se já existir).
// ============================================================


// ------------------------------------------------------------
// 1. DADOS DA PÁGINA
// ------------------------------------------------------------

// Id da redação, lido do endereço (?id=7)
const idDaRedacao = Number(new URLSearchParams(location.search).get("id"));

// As 5 listas de nota (uma por competência)
const camposDeNota = document.querySelectorAll(".nota-comp");

// Notas possíveis em cada competência
const NOTAS_POSSIVEIS = [0, 40, 80, 120, 160, 200];

// Se a redação já foi corrigida, guarda a correção aqui
let correcaoExistente = null;

// Id que a API exige ao criar uma correção nova (maior id atual + 1)
let proximoIdDaCorrecao = 1;


// ------------------------------------------------------------
// 2. LEITORES DE CAMPOS (mesma ideia do professor-base.js)
// ------------------------------------------------------------

// Id da redação a que uma correção pertence
function obterIdDaRedacaoDaCorrecao(correcao) {
    return Number(correcao?.id_redacao_fk ?? correcao?.id_redacao);
}


// ------------------------------------------------------------
// 3. NOTAS
// ------------------------------------------------------------

// Preenche cada lista com as notas 0, 40, 80, 120, 160 e 200
function montarListasDeNota() {
    camposDeNota.forEach((campo) => {
        campo.innerHTML =
            '<option value="">Selecione a nota</option>' +
            NOTAS_POSSIVEIS.map((nota) => `<option value="${nota}">${nota}</option>`).join("");

        campo.addEventListener("change", atualizarNotaTotal);
    });
}

// Soma as competências já escolhidas e mostra o total na tela
function atualizarNotaTotal() {
    let notaTotal = 0;
    let preenchidas = 0;

    camposDeNota.forEach((campo) => {
        if (campo.value !== "") {
            notaTotal += Number(campo.value);
            preenchidas++;
        }
    });

    pegarPorId("notaTotal").textContent = notaTotal;
    pegarPorId("competenciasPreenchidas").textContent = `${preenchidas}/5`;
}

// ------------------------------------------------------------
// RASCUNHO (guardado só neste navegador)
// ------------------------------------------------------------

// Cada aluno e cada atividade têm o seu próprio rascunho
// ------------------------------------------------------------
// 4.1 RASCUNHO (fica guardado só neste navegador)
// Guarda as 5 notas e o comentário. Cada professor tem um rascunho
// por redação, por isso a chave leva os dois ids.
// ------------------------------------------------------------

const chaveDoRascunho = () => `rascunho:${idProfessor}:${idDaRedacao}`;

pegarPorId("btnSalvar")?.addEventListener("click", () => {
    pegarPorId("status").textContent = salvarRascunho()
        ? "Rascunho salvo neste navegador."
        : "Não foi possível salvar o rascunho.";
});

// Guarda no navegador o que está nos campos agora.
// Devolve true se deu certo e false se o navegador não permitiu.
function salvarRascunho() {
    const rascunho = {
        notas: [...camposDeNota].map((campo) => campo.value),
        comentario: pegarPorId("feedback").value
    };

    try {
        localStorage.setItem(chaveDoRascunho(), JSON.stringify(rascunho));
        return true;
    } catch {
        return false;
    }
}

// Coloca nos campos o rascunho guardado, se existir.
// Devolve true se encontrou um rascunho.
function carregarRascunho() {
    try {
        const textoGuardado = localStorage.getItem(chaveDoRascunho());
        if (!textoGuardado) return false;

        const rascunho = JSON.parse(textoGuardado);

        camposDeNota.forEach((campo, indice) => {
            campo.value = rascunho.notas?.[indice] ?? "";
        });

        pegarPorId("feedback").value = rascunho.comentario ?? "";
        atualizarNotaTotal();
        return true;
    } catch {
        // sem acesso ao armazenamento: começa com os campos vazios
        return false;
    }
}

// Apaga o rascunho (usado depois que a correção é salva de verdade)
function apagarRascunho() {
    try {
        localStorage.removeItem(chaveDoRascunho());
    } catch {
        // sem acesso ao armazenamento: não há o que apagar
    }
}


// ------------------------------------------------------------
// 4. MOSTRAR A REDAÇÃO E A CORREÇÃO
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

    pegarPorId("paragrafos").textContent = paragrafos.length;
    pegarPorId("palavras").textContent = textoCompleto ? textoCompleto.split(/\s+/).length : 0;
    pegarPorId("caracteres").textContent = textoCompleto.length;
}

// Troca a etiqueta de situação no topo da página
function mostrarSituacao(corrigida) {
    const etiqueta = pegarPorId("situacao");

    etiqueta.textContent = corrigida ? "Corrigida" : "Aguardando correção";
    etiqueta.className = corrigida ? "situacao encerrada" : "situacao agendada";
}

// Coloca nos campos a correção que já foi feita antes
function preencherCorrecao(correcao) {
    camposDeNota.forEach((campo, indice) => {
        campo.value = correcao[`competencia_${indice + 1}`];
    });

    pegarPorId("feedback").value = correcao.comentario ?? "";
    atualizarNotaTotal();
}


// ------------------------------------------------------------
// 5. SALVAR A CORREÇÃO
// ------------------------------------------------------------

const botaoDevolver = pegarPorId("btnDevolver");


async function salvarCorrecao() {
    const notas = [...camposDeNota].map((campo) => campo.value);
    const comentario = pegarPorId("feedback").value.trim();

    // Marca em vermelho as competências que faltam
    camposDeNota.forEach((campo) => campo.classList.toggle("is-invalid", campo.value === ""));

    if (notas.includes("")) {
        mostrarErro("Avalie as 5 competências antes de salvar.", "status");
        return;
    }

    if (!comentario) {
        mostrarErro("Escreva um comentário para o aluno.", "status");
        return;
    }

    // Monta o corpo exatamente como a rota /correcao espera
    const dadosDaCorrecao = {
        id_redacao: idDaRedacao,
        id_professor: idProfessor,
        competencia_1: Number(notas[0]),
        competencia_2: Number(notas[1]),
        competencia_3: Number(notas[2]),
        competencia_4: Number(notas[3]),
        competencia_5: Number(notas[4]),
        comentario,
        data_correcao: dataDeHoje()
    };

    botaoDevolver.disabled = true;
    try {
        if (correcaoExistente) {
            await chamarApi(`/correcao/${dadosDaCorrecao.id_correcao}`, {
                method: "PUT",
                body: JSON.stringify(dadosDaCorrecao)
            });
        } else {
            await chamarApi("/correcao", {
                method: "POST",
                body: JSON.stringify(dadosDaCorrecao)
            });
        }

        // Daqui em diante, salvar de novo atualiza esta mesma correção
        correcaoExistente = dadosDaCorrecao;
        mostrarSituacao(true);
        apagarRascunho()
        window.alert("Correção salva e devolvida ao aluno.");
        location.href = "area-professor.html";

    } catch (erro) {
        mostrarErro(erro.message, "status");
        botaoDevolver.disabled = false;
    }
}


// ------------------------------------------------------------
// 6. INICIAR A PÁGINA
// ------------------------------------------------------------

async function iniciar() {
    montarListasDeNota();

    try {
        const dados = await carregarDadosDoProfessor();

        // Procura só entre as redações deste professor
        const redacao = dados.redacoes.find((item) => Number(item.id_redacao) === idDaRedacao);

        if (!redacao) {
            mostrarErro("Redação não encontrada.", "status");
            return;
        }

        const aluno = dados.alunos.find(
            (item) => Number(item.id_aluno) === obterIdDoAlunoDaRedacao(redacao)
        );
        const turma = dados.turmas.find(
            (item) => Number(item.id_turma) === obterIdDaTurmaDoAluno(aluno)
        );

        pegarPorId("alunoNome").textContent = aluno?.nome ?? "—";
        pegarPorId("alunoTurma").textContent = turma?.nome ?? "—";
        pegarPorId("dataEnvio").textContent = formatarData(obterDataDeEnvio(redacao));
        pegarPorId("tema").textContent = dados.obterTituloDoTema(redacao.tema);
        mostrarTexto(redacao.texto);

        // Descobre se já existe correção e qual será o próximo id
        const todasAsCorrecoes = await buscarLista("/correcao");

        correcaoExistente =
            todasAsCorrecoes.find(
                (correcao) => obterIdDaRedacaoDaCorrecao(correcao) === idDaRedacao
            ) ?? null;

        if (correcaoExistente) preencherCorrecao(correcaoExistente);
        else if (carregarRascunho()) pegarPorId("status").textContent = "Rascunho recuperado.";

        if (correcaoExistente) {
            botaoDevolver.disabled = true;
            pegarPorId("status").textContent = "Esta redação já foi corrigida.";
        }

        mostrarSituacao(Boolean(correcaoExistente));
    } catch (erro) {
        mostrarErro(erro.message, "status");
    }
}

pegarPorId("btnDevolver")?.addEventListener("click", salvarCorrecao);

iniciar();