from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models import Lote, Ativo, Indexador, Posicao
from typing import List, Dict, Any, Optional
from decimal import Decimal


def get_file_history(
    db: Session, 
    limit: int = 10, 
    offset: int = 0
) -> Dict[str, Any]:
    """Busca histórico de arquivos com paginação"""
    # Buscar lotes com informações básicas
    lotes = (
        db.query(Lote)
        .order_by(desc(Lote.created_at))
        .offset(offset)
        .limit(limit)
        .all()
    )
    
    # Para cada lote, buscar estatísticas
    history_data = []
    for lote in lotes:
        # Contar ativos e valor total do lote
        ativos_count = db.query(Ativo).filter(Ativo.id_lote == lote.id_lote).count()
        valor_total = (
            db.query(func.sum(Posicao.vl_principal))
            .join(Ativo)
            .filter(Ativo.id_lote == lote.id_lote)
            .scalar() or 0
        )
        
        # Buscar indexadores únicos
        indexadores = (
            db.query(Indexador.cd_indexador)
            .join(Ativo)
            .filter(Ativo.id_lote == lote.id_lote)
            .distinct()
            .all()
        )
        
        history_data.append({
            "id_lote": lote.id_lote,
            "nome_arquivo": f"lote_{lote.id_lote}.xml",
            "data_envio": lote.created_at.isoformat(),
            "quantidade_ativos": ativos_count,
            "valor_total": float(valor_total),
            "indexadores": [idx.cd_indexador for idx in indexadores],
            "status": "processado"
        })
    
    # Contar total de lotes
    total_lotes = db.query(Lote).count()
    
    return {
        "files": history_data,
        "total": total_lotes,
        "limit": limit,
        "offset": offset
    }


def get_file_details(db: Session, lote_id: int) -> Optional[Dict[str, Any]]:
    """Busca detalhes de um arquivo específico"""
    # Buscar lote
    lote = db.query(Lote).filter(Lote.id_lote == lote_id).first()
    if not lote:
        return None
    
    # Buscar ativos do lote
    ativos = (
        db.query(Ativo, Posicao, Indexador)
        .join(Posicao)
        .join(Indexador)
        .filter(Ativo.id_lote == lote_id)
        .all()
    )
    
    # Organizar dados
    ativos_data = []
    for ativo, posicao, indexador in ativos:
        ativos_data.append({
            "codigo": ativo.cd_ativo,
            "valor_principal": float(posicao.vl_principal),
            "indexador": indexador.cd_indexador,
            "data_vencimento": ativo.dt_vencimento.isoformat() if ativo.dt_vencimento else None
        })
    
    # Estatísticas do lote
    total_ativos = len(ativos_data)
    valor_total = sum(ativo["valor_principal"] for ativo in ativos_data)
    
    # Indexadores únicos
    indexadores_unicos = list(set(ativo["indexador"] for ativo in ativos_data))
    
    return {
        "lote": {
            "id_lote": lote.id_lote,
            "nome_arquivo": f"lote_{lote.id_lote}.xml",
            "data_envio": lote.created_at.isoformat(),
            "status": "processado"
        },
        "estatisticas": {
            "total_ativos": total_ativos,
            "valor_total": valor_total,
            "indexadores": indexadores_unicos
        },
        "ativos": ativos_data
    }


def get_file_analytics(db: Session, lote_id: int) -> Optional[Dict[str, Any]]:
    """Busca analytics de um arquivo específico"""
    # Verificar se o lote existe
    lote = db.query(Lote).filter(Lote.id_lote == lote_id).first()
    if not lote:
        return None
    
    # Buscar dados do lote específico
    total_ativos = db.query(Ativo).filter(Ativo.id_lote == lote_id).count()
    total_indexadores = (
        db.query(Indexador.cd_indexador)
        .join(Ativo)
        .filter(Ativo.id_lote == lote_id)
        .distinct()
        .count()
    )
    valor_total = (
        db.query(func.sum(Posicao.vl_principal))
        .join(Ativo)
        .filter(Ativo.id_lote == lote_id)
        .scalar() or 0
    )
    
    # Distribuição por indexador
    indexadores_dist = (
        db.query(Indexador.cd_indexador, func.count(Ativo.id_ativo).label("quantidade"))
        .select_from(Indexador)
        .join(Ativo, Indexador.id_indexador == Ativo.id_indexador)
        .filter(Ativo.id_lote == lote_id)
        .group_by(Indexador.cd_indexador)
        .all()
    )
    
    indexadores_parsed = []
    for cd, qtd in indexadores_dist:
        percentual = (qtd / total_ativos * 100) if total_ativos else 0
        indexadores_parsed.append({
            "nome": cd, 
            "quantidade": qtd, 
            "percentual": round(percentual, 1)
        })
    
    # Top ativos
    top_ativos = (
        db.query(Ativo.cd_ativo, Posicao.vl_principal, Indexador.cd_indexador)
        .select_from(Ativo)
        .join(Posicao, Ativo.id_ativo == Posicao.id_ativo)
        .join(Indexador, Ativo.id_indexador == Indexador.id_indexador)
        .filter(Ativo.id_lote == lote_id)
        .order_by(desc(Posicao.vl_principal))
        .limit(5)
        .all()
    )
    
    top_ativos_parsed = [
        {
            "codigo": ativo.cd_ativo, 
            "valor": float(ativo.vl_principal), 
            "indexador": ativo.cd_indexador
        }
        for ativo in top_ativos
    ]
    
    return {
        "lote_id": lote_id,
        "nome_arquivo": f"lote_{lote.id_lote}.xml",
        "data_envio": lote.created_at.isoformat(),
        "total_ativos": total_ativos,
        "total_indexadores": total_indexadores,
        "valor_total": float(valor_total),
        "indexadores": indexadores_parsed,
        "top_ativos": top_ativos_parsed
    }
