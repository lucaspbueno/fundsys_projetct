from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging
from datetime import date

from app.services.anbima_enrichment import AnbimaEnrichmentService
from app.persiste.util.ativo_enriquecido import (
    insert_ativo_enriquecido,
    get_ativo_enriquecido_by_ativo_id,
    get_ativos_para_enriquecimento
)
from app.models import AtivoEnriquecido
from app.DTOs.ativo_enriquecido import AtivoEnriquecidoDTO

logger = logging.getLogger(__name__)

class EnrichmentService:
    """
    Serviço principal para enriquecimento de dados de ativos
    """
    
    def __init__(self):
        self.anbima_service = AnbimaEnrichmentService()
    
    def enrich_single_ativo(self, db: Session, ativo_id: int) -> Dict[str, Any]:
        """
        Enriquece um único ativo
        
        Args:
            db: Sessão do banco de dados
            ativo_id: ID do ativo a ser enriquecido
            
        Returns:
            Dict com resultado do enriquecimento
        """
        try:
            from app.models import Ativo
            
            # Buscar o ativo
            ativo = db.query(Ativo).filter(Ativo.id_ativo == ativo_id).first()
            if not ativo:
                return {
                    'sucesso': False,
                    'erro': 'Ativo não encontrado',
                    'ativo_id': ativo_id
                }
            
            # Verificar se já tem dados enriquecidos
            dados_existentes = get_ativo_enriquecido_by_ativo_id(db, ativo_id)
            if dados_existentes and not dados_existentes.fl_erro_enriquecimento:
                return {
                    'sucesso': True,
                    'mensagem': 'Ativo já possui dados enriquecidos',
                    'ativo_id': ativo_id,
                    'dados': dados_existentes
                }
            
            # Buscar dados na ANBIMA
            logger.info(f"Iniciando enriquecimento do ativo {ativo.cd_ativo} (ID: {ativo_id})")
            dados_anbima = self.anbima_service.enrich_ativo(ativo.cd_ativo)
            
            if not dados_anbima or dados_anbima.get('erro'):
                # Erro na busca
                ativo_enriquecido = AtivoEnriquecido(
                    id_ativo=ativo_id,
                    fl_enriquecido=False,
                    fl_erro_enriquecimento=True,
                    ds_erro_enriquecimento=dados_anbima.get('mensagem', 'Erro desconhecido') if dados_anbima else 'Nenhum dado encontrado',
                    dt_ultimo_enriquecimento=date.today()
                )
            else:
                # Sucesso na busca
                ativo_enriquecido = AtivoEnriquecido(
                    id_ativo=ativo_id,
                    serie=dados_anbima.get('serie'),
                    emissao=dados_anbima.get('emissao'),
                    devedor=dados_anbima.get('devedor'),
                    securitizadora=dados_anbima.get('securitizadora'),
                    resgate_antecipado=dados_anbima.get('resgate_antecipado'),
                    agente_fiduciario=dados_anbima.get('agente_fiduciario'),
                    fl_enriquecido=True,
                    fl_erro_enriquecimento=False,
                    dt_ultimo_enriquecimento=date.today()
                )
            
            # Persistir dados
            ativo_enriquecido_persistido = insert_ativo_enriquecido(db, ativo_enriquecido, commit=True)
            
            return {
                'sucesso': True,
                'ativo_id': ativo_id,
                'dados': ativo_enriquecido_persistido,
                'enriquecido': not ativo_enriquecido.fl_erro_enriquecimento
            }
            
        except Exception as e:
            logger.error(f"Erro ao enriquecer ativo {ativo_id}: {e}")
            return {
                'sucesso': False,
                'erro': str(e),
                'ativo_id': ativo_id
            }
    
    def enrich_multiple_ativos(self, db: Session, ativo_ids: List[int]) -> Dict[str, Any]:
        """
        Enriquece múltiplos ativos
        
        Args:
            db: Sessão do banco de dados
            ativo_ids: Lista de IDs dos ativos
            
        Returns:
            Dict com resultados do enriquecimento
        """
        resultados: Dict[str, Any] = {
            'sucessos': [],
            'erros': [],
            'total': len(ativo_ids),
            'enriquecidos': 0,
            'falhas': 0
        }
        
        for ativo_id in ativo_ids:
            resultado = self.enrich_single_ativo(db, ativo_id)
            
            if resultado['sucesso']:
                resultados['sucessos'].append(resultado)
                if resultado.get('enriquecido', False):
                    resultados['enriquecidos'] += 1
            else:
                resultados['erros'].append(resultado)
                resultados['falhas'] += 1
        
        return resultados
    
    def enrich_pending_ativos(self, db: Session, limit: int = 50) -> Dict[str, Any]:
        """
        Enriquece ativos pendentes de enriquecimento
        
        Args:
            db: Sessão do banco de dados
            limit: Limite de ativos a processar
            
        Returns:
            Dict com resultados do enriquecimento
        """
        try:
            # Buscar ativos pendentes
            ativos_pendentes = get_ativos_para_enriquecimento(db, limit)
            
            if not ativos_pendentes:
                return {
                    'sucesso': True,
                    'mensagem': 'Nenhum ativo pendente de enriquecimento',
                    'total': 0,
                    'enriquecidos': 0,
                    'falhas': 0
                }
            
            # Extrair IDs dos ativos
            ativo_ids = [ativo.id_ativo for ativo in ativos_pendentes]
            
            # Enriquecer ativos
            return self.enrich_multiple_ativos(db, ativo_ids)
            
        except Exception as e:
            logger.error(f"Erro ao enriquecer ativos pendentes: {e}")
            return {
                'sucesso': False,
                'erro': str(e),
                'total': 0,
                'enriquecidos': 0,
                'falhas': 0
            }
    
    def get_enrichment_status(self, db: Session) -> Dict[str, Any]:
        """
        Retorna status do enriquecimento dos ativos
        
        Args:
            db: Sessão do banco de dados
            
        Returns:
            Dict com estatísticas de enriquecimento
        """
        try:
            from app.models import Ativo, AtivoEnriquecido
            from sqlalchemy import func
            
            # Total de ativos
            total_ativos = db.query(func.count(Ativo.id_ativo)).scalar()
            
            # Ativos enriquecidos com sucesso
            ativos_enriquecidos = db.query(func.count(AtivoEnriquecido.id_ativo_enriquecido)).filter(
                AtivoEnriquecido.fl_enriquecido == True,
                AtivoEnriquecido.fl_erro_enriquecimento == False
            ).scalar()
            
            # Ativos com erro no enriquecimento
            ativos_com_erro = db.query(func.count(AtivoEnriquecido.id_ativo_enriquecido)).filter(
                AtivoEnriquecido.fl_erro_enriquecimento == True
            ).scalar()
            
            # Ativos sem dados enriquecidos
            ativos_sem_enriquecimento = total_ativos - ativos_enriquecidos - ativos_com_erro
            
            return {
                'total_ativos': total_ativos,
                'enriquecidos': ativos_enriquecidos,
                'com_erro': ativos_com_erro,
                'sem_enriquecimento': ativos_sem_enriquecimento,
                'percentual_enriquecidos': (ativos_enriquecidos / total_ativos * 100) if total_ativos > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter status de enriquecimento: {e}")
            return {
                'erro': str(e)
            }
