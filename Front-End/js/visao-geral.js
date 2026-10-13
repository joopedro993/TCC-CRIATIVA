// ============================================================
// visao-geral.js
//
// Página inicial da Área do Professor. Mostra:
//   - a saudação com o nome do professor;
//   - os quatro números do topo (turmas, alunos, atividades e
//     redações para corrigir).
//
// Depende de: base-professor.js (carregar antes).
// Elementos da página que usa: statTurmas, statAlunos, statAtividades,
//   statPendentes, nomeProfessor, alerta.
// ============================================================

(async () => {
    try {
        const dados = await carregarDadosDoProfessor();

        // Redações ainda sem correção: as que NÃO aparecem no mapa de notas
        const redacoesPendentes = dados.redacoes.filter(
            (redacao) => !dados.notaPorRedacao.has(Number(redacao.id_redacao))
        );

        // Os quatro números do topo
        pegarPorId("statTurmas").textContent = dados.turmas.length;
        pegarPorId("statAlunos").textContent = dados.alunos.length;
        pegarPorId("statAtividades").textContent = dados.atividades.length;
        pegarPorId("statPendentes").textContent = redacoesPendentes.length;

        await mostrarNomeDoProfessor();
    } catch (erro) {
        mostrarErro(erro.message);
    }
})();

// Preenche a saudação com o nome do professor.
// Usa o nome já guardado no navegador; se não houver, busca na API e guarda
// para as próximas vezes. Se a busca falhar, a saudação padrão continua.
async function mostrarNomeDoProfessor() {
    const nomeSalvo = localStorage.getItem("nome");

    if (nomeSalvo) {
        pegarPorId("nomeProfessor").textContent = nomeSalvo;
        return;
    }

    // O catch devolve um objeto vazio para não interromper a página em caso de erro
    const professor = await chamarApi(`/professores/${idProfessor}`).catch(() => ({}));

    if (professor.nome) {
        pegarPorId("nomeProfessor").textContent = professor.nome;
        localStorage.setItem("nome", professor.nome);
    }
}