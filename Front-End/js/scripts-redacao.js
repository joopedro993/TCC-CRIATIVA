const LIMITE = 1862;
const CHAVE_RASCUNHO = 'criativa:rascunho';

const editor = document.getElementById('editor');
const contador = document.getElementById('contador');
const barra = document.getElementById('barra');
const progressoWrap = document.getElementById('progressoWrap');
const palavras = document.getElementById('palavras');
const paragrafos = document.getElementById('paragrafos');
const status = document.getElementById('status');

function atualizar() {
    // Garante o limite mesmo se o texto for colado
    if (editor.value.length > LIMITE) {
        editor.value = editor.value.slice(0, LIMITE);
    }

    const total = editor.value.length;
    const pct = Math.min(100, (total / LIMITE) * 100);

    contador.textContent = total + ' / ' + LIMITE + ' caracteres';
    barra.style.width = pct + '%';
    progressoWrap.setAttribute('aria-valuenow', total);

    // Cores: roxo normal, amarelo a partir de 90%, vermelho no limite
    const estado = total >= LIMITE ? 'limite' : (total >= LIMITE * 0.9 ? 'aviso' : '');
    contador.className = 'redacao-contador ' + estado;
    barra.className = 'progress-bar ' + estado;

    const texto = editor.value.trim();
    palavras.textContent = texto ? texto.split(/\s+/).length : 0;
    paragrafos.textContent = texto ? texto.split(/\n+/).filter((p) => p.trim()).length : 0;
}

function mostrarStatus(msg) {
    status.textContent = msg;
}

// Rascunho salvo no navegador
function salvar() {
    try {
        localStorage.setItem(CHAVE_RASCUNHO, editor.value);
        mostrarStatus('Rascunho salvo às ' + new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }) + '.');
    } catch (e) {
        mostrarStatus('Não foi possível salvar o rascunho neste navegador.');
    }
}

try {
    const guardado = localStorage.getItem(CHAVE_RASCUNHO);
    if (guardado) editor.value = guardado.slice(0, LIMITE);
} catch (e) { /* sem acesso ao armazenamento */ }

editor.addEventListener('input', atualizar);
document.getElementById('btnSalvar').addEventListener('click', salvar);

document.getElementById('btnEnviar').addEventListener('click', () => {
    if (editor.value.trim().length === 0) {
        mostrarStatus('Escreva sua redação antes de enviar.');
        editor.focus();
        return;
    }
    // TODO: enviar ao back-end, por exemplo:
    // fetch('/api/redacoes', { method: 'POST', headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ tema: document.getElementById('tema').textContent, texto: editor.value }) });
    mostrarStatus('Redação pronta para envio ao professor (conecte ao back-end).');
});

document.getElementById('btnSugestao').addEventListener('click', () => {
    const caixa = document.getElementById('sugestao');
    // TODO: substituir pela chamada real à IA, enviando tema + texto atual.
    caixa.textContent = 'Aqui aparecerá a sugestão da IA, como uma pergunta ou dica para você ' +
        'aprofundar seu argumento, sem reescrever o seu texto.';
    caixa.classList.remove('d-none');
});

atualizar();