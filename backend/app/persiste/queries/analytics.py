from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models import Ativo, Indexador, Lote, Posicao, AtivoEnriquecido
from typing import List, Dict, Any, Optional
from decimal import Decimal


def get_overview_data(db: Session, enriched: bool = False) -> Dict[str, Any]:
    """Busca dados do overview geral"""
    # Total de ativos
    total_ativos = db.query(Ativo).count()
    
    # Total de indexadores únicos
    total_indexadores = db.query(Indexador).count()
    
    # Valor total (soma das posições)
    valor_total = db.query(func.sum(Posicao.vl_principal)).scalar() or 0
    
    # Indexadores com contagem
    indexadores_stats = db.query(
        Indexador.cd_indexador,
        func.count(Ativo.id_ativo).label('quantidade')
    ).select_from(Indexador).join(Ativo, Indexador.id_indexador == Ativo.id_indexador).group_by(Indexador.cd_indexador).all()
    
    # Top 5 ativos por valor
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
        ).select_from(Ativo).join(Posicao, Ativo.id_ativo == Posicao.id_ativo).join(Indexador, Ativo.id_indexador == Indexador.id_indexador).outerjoin(AtivoEnriquecido, Ativo.id_ativo == AtivoEnriquecido.id_ativo).order_by(desc(Posicao.vl_principal)).limit(5).all()
    else:
        top_ativos = db.query(
            Ativo.cd_ativo,
            Posicao.vl_principal,
            Indexador.cd_indexador
        ).select_from(Ativo).join(Posicao, Ativo.id_ativo == Posicao.id_ativo).join(Indexador, Ativo.id_indexador == Indexador.id_indexador).order_by(desc(Posicao.vl_principal)).limit(5).all()
    
    return {
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
                **({"serie": ativo.serie, "emissao": ativo.emissao, "devedor": ativo.devedor, "securitizadora": ativo.securitizadora, "resgate_antecipado": ativo.resgate_antecipado, "agente_fiduciario": ativo.agente_fiduciario} if enriched else {})
            }
            for ativo in top_ativos
        ]
    }


def get_indexadores_data(db: Session) -> Dict[str, Any]:
    """Busca dados dos indexadores"""
    indexadores = db.query(
        Indexador.cd_indexador,
        Indexador.sgl_indexador,
        func.count(Ativo.id_ativo).label('quantidade'),
        func.sum(Posicao.vl_principal).label('valor_total')
    ).select_from(Indexador).join(Ativo, Indexador.id_indexador == Ativo.id_indexador).join(Posicao, Ativo.id_ativo == Posicao.id_ativo).group_by(
        Indexador.cd_indexador, 
        Indexador.sgl_indexador
    ).all()
    
    total_ativos = db.query(Ativo).count()
    
    return {
        "indexadores": [
            {
                "codigo": item.cd_indexador,
                "sigla": item.sgl_indexador or "",
                "quantidade": item.quantidade,
                "percentual": round((item.quantidade / total_ativos * 100), 1) if total_ativos > 0 else 0,
                "valor_total": float(item.valor_total or 0)
            }
            for item in indexadores
        ]
    }


def get_ativos_data(
    db: Session, 
    indexador: Optional[str] = None, 
    limit: int = 50, 
    offset: int = 0,
    enriched: bool = False
) -> Dict[str, Any]:
    """Busca dados dos ativos com filtros"""
    if enriched:
        query = db.query(Ativo, Posicao, Indexador, AtivoEnriquecido).select_from(Ativo).join(Posicao, Ativo.id_ativo == Posicao.id_ativo).join(Indexador, Ativo.id_indexador == Indexador.id_indexador).outerjoin(AtivoEnriquecido, Ativo.id_ativo == AtivoEnriquecido.id_ativo)
    else:
        query = db.query(Ativo, Posicao, Indexador).select_from(Ativo).join(Posicao, Ativo.id_ativo == Posicao.id_ativo).join(Indexador, Ativo.id_indexador == Indexador.id_indexador)
    
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


def get_evolucao_mensal_data(
    db: Session, 
    ano: Optional[int] = None
) -> Dict[str, Any]:
    """Busca dados da evolução mensal"""
    query = db.query(
        func.extract('month', Lote.dt_operacao).label('mes'),
        func.count(Ativo.id_ativo).label('quantidade'),
        func.sum(Posicao.vl_principal).label('valor_total')
    ).select_from(Ativo).join(Posicao, Ativo.id_ativo == Posicao.id_ativo).join(Lote, Ativo.id_lote == Lote.id_lote).group_by(
        func.extract('month', Lote.dt_operacao)
    )
    
    if ano:
        query = query.filter(func.extract('year', Lote.dt_operacao) == ano)
    
    evolucao = query.all()
    
    return {
        "evolucao": [
            {
                "mes": int(item.mes),
                "quantidade": item.quantidade,
                "valor_total": float(item.valor_total or 0)
            }
            for item in evolucao
        ]
    }
