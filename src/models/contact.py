"""
Modelo de Contato
"""
from dataclasses import dataclass, field
from typing import Optional, Dict
from enum import Enum
from datetime import datetime


class ContactStatus(Enum):
    """Status do envio para o contato"""
    PENDING = "Pendente"
    SENT = "Enviado"
    FAILED = "Falhou"
    SKIPPED = "Sem WhatsApp"
    INVALID_PHONE = "Tel. Invalido"


@dataclass
class Contact:
    """Representa um contato da planilha"""
    
    full_name: str
    phone: str
    email: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    company: Optional[str] = None
    extra_data: Dict[str, str] = field(default_factory=dict)
    status: ContactStatus = field(default=ContactStatus.PENDING)
    error_message: Optional[str] = None
    sent_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Normaliza dados apos inicializacao"""
        self.full_name = str(self.full_name).strip()
        self.phone = self._normalize_phone(str(self.phone))
    
    def _normalize_phone(self, phone: str) -> str:
        """Normaliza numero de telefone para formato internacional"""
        # Remove tudo que nao e numero
        digits = ''.join(filter(str.isdigit, phone))
        
        # Remove zero inicial
        if digits.startswith('0'):
            digits = digits[1:]
        
        # Adiciona codigo do Brasil se necessario
        if len(digits) in [10, 11]:
            digits = '55' + digits
            
        return digits
    
    @property
    def first_name(self) -> str:
        """Retorna primeiro nome"""
        parts = self.full_name.split()
        return parts[0] if parts else ""
    
    @property
    def last_name(self) -> str:
        """Retorna ultimo nome"""
        parts = self.full_name.split()
        return parts[-1] if len(parts) > 1 else ""
    
    def mark_as_sent(self):
        """Marca contato como enviado"""
        self.status = ContactStatus.SENT
        self.sent_at = datetime.now()
    
    def mark_as_failed(self, error: str):
        """Marca contato como falho"""
        self.status = ContactStatus.FAILED
        self.error_message = error
    
    def mark_as_skipped(self):
        """Marca contato como pulado (sem WhatsApp)"""
        self.status = ContactStatus.SKIPPED
        self.error_message = "Numero sem WhatsApp"
    
    def mark_as_invalid(self, reason: str):
        """Marca telefone como invalido"""
        self.status = ContactStatus.INVALID_PHONE
        self.error_message = reason
    
    def to_dict(self) -> dict:
        """Converte para dicionario"""
        return {
            "nome": self.full_name,
            "telefone": self.phone,
            "status": self.status.value,
            "erro": self.error_message,
            "enviado_em": self.sent_at.isoformat() if self.sent_at else None
        }