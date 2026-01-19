"""
Servico de validacao de telefones
"""
import re
from typing import Tuple, Set


class PhoneService:
    """Servico para validacao de numeros de telefone brasileiros"""
    
    # Padrao para telefone brasileiro
    _PATTERN = re.compile(r'^55[1-9][1-9]\d{8,9}$')
    
    # DDDs validos do Brasil
    _VALID_DDDS: Set[int] = {
        11, 12, 13, 14, 15, 16, 17, 18, 19,  # SP
        21, 22, 24,                           # RJ
        27, 28,                               # ES
        31, 32, 33, 34, 35, 37, 38,          # MG
        41, 42, 43, 44, 45, 46,              # PR
        47, 48, 49,                           # SC
        51, 53, 54, 55,                       # RS
        61,                                   # DF
        62, 64,                               # GO
        63,                                   # TO
        65, 66,                               # MT
        67,                                   # MS
        68,                                   # AC
        69,                                   # RO
        71, 73, 74, 75, 77,                  # BA
        79,                                   # SE
        81, 82, 83, 84, 85, 86, 87, 88, 89,  # Nordeste
        91, 92, 93, 94, 95, 96, 97, 98, 99,  # Norte
    }
    
    @classmethod
    def validate(cls, phone: str) -> Tuple[bool, str]:
        """
        Valida numero de telefone
        
        Returns:
            Tuple[e_valido, mensagem_erro]
        """
        if not phone:
            return False, "Telefone vazio"
        
        # Verifica padrao geral
        if not cls._PATTERN.match(phone):
            return False, f"Formato invalido: {phone}"
        
        # Valida DDD
        ddd = int(phone[2:4])
        if ddd not in cls._VALID_DDDS:
            return False, f"DDD invalido: {ddd}"
        
        # Verifica se celular comeca com 9
        number_part = phone[4:]
        if len(number_part) == 9 and not number_part.startswith('9'):
            return False, "Celular deve comecar com 9"
        
        return True, "OK"
    
    @classmethod
    def is_mobile(cls, phone: str) -> bool:
        """Verifica se e numero de celular"""
        if len(phone) < 5:
            return False
        number_part = phone[4:]
        return len(number_part) == 9 and number_part.startswith('9')