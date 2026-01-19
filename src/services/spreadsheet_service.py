"""
Servico de leitura de planilhas
"""
from pathlib import Path
from typing import List, Optional, Tuple
import pandas as pd

from src.models import Contact
from src.config import config


class SpreadsheetService:
    """Servico para leitura e processamento de planilhas"""
    
    def __init__(self):
        self._dataframe: Optional[pd.DataFrame] = None
        self._file_path: Optional[Path] = None
    
    def load(self, file_path: str) -> Tuple[bool, str]:
        """
        Carrega planilha do arquivo
        
        Returns:
            Tuple[sucesso, mensagem]
        """
        self._file_path = Path(file_path)
        
        # Valida arquivo
        if not self._file_path.exists():
            return False, "Arquivo nao encontrado"
        
        ext = self._file_path.suffix.lower()
        if ext not in config.SPREADSHEET_EXTENSIONS:
            return False, f"Extensao invalida. Use: {', '.join(config.SPREADSHEET_EXTENSIONS)}"
        
        try:
            # Le arquivo baseado na extensao
            if ext == '.csv':
                self._dataframe = pd.read_csv(self._file_path, dtype=str)
            elif ext == '.xlsx':
                self._dataframe = pd.read_excel(self._file_path, engine='openpyxl', dtype=str)
            elif ext == '.xls':
                self._dataframe = pd.read_excel(self._file_path, engine='xlrd', dtype=str)
            
            # Normaliza nomes das colunas
            self._dataframe.columns = [
                col.strip().lower().replace(' ', '_') 
                for col in self._dataframe.columns
            ]
            
            return True, f"{len(self._dataframe)} linhas carregadas"
            
        except Exception as e:
            return False, f"Erro ao ler arquivo: {str(e)}"
    
    def get_columns(self) -> List[str]:
        """Retorna lista de colunas disponiveis"""
        if self._dataframe is None:
            return []
        return list(self._dataframe.columns)
    
    def get_contacts(
        self,
        name_column: str = "nome_completo",
        phone_column: str = "telefone"
    ) -> List[Contact]:
        """
        Extrai contatos da planilha
        
        Args:
            name_column: Nome da coluna com nome completo
            phone_column: Nome da coluna com telefone
        
        Returns:
            Lista de objetos Contact
        """
        if self._dataframe is None:
            return []
        
        # Busca colunas
        name_col = self._find_column(name_column, ['nome', 'name', 'nome_completo'])
        phone_col = self._find_column(phone_column, ['telefone', 'phone', 'celular', 'whatsapp'])
        email_col = self._find_column("email", ['email', 'e-mail', 'correio'])
        city_col = self._find_column("cidade", ['cidade', 'city', 'municipio'])
        state_col = self._find_column("estado", ['estado', 'state', 'uf'])
        company_col = self._find_column("empresa", ['empresa', 'company', 'organizacao'])
        
        contacts = []
        for _, row in self._dataframe.iterrows():
            name = str(row[name_col]).strip() if pd.notna(row[name_col]) else ""
            phone = str(row[phone_col]).strip() if pd.notna(row[phone_col]) else ""
            
            # Coleta dados extras
            extra_data = {}
            for col in self._dataframe.columns:
                if col not in [name_col, phone_col]:
                    value = str(row[col]).strip() if pd.notna(row[col]) else ""
                    extra_data[col] = value
            
            email = extra_data.get('email', None)
            city = extra_data.get('cidade', None) 
            state = extra_data.get('estado', None)
            company = extra_data.get('empresa', None)
            
            if name and phone and name.lower() != 'nan':
                contacts.append(Contact(
                    full_name=name, 
                    phone=phone,
                    email=email,
                    city=city,
                    state=state,
                    company=company,
                    extra_data=extra_data
                ))
        
        return contacts
    
    def _find_column(self, target: str, alternatives: List[str]) -> Optional[str]:
        """Busca coluna pelo nome ou alternativas"""
        if self._dataframe is None:
            return None
            
        columns = list(self._dataframe.columns)
        target = target.lower().replace(' ', '_')
        
        # Busca exata
        if target in columns:
            return target
        
        # Busca por alternativas
        for alt in alternatives:
            if alt in columns:
                return alt
        
        # Busca parcial
        for col in columns:
            if target in col or any(alt in col for alt in alternatives):
                return col
        
        return None
    
    @property
    def row_count(self) -> int:
        """Retorna numero de linhas"""
        return len(self._dataframe) if self._dataframe is not None else 0
    
    @property
    def is_loaded(self) -> bool:
        """Verifica se planilha esta carregada"""
        return self._dataframe is not None