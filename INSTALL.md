# 🚀 Guia de Instalação - Support Agent API

## ✅ Pré-requisitos

- Python 3.8 ou superior
- pip (gestor de pacotes Python)
- Chave API do Google Gemini

## 📋 Passo a Passo

### 1️⃣ Clonar/Baixar o Projeto

```bash
cd c:\Users\maste\OneDrive\Desktop\Suport_Agent
```

### 2️⃣ Criar Ambiente Virtual (Recomendado)

```bash
# No Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# No Windows (CMD)
python -m venv venv
venv\Scripts\activate.bat

# No Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar Variáveis de Ambiente

#### Opção A: Arquivo .env (Recomendado)

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e adicione sua chave API
# No Windows:
copy .env.example .env
```

Edite o arquivo `.env`:
```env
GENAI_API_KEY=sua_chave_aqui
```

#### Opção B: Variável de Ambiente do Sistema

Windows (PowerShell):
```powershell
$env:GENAI_API_KEY = "sua_chave_aqui"
```

Windows (CMD):
```cmd
set GENAI_API_KEY=sua_chave_aqui
```

Mac/Linux:
```bash
export GENAI_API_KEY="sua_chave_aqui"
```

### 5️⃣ Preparar Base de Conhecimento

1. Adicione seus PDFs ou arquivos TXT em: `data/runbooks/`
2. Exemplo de arquivo: `data/runbooks/Erros.txt` (já está incluído)

### 6️⃣ Iniciar a API

```bash
python api.py
```

Você verá algo como:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
✅ Banco de dados inicializado
✅ Runbooks carregados
INFO:     Application startup complete [Uvicorn]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 7️⃣ Acessar a API

- **API Base:** http://localhost:8000
- **Swagger UI (Documentação Interativa):** http://localhost:8000/docs

### 8️⃣ Testar a API

```bash
# Terminal 1 - Manter a API rodando
python api.py

# Terminal 2 - Executar teste
python client_example.py
```

---

## 🆘 Troubleshooting

### Erro: "GENAI_API_KEY não encontrado"

**Solução:** Certifique-se de que:
1. O arquivo `.env` existe na raiz do projeto
2. A variável `GENAI_API_KEY` está preenchida corretamente
3. Não há espaços extras ao redor da chave

### Erro: "ModuleNotFoundError"

**Solução:** Instale as dependências:
```bash
pip install -r requirements.txt
```

### Erro: "Porta 8000 já está em uso"

**Solução:** Use outra porta:
```bash
python -m uvicorn api:app --host 0.0.0.0 --port 8001
```

### ChromaDB/Vector DB não carregando

**Solução:** Delete a pasta `vector_db/` e deixe ela ser recriada:
```bash
rm -r vector_db/  # Mac/Linux
rmdir /s vector_db  # Windows
python api.py  # Recria e indexa
```

### Banco de dados SQLite corrompido

**Solução:** Delete a pasta `db/`:
```bash
rm -r db/  # Mac/Linux
rmdir /s db  # Windows
python api.py  # Recria as tabelas
```

---

## 🔄 Próximos Passos

1. **Testar a API** com `python client_example.py`
2. **Adicionar runbooks** em `data/runbooks/`
3. **Integrar frontend** usando a documentação Swagger
4. **Deploy** seguindo as instruções em README.md

---

## 📚 Recursos Adicionais

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://www.sqlalchemy.org/)
- [Google Gemini API](https://ai.google.dev/)
- [ChromaDB Docs](https://docs.trychroma.com/)

