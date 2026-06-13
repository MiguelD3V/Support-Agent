# Support Agent API 🚀

Uma API REST para um agente de suporte técnico com histórico de conversas baseado em RAG (Retrieval-Augmented Generation).

## 🎯 Recursos

- ✅ **API REST** - Endpoints para interagir com o agente
- 📝 **Histórico de Conversas** - SQLite para armazenar todas as conversas
- 🔍 **RAG** - Busca em base de conhecimento com ChromaDB
- 🤖 **IA Inteligente** - Powered by Google Gemini
- 📊 **Paginação** - Suporte para listar conversas com limite
- 🔄 **CORS** - Habilitado para integração com front-end

## 📋 Requisitos

- Python 3.8+
- Variável de ambiente `GENAI_API_KEY` configurada

## 🔧 Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar a API
python api.py
```

A API estará disponível em `http://localhost:8000`

### Swagger UI (Documentação Interativa)
- Acesse: `http://localhost:8000/docs`

## 📡 Endpoints da API

### 1️⃣ Criar Nova Conversa
```http
POST /chat/new
```

**Resposta:**
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "criada_em": "2024-01-15T10:30:00",
  "message": "Conversa criada com sucesso"
}
```

---

### 2️⃣ Enviar Mensagem
```http
POST /chat/{conversation_id}/message
Content-Type: application/json

{
  "mensagem": "Estou recebendo o erro G999 na UMED"
}
```

**Resposta:**
```json
{
  "resposta": "🎧 **ROTEIRO DE INSTRUÇÃO PARA O CLIENTE**\n\nErro Identificado: G999\n...",
  "usuario_message_id": 1,
  "agent_message_id": 2,
  "timestamp": "2024-01-15T10:30:15"
}
```

---

### 3️⃣ Obter Histórico de Conversa
```http
GET /chat/{conversation_id}
```

**Resposta:**
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "titulo": "Conversa de 15/01/2024 10:30",
  "criada_em": "2024-01-15T10:30:00",
  "ultima_atualizacao": "2024-01-15T10:35:20",
  "messages": [
    {
      "usuario": "user",
      "conteudo": "Estou recebendo o erro G999 na UMED",
      "timestamp": "2024-01-15T10:30:10"
    },
    {
      "usuario": "agent",
      "conteudo": "🎧 **ROTEIRO DE INSTRUÇÃO PARA O CLIENTE**...",
      "timestamp": "2024-01-15T10:30:15"
    }
  ]
}
```

---

### 4️⃣ Listar Todas as Conversas
```http
GET /chat?limit=50&offset=0
```

**Resposta:**
```json
{
  "total": 42,
  "conversas": [
    {
      "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
      "titulo": "Conversa de 15/01/2024 10:30",
      "criada_em": "2024-01-15T10:30:00",
      "ultima_atualizacao": "2024-01-15T10:35:20",
      "total_mensagens": 5
    }
  ]
}
```

---

### 5️⃣ Atualizar Título da Conversa
```http
PUT /chat/{conversation_id}/titulo
Content-Type: application/json

{
  "titulo": "Erro G999 - Problema na UMED"
}
```

**Resposta:**
```json
{
  "message": "Título atualizado com sucesso",
  "novo_titulo": "Erro G999 - Problema na UMED"
}
```

---

### 6️⃣ Deletar Conversa
```http
DELETE /chat/{conversation_id}
```

**Resposta:**
```json
{
  "message": "Conversa deletada com sucesso"
}
```

---

## 💻 Exemplo de Uso com Python

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Criar conversa
resp = requests.post(f"{BASE_URL}/chat/new")
conversation_id = resp.json()["conversation_id"]
print(f"Conversa criada: {conversation_id}")

# 2. Enviar mensagem
payload = {"mensagem": "Erro G999 na UMED"}
resp = requests.post(f"{BASE_URL}/chat/{conversation_id}/message", json=payload)
resposta = resp.json()
print(f"Resposta do agente:\n{resposta['resposta']}")

# 3. Obter histórico
resp = requests.get(f"{BASE_URL}/chat/{conversation_id}")
historico = resp.json()
print(f"Total de mensagens: {len(historico['messages'])}")

# 4. Listar conversas
resp = requests.get(f"{BASE_URL}/chat?limit=10")
conversas = resp.json()
print(f"Total de conversas: {conversas['total']}")
```

---

## 💻 Exemplo com cURL

```bash
# Criar conversa
curl -X POST http://localhost:8000/chat/new

# Enviar mensagem (substituir {id} pelo conversation_id)
curl -X POST http://localhost:8000/chat/{id}/message \
  -H "Content-Type: application/json" \
  -d '{"mensagem": "Qual é o erro G999?"}'

# Obter histórico
curl -X GET http://localhost:8000/chat/{id}

# Listar conversas
curl -X GET "http://localhost:8000/chat?limit=10&offset=0"
```

---

## 🗄️ Estrutura do Banco de Dados

### Tabela: `conversations`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | ID único (primary key) |
| conversation_id | STRING | UUID único da conversa |
| titulo | STRING | Título customizável |
| criada_em | DATETIME | Data de criação |
| ultima_atualizacao | DATETIME | Última atualização |

### Tabela: `messages`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | ID único (primary key) |
| conversation_id | STRING | Foreign key para conversations |
| usuario | STRING | "user" ou "agent" |
| conteudo | TEXT | Conteúdo da mensagem |
| timestamp | DATETIME | Data/hora da mensagem |

---

## 🚀 Deployment

### Usando Gunicorn (Produção)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 api:app
```

### Usando Docker

```dockerfile
FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## ⚙️ Variáveis de Ambiente

Crie um arquivo `.env`:

```env
GENAI_API_KEY=sua_chave_aqui
```

---

## 📝 Notas

- O banco de dados SQLite é criado automaticamente em `db/suport_agent.db`
- As runbooks são carregadas na inicialização da API
- CORS está habilitado para qualquer origem (customize conforme necessário)
- Cada conversa tem um UUID único para rastreabilidade

---

## 🆘 Suporte

Para dúvidas ou problemas, consulte a documentação interativa em `/docs` após iniciar a API.

