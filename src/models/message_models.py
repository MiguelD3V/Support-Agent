from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel
from src.db.database import Base
from typing import Optional, List

class ConversationDB(Base):
    
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, unique=True, index=True)
    titulo = Column(String, nullable=True)
    criada_em = Column(DateTime, default=func.now())
    ultima_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    
    messages = relationship("MessageDB", back_populates="conversation", cascade="all, delete-orphan")


class MessageDB(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, ForeignKey("conversations.conversation_id"))
    usuario = Column(String)  # "user" ou "agent"
    conteudo = Column(Text)
    timestamp = Column(DateTime, default=func.now())
    
    conversation = relationship("ConversationDB", back_populates="messages")

