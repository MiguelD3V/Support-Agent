from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class MessageSchema(BaseModel):
    usuario: str
    conteudo: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class ConversationSchema(BaseModel):
    conversation_id: str
    titulo: Optional[str] = None
    criada_em: datetime
    ultima_atualizacao: datetime
    messages: List[MessageSchema] = []
    
    class Config:
        from_attributes = True


class MessageRequestSchema(BaseModel):
    mensagem: str


class ConversationListSchema(BaseModel):
    conversation_id: str
    titulo: Optional[str] = None
    criada_em: datetime
    ultima_atualizacao: datetime
    total_mensagens: int = 0
    
    class Config:
        from_attributes = True
