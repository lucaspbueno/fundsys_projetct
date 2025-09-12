from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models import Ativo, Indexador, Lote, Posicao, AtivoEnriquecido, FundoInvestimento
from typing import Dict, Any, Optional
from decimal import Decimal

def get_fundo_analytics_data(db: Session, fundo_id: int, enriched: bool = False) -> Dict[str, Any]:
    """
    Busca dados de analytics para um fundo específico
    
    Args:
        db: Sessão do banco de dados
        fundo_id: ID do fundo
        enriched: Se deve incluir dados enriquecidos
        
    Returns:
        Dict com dados de analytics do fundo
    """
    try:
        # Verificar se fundo existe
        fundo = db.query(FundoInvestimento).filter(
            FundoInvestimento.id_fundo_investimento == fundo_id
        ).first()
        
        if not fundo:
            return {}
        
        # Total de ativos do fundo
        total_ativos = db.query(Ativo).filter(
            Ativo.id_fundo == fundo_id
        ).count()
        
        # Total de indexadores únicos do fundo
        total_indexadores = db.query(Indexador).join(Ativo).filter(
            Ativo.id_fundo == fundo_id
        ).count()
        
        # Valor total do fundo (soma das posições)
        valor_total = db.query(func.sum(Posicao.vl_principal)).join(Ativo).filter(
            Ativo.id_fundo == fundo_id
        ).scalar() or 0
        
        # Indexadores com contagem do fundo
        indexadores_stats = db.query(
            Indexador.cd_indexador,
            func.count(Ativo.id_ativo).label('quantidade')
        ).select_from(Indexador).join(Ativo, Indexador.id_indexador == Ativo.id_indexador).filter(
            Ativo.id_fundo == fundo_id
        ).group_by(Indexador.cd_indexador).all()
        
        # Top 5 ativos por valor do fundo
        if enriched:
            top_ativos = db.query(
                Ativo.cd_ativo,
                Posicao.vl_principal,
                Indexador.cd_indexador,
                AtivoEnriquecido.serie,
                AtivoEnriquecido.emissao,
                AtivoEnriquecido.devedor,
                AtivoEnriquecido.securitizadora,
                AtivoEnriquecido.resgate_antecipado,
                AtivoEnriquecido.agente_fiduciario
            ).select_from(Ativo).join(Posicao, Ativo.id_ativo == Posicao.id_ativo).join(
                Indexador, Ativo.id_indexador == Indexador.id_indexador
            ).outerjoin(AtivoEnriquecido, Ativo.id_ativo == AtivoEnriquecido.id_ativo).filter(
                Ativo.id_fundo == fundo_id
            ).order_by(desc(Posicao.vl_principal)).limit(5).all()
        else:
            top_ativos = db.query(
                Ativo.cd_ativo,
                Posicao.vl_principal,
                Indexador.cd_indexador
            ).select_from(Ativo).join(Posicao, Ativo.id_ativo == Posicao.id_ativo).join(
                Indexador, Ativo.id_indexador == Indexador.id_indexador
            ).filter(
                Ativo.id_fundo == fundo_id
            ).order_by(desc(Posicao.vl_principal)).limit(5).all()
        
        # Evolução mensal do fundo
        evolucao_mensal = db.query(
            func.extract('month', Lote.dt_operacao).label('mes'),
            func.count(Ativo.id_ativo).label('quantidade'),
            func.sum(Posicao.vl_principal).label('valor_total')
        ).select_from(Ativo).join(Posicao, Ativo.id_ativo == Posicao.id_ativo).join(
            Lote, Ativo.id_lote == Lote.id_lote
        ).filter(
            Ativo.id_fundo == fundo_id
        ).group_by(
            func.extract('month', Lote.dt_operacao)
        ).all()
        
        # Mapear números de mês para nomes
        meses_nomes = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }
        
        return {
            "fundo_id": fundo_id,
            "fundo_nome": fundo.nm_fundo_investimento,
            "total_ativos": total_ativos,
            "total_indexadores": total_indexadores,
            "valor_total": float(valor_total),
            "indexadores": [
                {
                    "nome": item.cd_indexador,
                    "quantidade": item.quantidade,
                    "percentual": round((item.quantidade / total_ativos * 100), 1) if total_ativos > 0 else 0
                }
                for item in indexadores_stats
            ],
            "top_ativos": [
                {
                    "codigo": ativo.cd_ativo,
                    "valor": float(ativo.vl_principal),
                    "indexador": ativo.cd_indexador,
                    **({"serie": ativo.serie, "emissao": ativo.emissao, "devedor": ativo.devedor, 
                        "securitizadora": ativo.securitizadora, "resgate_antecipado": ativo.resgate_antecipado, 
                        "agente_fiduciario": ativo.agente_fiduciario} if enriched else {})
                }
                for ativo in top_ativos
            ],
            "evolucao_mensal": [
                {
                    "mes": meses_nomes.get(int(item.mes), f"Mês {int(item.mes)}"),
                    "quantidade": item.quantidade,
                    "valor_total": float(item.valor_total or 0)
                }
                for item in evolucao_mensal
            ]
        }
        
    except Exception as e:
        print(f"Erro ao buscar analytics do fundo {fundo_id}: {e}")
        return {}

