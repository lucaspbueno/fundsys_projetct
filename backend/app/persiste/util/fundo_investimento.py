from sqlalchemy.orm import Session
from app.models import FundoInvestimento, ArquivoOriginal
from app.DTOs.fundo_investimento import FundoInvestimentoDTO, ArquivoOriginalDTO
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

def insert_fundo_investimento(
    db: Session,
    fundo: FundoInvestimento,
    *,
    commit: bool = False,
) -> FundoInvestimento:
    """
    Insere um novo fundo de investimento
    
    Args:
        db: Sessão do banco de dados
        fundo: Instância do modelo FundoInvestimento
        commit: Se deve fazer commit da transação
        
    Returns:
        Instância do FundoInvestimento persistida
    """
    try:
        db.add(fundo)
        if commit:
            db.commit()
        else:
            db.flush()
        
        logger.info(f"Fundo de investimento inserido: {fundo.nm_fundo_investimento} (ID: {fundo.id_fundo_investimento})")
        return fundo
        
    except Exception as e:
        logger.error(f"Erro ao inserir fundo de investimento: {e}")
        if commit:
            db.rollback()
        raise

def insert_arquivo_original(
    db: Session,
    arquivo: ArquivoOriginal,
    *,
    commit: bool = False,
) -> ArquivoOriginal:
    """
    Insere um arquivo original
    
    Args:
        db: Sessão do banco de dados
        arquivo: Instância do modelo ArquivoOriginal
        commit: Se deve fazer commit da transação
        
    Returns:
        Instância do ArquivoOriginal persistida
    """
    try:
        db.add(arquivo)
        if commit:
            db.commit()
        else:
            db.flush()
        
        logger.info(f"Arquivo original inserido: {arquivo.nm_arquivo} (ID: {arquivo.id_arquivo_original})")
        return arquivo
        
    except Exception as e:
        logger.error(f"Erro ao inserir arquivo original: {e}")
        if commit:
            db.rollback()
        raise

def get_fundo_by_id(
    db: Session,
    fundo_id: int
) -> Optional[FundoInvestimento]:
    """
    Busca um fundo por ID
    
    Args:
        db: Sessão do banco de dados
        fundo_id: ID do fundo
        
    Returns:
        Instância do FundoInvestimento ou None se não encontrado
    """
    try:
        return db.query(FundoInvestimento).filter(
            FundoInvestimento.id_fundo_investimento == fundo_id
        ).first()
    except Exception as e:
        logger.error(f"Erro ao buscar fundo {fundo_id}: {e}")
        return None

def get_fundo_by_hash_arquivo(
    db: Session,
    hash_arquivo: str
) -> Optional[FundoInvestimento]:
    """
    Busca um fundo pelo hash do arquivo (para detectar duplicatas)
    
    Args:
        db: Sessão do banco de dados
        hash_arquivo: Hash do arquivo
        
    Returns:
        Instância do FundoInvestimento ou None se não encontrado
    """
    try:
        return db.query(FundoInvestimento).join(
            ArquivoOriginal, 
            FundoInvestimento.id_fundo_investimento == ArquivoOriginal.id_fundo_investimento
        ).filter(
            ArquivoOriginal.hash_arquivo == hash_arquivo
        ).first()
    except Exception as e:
        logger.error(f"Erro ao buscar fundo por hash {hash_arquivo}: {e}")
        return None

def get_all_fundos(
    db: Session,
    limit: int = 50,
    offset: int = 0
) -> List[FundoInvestimento]:
    """
    Busca todos os fundos com paginação
    
    Args:
        db: Sessão do banco de dados
        limit: Limite de resultados
        offset: Offset para paginação
        
    Returns:
        Lista de fundos
    """
    try:
        return db.query(FundoInvestimento).order_by(
            FundoInvestimento.created_at.desc()
        ).offset(offset).limit(limit).all()
    except Exception as e:
        logger.error(f"Erro ao buscar fundos: {e}")
        return []

def count_fundos(db: Session) -> int:
    """
    Conta o total de fundos
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Número total de fundos
    """
    try:
        return db.query(FundoInvestimento).count()
    except Exception as e:
        logger.error(f"Erro ao contar fundos: {e}")
        return 0

def get_arquivo_by_hash(
    db: Session,
    hash_arquivo: str
) -> Optional[ArquivoOriginal]:
    """
    Busca um arquivo pelo hash
    
    Args:
        db: Sessão do banco de dados
        hash_arquivo: Hash do arquivo
        
    Returns:
        Instância do ArquivoOriginal ou None se não encontrado
    """
    try:
        return db.query(ArquivoOriginal).filter(
            ArquivoOriginal.hash_arquivo == hash_arquivo
        ).first()
    except Exception as e:
        logger.error(f"Erro ao buscar arquivo por hash {hash_arquivo}: {e}")
        return None

