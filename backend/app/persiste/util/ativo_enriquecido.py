from sqlalchemy.orm import Session
from app.models import AtivoEnriquecido
from app.DTOs.ativo_enriquecido import AtivoEnriquecidoDTO
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def insert_ativo_enriquecido(
    db: Session,
    ativo_enriquecido: AtivoEnriquecido,
    *,
    commit: bool = False,
) -> AtivoEnriquecido:
    """
    Insere ou atualiza dados enriquecidos de um ativo
    
    Args:
        db: Sessão do banco de dados
        ativo_enriquecido: Instância do modelo AtivoEnriquecido
        commit: Se deve fazer commit da transação
        
    Returns:
        Instância do AtivoEnriquecido persistida
    """
    try:
        # Verificar se já existe dados enriquecidos para este ativo
        existing = db.query(AtivoEnriquecido).filter(
            AtivoEnriquecido.id_ativo == ativo_enriquecido.id_ativo
        ).first()
        
        if existing:
            # Atualizar dados existentes
            existing.serie = ativo_enriquecido.serie
            existing.emissao = ativo_enriquecido.emissao
            existing.devedor = ativo_enriquecido.devedor
            existing.securitizadora = ativo_enriquecido.securitizadora
            existing.resgate_antecipado = ativo_enriquecido.resgate_antecipado
            existing.agente_fiduciario = ativo_enriquecido.agente_fiduciario
            existing.fl_enriquecido = ativo_enriquecido.fl_enriquecido
            existing.dt_ultimo_enriquecimento = ativo_enriquecido.dt_ultimo_enriquecimento
            existing.fl_erro_enriquecimento = ativo_enriquecido.fl_erro_enriquecimento
            existing.ds_erro_enriquecimento = ativo_enriquecido.ds_erro_enriquecimento
            
            db.flush()
            logger.info(f"Dados enriquecidos atualizados para ativo {ativo_enriquecido.id_ativo}")
            return existing
        else:
            # Inserir novos dados
            db.add(ativo_enriquecido)
            db.flush()
            logger.info(f"Dados enriquecidos inseridos para ativo {ativo_enriquecido.id_ativo}")
            return ativo_enriquecido
            
    except Exception as e:
        logger.error(f"Erro ao persistir dados enriquecidos para ativo {ativo_enriquecido.id_ativo}: {e}")
        raise

def get_ativo_enriquecido_by_ativo_id(
    db: Session,
    id_ativo: int
) -> Optional[AtivoEnriquecido]:
    """
    Busca dados enriquecidos por ID do ativo
    
    Args:
        db: Sessão do banco de dados
        id_ativo: ID do ativo
        
    Returns:
        Instância do AtivoEnriquecido ou None se não encontrado
    """
    try:
        return db.query(AtivoEnriquecido).filter(
            AtivoEnriquecido.id_ativo == id_ativo
        ).first()
    except Exception as e:
        logger.error(f"Erro ao buscar dados enriquecidos para ativo {id_ativo}: {e}")
        return None

def get_ativos_para_enriquecimento(
    db: Session,
    limit: int = 100
) -> list[AtivoEnriquecido]:
    """
    Busca ativos que precisam ser enriquecidos
    
    Args:
        db: Sessão do banco de dados
        limit: Limite de ativos a retornar
        
    Returns:
        Lista de ativos que precisam ser enriquecidos
    """
    try:
        from app.models import Ativo
        
        # Buscar ativos que não têm dados enriquecidos ou que falharam no enriquecimento
        subquery = db.query(AtivoEnriquecido.id_ativo).subquery()
        
        ativos = db.query(Ativo).outerjoin(
            AtivoEnriquecido, Ativo.id_ativo == AtivoEnriquecido.id_ativo
        ).filter(
            (AtivoEnriquecido.id_ativo == None) | 
            (AtivoEnriquecido.fl_erro_enriquecimento == True)
        ).limit(limit).all()
        
        return ativos
    except Exception as e:
        logger.error(f"Erro ao buscar ativos para enriquecimento: {e}")
        return []