def get_fundo_ativos_data(
    db: Session, 
    fundo_id: int,
    indexador: Optional[str] = None, 
    limit: int = 50, 
    offset: int = 0,
    enriched: bool = False
) -> Dict[str, Any]:
    """
    Busca dados dos ativos de um fundo específico
    
    Args:
        db: Sessão do banco de dados
        fundo_id: ID do fundo
        indexador: Filtro por indexador
        limit: Limite de resultados
        offset: Offset para paginação
        enriched: Se deve incluir dados enriquecidos
        
    Returns:
        Dict com dados dos ativos do fundo
    """
    try:
        if enriched:
            query = db.query(Ativo, Posicao, Indexador, AtivoEnriquecido).select_from(Ativo).join(
                Posicao, Ativo.id_ativo == Posicao.id_ativo
            ).join(Indexador, Ativo.id_indexador == Indexador.id_indexador).outerjoin(
                AtivoEnriquecido, Ativo.id_ativo == AtivoEnriquecido.id_ativo
            ).filter(Ativo.id_fundo == fundo_id)
        else:
            query = db.query(Ativo, Posicao, Indexador).select_from(Ativo).join(
                Posicao, Ativo.id_ativo == Posicao.id_ativo
            ).join(Indexador, Ativo.id_indexador == Indexador.id_indexador).filter(
                Ativo.id_fundo == fundo_id
            )
        
        if indexador:
            query = query.filter(Indexador.cd_indexador == indexador)
        
        ativos = query.offset(offset).limit(limit).all()
        total = query.count()
        
        if enriched:
            return {
                "ativos": [
                    {
                        "codigo": ativo.cd_ativo,
                        "valor_principal": float(posicao.vl_principal),
                        "indexador": indexador.cd_indexador,
                        "data_vencimento": ativo.dt_vencimento.isoformat() if ativo.dt_vencimento else None,
                        "serie": ativo_enriquecido.serie if ativo_enriquecido else None,
                        "emissao": ativo_enriquecido.emissao if ativo_enriquecido else None,
                        "devedor": ativo_enriquecido.devedor if ativo_enriquecido else None,
                        "securitizadora": ativo_enriquecido.securitizadora if ativo_enriquecido else None,
                        "resgate_antecipado": ativo_enriquecido.resgate_antecipado if ativo_enriquecido else None,
                        "agente_fiduciario": ativo_enriquecido.agente_fiduciario if ativo_enriquecido else None
                    }
                    for ativo, posicao, indexador, ativo_enriquecido in ativos
                ],
                "total": total,
                "limit": limit,
                "offset": offset
            }
        else:
            return {
                "ativos": [
                    {
                        "codigo": ativo.cd_ativo,
                        "valor_principal": float(posicao.vl_principal),
                        "indexador": indexador.cd_indexador,
                        "data_vencimento": ativo.dt_vencimento.isoformat() if ativo.dt_vencimento else None
                    }
                    for ativo, posicao, indexador in ativos
                ],
                "total": total,
                "limit": limit,
                "offset": offset
            }
            
    except Exception as e:
        print(f"Erro ao buscar ativos do fundo {fundo_id}: {e}")
        return {"ativos": [], "total": 0, "limit": limit, "offset": offset}

