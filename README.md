# 🤖 AI Support Agent - RAG com Google Gemini

Um assistente de suporte técnico baseado em Inteligência Artificial que combina **RAG (Retrieval-Augmented Generation)**, **ChromaDB** e **Google Gemini** para auxiliar equipes de atendimento na resolução de incidentes e registro de chamados.

O sistema consulta uma base de conhecimento privada composta por manuais, procedimentos e runbooks da empresa, fornecendo respostas contextualizadas e gerando automaticamente instruções para atendimento e protocolos de registro.

---

## 🚀 Visão Geral

Este projeto foi desenvolvido para atuar como um **copiloto de suporte técnico**, permitindo que operadores consultem rapidamente procedimentos internos sem precisar pesquisar manualmente em documentos extensos.

A solução utiliza:

* **RAG (Retrieval-Augmented Generation)** para recuperar informações relevantes da base de conhecimento.
* **ChromaDB** como banco de dados vetorial para armazenamento dos embeddings.
* **Google Gemini 3.1 Flash lite** como modelo de linguagem principal.
* **Function Calling** para permitir que a IA utilize ferramentas de busca automaticamente.

---

## ✨ Funcionalidades

### 📚 Base de Conhecimento Inteligente

* Indexação automática de arquivos `.txt` e `.pdf`
* Busca semântica utilizando embeddings vetoriais
* Consulta contextual baseada na pergunta do usuário

### 🔄 Atualização Incremental

* Detecção automática de alterações nos documentos
* Atualização apenas dos arquivos modificados
* Evita duplicação de conteúdo no banco vetorial

### 🧠 Function Calling

* O modelo decide quando consultar a base de conhecimento
* Busca automática de informações relevantes
* Respostas mais precisas e contextualizadas

---

## 🏗️ Arquitetura

```text
Usuário
   │
   ▼
Google Gemini
   │
Function Calling
   │
   ▼
Ferramentas do Agente
   │
   ▼
Motor RAG
   │
   ▼
ChromaDB
   │
   ▼
Runbooks (.txt/.pdf)
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia              | Finalidade                             |
| ----------------------- | -------------------------------------- |
| Python 3.x              | Linguagem principal                    |
| Google Gemini 1.5 Flash | Modelo de IA                           |
| ChromaDB                | Banco vetorial                         |
| PyPDF2                  | Leitura de PDFs                        |
| python-dotenv           | Gerenciamento de variáveis de ambiente |

---

## 📂 Estrutura do Projeto

```text
📁 ai-support-agent
│
├── 📁 data
│   └── 📁 runbooks
│       ├── erros.txt
│       └── instrucoes.pdf
│
├── 📁 src
│   ├── agent.py
│   ├── rag_engine.py
│   └── tools.py
│
├── 📁 vector_db
│
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/MiguelD3V/Support-Agent.git

cd ai-support-agent
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
GENAI_API_KEY=sua_chave_api
```

Obtenha sua chave através do Google AI Studio.

⚠️ Nunca envie o arquivo `.env` para o GitHub.

---

## 📚 Adicionando Conhecimento

Coloque seus documentos na pasta:

```text
data/runbooks/
```

Formatos suportados:

* TXT
* PDF

Exemplo:

```text
Erro 001: Realize o procedimento de desligar todos os aparelhos e ligar novamente.
```

Ao iniciar a aplicação, os documentos serão indexados automaticamente.

---

## ▶️ Executando o Projeto

```bash
python main.py
```

Exemplo de pergunta:

```text
O cliente está reportando o erro 001.
```

Resposta esperada:

```text
🎧 **ROTEIRO DE INSTRUÇÃO PARA O CLIENTE**
**Erro Identificado:**
**Resolução Técnica:** 
=======================================


...
```

```text
📋 **PROTOCOLO PARA REGISTRO NO SISTEMA**
**ANALISE/TESTE:**
**CONCLUSÃO:** 
...
```

---

## 💡 Possíveis Evoluções

* Interface Web com FastAPI
* Integração com WhatsApp
* Integração com sistemas de chamados
* Histórico de conversas
* Dashboard de métricas
* Suporte a DOCX e XLSX
* Agentes especializados por área

---

## 🎯 Objetivo do Projeto

Este projeto foi criado para estudo e demonstração de conceitos avançados de IA aplicada:

* Retrieval-Augmented Generation (RAG)
* Engenharia de Prompt
* Function Calling
* Bancos Vetoriais
* Agentes de IA
* Automação de Suporte Técnico


