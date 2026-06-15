from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from src.agent import Agent
from src.db.database import get_db, init_db
from src.models.message_models import (
    ConversationDB, 
    MessageDB, 
)
from src.schemas.message_schema import (
    ConversationSchema,
    MessageRequestSchema,
    ConversationListSchema
)

from src.services.message_service import criar_conversa as criar_conversa_service
from src.services.message_service import envia_conversa as envia_conversa_service

from src.tools import rag_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    rag_engine.load_runbooks()
    print("✅ Banco de dados inicializado")
    print("✅ Runbooks carregados")
    yield
    print("🛑 Aplicação encerrada")

app = FastAPI(
    title="Support Agent API",
    description="API para atendimento técnico com histórico de conversas",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_agent_cache = {}

def get_agent():
    """Obter ou criar instância do agente"""
    if "agent" not in _agent_cache:
        try:
            _agent_cache["agent"] = Agent()
        except ValueError as e:
            raise HTTPException(status_code=500, detail=f"Erro ao inicializar agente: {str(e)}")
    return _agent_cache["agent"]

@app.get("/")
def root():
    """Health check"""
    return {
        "status": "online",
        "message": "Support Agent API está rodando",
        "version": "1.0.0"
    }


@app.post("/chat/new")
def criar_conversa(db: Session = Depends(get_db)):
    """
    Criar uma nova conversa
    
    Retorna:
    - conversation_id: ID único da conversa
    - criada_em: Data de criação
    """
    nova_conversa = criar_conversa_service(db)
    
    return {
        "conversation_id": nova_conversa.conversation_id,
        "criada_em": nova_conversa.criada_em,
        "message": "Conversa criada com sucesso"
    }


@app.post("/chat/{conversation_id}/message")
def enviar_mensagem(
    conversation_id: str,
    request: MessageRequestSchema,
    db: Session = Depends(get_db)
):
    """
    Enviar mensagem para o agente
    
    Parâmetros:
    - conversation_id: ID da conversa
    - mensagem: Texto da mensagem do usuário
    
    Retorna:
    - resposta: Resposta do agente
    - usuario_message_id: ID da mensagem do usuário
    - agent_message_id: ID da resposta do agente
    """
    
    agent = get_agent()
    result = envia_conversa_service(conversation_id, request, db, agent)
    
    return {
        "resposta": result["resposta"],
        "usuario_message_id": result["msg_usuario_id"],
        "agent_message_id": result["msg_agente_id"],
        "timestamp": result["timestamp"]
    }


@app.get("/chat/{conversation_id}")
def obter_historico(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """
    Obter histórico completo de uma conversa
    
    Parâmetros:
    - conversation_id: ID da conversa
    
    Retorna:
    - Histórico completo com todas as mensagens
    """
    
    conversa = db.query(ConversationDB).filter(
        ConversationDB.conversation_id == conversation_id
    ).first()
    
    if not conversa:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    return ConversationSchema.from_orm(conversa)


@app.get("/chat")
def listar_conversas(
    db: Session = Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    """
    Listar todas as conversas
    
    Parâmetros:
    - limit: Número máximo de resultados
    - offset: Deslocamento para paginação
    
    Retorna:
    - Lista de conversas com resumo
    """
    
    conversas = db.query(ConversationDB).order_by(
        ConversationDB.ultima_atualizacao.desc()
    ).offset(offset).limit(limit).all()
    
    resultado = []
    for conversa in conversas:
        resultado.append({
            "conversation_id": conversa.conversation_id,
            "titulo": conversa.titulo,
            "criada_em": conversa.criada_em,
            "ultima_atualizacao": conversa.ultima_atualizacao,
            "total_mensagens": len(conversa.messages)
        })
    
    return {
        "total": db.query(ConversationDB).count(),
        "conversas": resultado
    }


@app.delete("/chat/{conversation_id}")
def deletar_conversa(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """
    Deletar uma conversa e seu histórico
    
    Parâmetros:
    - conversation_id: ID da conversa
    """
    
    conversa = db.query(ConversationDB).filter(
        ConversationDB.conversation_id == conversation_id
    ).first()
    
    if not conversa:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    db.delete(conversa)
    db.commit()
    
    return {"message": "Conversa deletada com sucesso"}


@app.put("/chat/{conversation_id}/titulo")
def atualizar_titulo(
    conversation_id: str,
    request: dict,
    db: Session = Depends(get_db)
):
    """
    Atualizar o título de uma conversa
    
    Parâmetros:
    - conversation_id: ID da conversa
    - titulo: Novo título
    """
    
    if "titulo" not in request:
        raise HTTPException(status_code=400, detail="Campo 'titulo' é obrigatório")
    
    conversa = db.query(ConversationDB).filter(
        ConversationDB.conversation_id == conversation_id
    ).first()
    
    if not conversa:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    conversa.titulo = request["titulo"]
    db.commit()
    
    return {"message": "Título atualizado com sucesso", "novo_titulo": conversa.titulo}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
