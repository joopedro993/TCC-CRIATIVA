import express from 'express';
import cors from 'cors';
import { GoogleGenAI } from '@google/genai';
import 'dotenv/config';

const app = express();

app.use(cors());
app.use(express.json());

const ai = new GoogleGenAI({
  apiKey: process.env.GEMINI_API_KEY
});

app.post('/api/corrigir', async (req, res) => {
  const { redacao, tema } = req.body;

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
Você é um corretor especializado em redações do ENEM.

Analise a redação seguindo os critérios oficiais das cinco competências
da redação do ENEM.

Cada competência deve receber uma nota entre 0 e 200 pontos.

A soma das cinco competências deve resultar na nota final,
que deve variar entre 0 e 1000 pontos.

Analise a redação inteira antes de atribuir as notas.

COMPETÊNCIA 1:
Avalie o domínio da modalidade escrita formal da língua portuguesa.
Observe ortografia, acentuação, pontuação, concordância, regência,
colocação pronominal e construção das frases.

COMPETÊNCIA 2:
Avalie se o participante compreendeu corretamente o tema,
se desenvolveu o assunto proposto e se utilizou adequadamente
a estrutura dissertativo-argumentativa.
Avalie também a utilização de repertório sociocultural pertinente.

COMPETÊNCIA 3:
Avalie a seleção, organização e interpretação das informações,
fatos, opiniões e argumentos utilizados para defender o ponto de vista.
Verifique a existência de uma tese clara e argumentos relacionados a ela.

COMPETÊNCIA 4:
Avalie os mecanismos linguísticos utilizados para construir
a argumentação, especialmente os elementos de coesão,
conectivos e relações entre as partes do texto.

COMPETÊNCIA 5:
Avalie a proposta de intervenção para o problema abordado.
Observe ação, agente, modo/meio, efeito e detalhamento.
Verifique também o respeito aos direitos humanos.

IMPORTANTE:
Não invente erros que não existem.
Explique cada nota de maneira clara.
Se encontrar problemas, apresente exemplos retirados da própria redação.
Dê sugestões práticas para melhorar o texto.

RETORNE SOMENTE JSON, seguindo exatamente esta estrutura:

{
  "nota_final": 0,

  "competencias": {
    "c1": {
      "nome": "Competência 1 — Domínio da modalidade escrita formal",
      "nota": 0,
      "avaliacao": "texto",
      "pontos_positivos": ["texto"],
      "pontos_melhorar": ["texto"]
    },

    "c2": {
      "nome": "Competência 2 — Compreensão do tema",
      "nota": 0,
      "avaliacao": "texto",
      "pontos_positivos": ["texto"],
      "pontos_melhorar": ["texto"]
    },

    "c3": {
      "nome": "Competência 3 — Seleção e organização dos argumentos",
      "nota": 0,
      "avaliacao": "texto",
      "pontos_positivos": ["texto"],
      "pontos_melhorar": ["texto"]
    },

    "c4": {
      "nome": "Competência 4 — Coesão",
      "nota": 0,
      "avaliacao": "texto",
      "pontos_positivos": ["texto"],
      "pontos_melhorar": ["texto"]
    },

    "c5": {
      "nome": "Competência 5 — Proposta de intervenção",
      "nota": 0,
      "avaliacao": "texto",
      "pontos_positivos": ["texto"],
      "pontos_melhorar": ["texto"]
    }
  },

  "comentarios_gerais": [
    "texto"
  ],

  "correcoes": [
    {
      "trecho_errado": "trecho da redação",
      "motivo": "explicação do problema",
      "sugestao": "forma sugerida de melhorar"
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


    const textoResposta = response.text.trim();

    console.log("RESPOSTA DA GEMINI:");
    console.log(textoResposta);

    const resultadoJson = JSON.parse(textoResposta);

    res.json(resultadoJson);

  } catch (error) {

    console.error('--- ERRO DETALHADO NO SEU TERMINAL ---');
    console.error(error);
    console.error('--------------------------------------');

    res.status(500).json({
      error: 'Erro interno ao processar a correção.'
    });
  }
});

const PORT = 3001;

app.listen(PORT, () => {
  console.log(
    `🚀 O SEU Servidor de Redação está rodando com sucesso na porta ${PORT}!`
  );
});
