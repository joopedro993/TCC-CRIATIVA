import express from 'express';
import cors from 'cors';
import { GoogleGenAI } from '@google/genai';
import 'dotenv/config';

const app = express();

app.use(cors());
app.use(express.json());

// ==============================
// CONFIGURAÇÃO DA IA
// ==============================

const ai = new GoogleGenAI({
    apiKey: process.env.GEMINI_API_KEY
});

// ==============================
// ROTA DE CORREÇÃO DA REDAÇÃO
// ==============================

app.post('/api/corrigir', async (req, res) => {

    const { redacao, tema } = req.body;

    // Verifica se existe redação
    if (!redacao || redacao.trim() === '') {
        return res.status(400).json({
            error: 'A redação não pode estar vazia.'
        });
    }

    try {

        const response = await ai.models.generateContent({

            model: 'gemini-3.5-flash-lite',

            config: {

                responseMimeType: 'application/json',

                systemInstruction: `
Você é o corretor de redações da plataforma CRIATIVA.

Sua função é analisar redações no modelo dissertativo-argumentativo
utilizado no ENEM.

A redação deve ser avaliada de acordo com as cinco competências
oficiais do ENEM.

Cada competência deve receber uma nota entre 0 e 200 pontos.

A soma das cinco competências deve resultar na nota final,
variando de 0 a 1000 pontos.

COMPETÊNCIA 1:
Avalie o domínio da modalidade escrita formal da língua portuguesa.
Analise ortografia, acentuação, pontuação, concordância,
regência, colocação pronominal e construção das frases.

COMPETÊNCIA 2:
Avalie a compreensão do tema, o desenvolvimento do assunto,
a estrutura dissertativo-argumentativa e o repertório sociocultural.

COMPETÊNCIA 3:
Avalie a seleção, organização e interpretação das informações,
fatos, opiniões e argumentos utilizados para defender a tese.

COMPETÊNCIA 4:
Avalie a utilização dos mecanismos de coesão e dos conectivos,
observando a relação entre as partes do texto.

COMPETÊNCIA 5:
Avalie a proposta de intervenção.
Observe agente, ação, meio/modo, efeito e detalhamento,
respeitando os direitos humanos.

REGRAS IMPORTANTES:

- Analise a redação inteira antes de atribuir as notas.
- Não invente erros.
- Utilize exemplos reais retirados da redação.
- Explique claramente cada avaliação.
- Apresente pontos positivos.
- Apresente pontos que podem ser melhorados.
- Dê sugestões práticas.
- A nota final deve ser exatamente a soma das cinco competências.
- Retorne SOMENTE JSON válido.

Use exatamente esta estrutura:

{
    "nota_final": 0,

    "competencias": {

        "c1": {
            "nome": "Competência 1 — Domínio da modalidade escrita formal",
            "nota": 0,
            "avaliacao": "",
            "pontos_positivos": [],
            "pontos_melhorar": []
        },

        "c2": {
            "nome": "Competência 2 — Compreensão do tema",
            "nota": 0,
            "avaliacao": "",
            "pontos_positivos": [],
            "pontos_melhorar": []
        },

        "c3": {
            "nome": "Competência 3 — Seleção e organização dos argumentos",
            "nota": 0,
            "avaliacao": "",
            "pontos_positivos": [],
            "pontos_melhorar": []
        },

        "c4": {
            "nome": "Competência 4 — Coesão",
            "nota": 0,
            "avaliacao": "",
            "pontos_positivos": [],
            "pontos_melhorar": []
        },

        "c5": {
            "nome": "Competência 5 — Proposta de intervenção",
            "nota": 0,
            "avaliacao": "",
            "pontos_positivos": [],
            "pontos_melhorar": []
        }
    },

    "comentarios_gerais": [],

    "correcoes": [
        {
            "trecho_errado": "",
            "motivo": "",
            "sugestao": ""
        }
    ]
}
`
            },

            contents: `
Tema da redação:
${tema || 'Tema não informado'}

Redação do aluno:
${redacao}
`
        });

        // ==============================
        // RECEBE RESPOSTA DA GEMINI
        // ==============================

        const textoResposta = response.text.trim();

        console.log('\n==============================');
        console.log('RESPOSTA DA GEMINI');
        console.log('==============================');
        console.log(textoResposta);
        console.log('==============================\n');

        // Converte resposta para JSON
        const resultadoJson = JSON.parse(textoResposta);

        // Envia para o Front-End
        res.json(resultadoJson);

    } catch (error) {

        console.error('\n================================');
        console.error('ERRO AO CORRIGIR REDAÇÃO');
        console.error('================================');
        console.error(error);
        console.error('================================\n');

        res.status(500).json({
            error: 'Erro interno ao processar a correção da redação.'
        });
    }
});

// ==============================
// SERVIDOR
// =============================

const PORT = 3001;

app.listen(PORT, () => {

    console.log('======================================');
    console.log('🚀 CRIATIVA');
    console.log(`🚀 Servidor rodando na porta ${PORT}`);
    console.log(`🚀 http://localhost:${PORT}`);
    console.log('======================================');

});
