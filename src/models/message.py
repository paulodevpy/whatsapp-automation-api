"""
Modelo de Mensagem com Template
"""
from dataclasses import dataclass
from typing import Optional, Dict, List
from pathlib import Path
from datetime import datetime


@dataclass
class MessageTemplate:
    """
    Template de mensagem com suporte a variaveis curinga
    
    Variaveis disponiveis:
        {nome_completo}  - Nome completo do contato
        {primeiro_nome}  - Primeiro nome
        {ultimo_nome}    - Ultimo nome
        {telefone}       - Telefone do contato
    """
    
    text: str
    image_path: Optional[str] = None
    
    # Mapeamento de variaveis curinga
    WILDCARDS: Dict[str, str] = None
    
    def __post_init__(self):
        """Inicializa wildcards"""
        self.WILDCARDS = {
            "{nome_completo}": "full_name",
            "{primeiro_nome}": "first_name",
            "{ultimo_nome}": "last_name",
            "{telefone}": "phone",
            "{email}": "email",
            "{cidade}": "city",
            "{estado}": "state",
            "{empresa}": "company",
        }
    
    def render(self, contact) -> str:
        """
        Renderiza template substituindo variaveis
        pelos dados do contato
        """
        rendered = self.text
        
        # Mapeamento de nomes de coluna para atributos
        attr_map = {
            'nome_completo': 'full_name',
            'primeiro_nome': 'first_name',
            'ultimo_nome': 'last_name',
            'telefone': 'phone',
            'email': 'email',
            'cidade': 'city',
            'estado': 'state',
            'empresa': 'company',
        }
        
        # Substitui variaveis do contato
        import re
        placeholders = re.findall(r'\{([^}]+)\}', rendered)
        for placeholder in placeholders:
            if placeholder in ['data_atual', 'hora_atual', 'saudacao']:
                continue  # Tratados separadamente
            attr = attr_map.get(placeholder, placeholder)
            if hasattr(contact, attr):
                value = getattr(contact, attr, "")
            else:
                value = contact.extra_data.get(attr, "")
            rendered = rendered.replace(f"{{{placeholder}}}", str(value))
        
        # Substitui variaveis de data e hora
        if "{data_atual}" in rendered:
            rendered = rendered.replace("{data_atual}", datetime.now().strftime("%d/%m/%Y"))
        if "{hora_atual}" in rendered:
            rendered = rendered.replace("{hora_atual}", datetime.now().strftime("%H:%M"))
        if "{saudacao}" in rendered:
            hour = datetime.now().hour
            if hour < 12:
                saudacao = "Bom dia"
            elif hour < 18:
                saudacao = "Boa tarde"
            else:
                saudacao = "Boa noite"
            rendered = rendered.replace("{saudacao}", saudacao)
        
        return rendered
    
    def has_image(self) -> bool:
        """Verifica se tem imagem configurada"""
        return bool(self.image_path) and Path(self.image_path).exists()
    
    def get_used_wildcards(self) -> List[str]:
        """Retorna lista de wildcards usados no texto"""
        return [wc for wc in self.WILDCARDS.keys() if wc in self.text]
    
    @classmethod
    def get_available_wildcards(cls) -> List[Dict[str, str]]:
        """Retorna lista de wildcards disponiveis"""
        return [
            {"variavel": "{primeiro_nome}", "descricao": "Primeiro nome do contato"},
            {"variavel": "{nome_completo}", "descricao": "Nome completo do contato"},
            {"variavel": "{ultimo_nome}", "descricao": "Ultimo nome do contato"},
            {"variavel": "{telefone}", "descricao": "Numero de telefone"},
        ]