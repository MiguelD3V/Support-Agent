from datetime import datetime
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.message_models import (
    ConversationDB,
    MessageDB, 
)
from src.schemas.message_schema import MessageRequestSchema

def criar_conversa(db: Session):
    conversation_id = str(uuid.uuid4())
    
    nova_conversa = ConversationDB(
        conversation_id=conversation_id,
        titulo=f"Conversa de {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )
    
    db.add(nova_conversa)
    db.commit()
    db.refresh(nova_conversa)

    return nova_conversa

def envia_conversa(conversation_id: str,
    request: MessageRequestSchema,
    db: Session,
    agent):
    
        # Validar conversa
    conversa = db.query(ConversationDB).filter(
        ConversationDB.conversation_id == conversation_id
    ).first()
    
    if not conversa:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    # Validar mensagem
    if not request.mensagem.strip():
        raise HTTPException(status_code=400, detail="Mensagem não pode estar vazia")
    
    # Salvar mensagem do usuário
    msg_usuario = MessageDB(
        conversation_id=conversation_id,
        usuario="user",
        conteudo=request.mensagem
    )
    db.add(msg_usuario)
    db.commit()
    db.refresh(msg_usuario)
    
    # Obter resposta do agente
    resposta = agent.send_message(request.mensagem)
    
    # Salvar resposta do agente
    msg_agente = MessageDB(
        conversation_id=conversation_id,
        usuario="agent",
        conteudo=resposta
    )
    db.add(msg_agente)
    
    # Atualizar conversa
    conversa.ultima_atualizacao = datetime.now()
    db.commit()
    db.refresh(msg_agente)
    
    return {
        "resposta": resposta,
        "msg_usuario_id": msg_usuario.id,
        "msg_agente_id": msg_agente.id,
        "timestamp": msg_agente.timestamp
    }