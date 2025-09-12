from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models import Ativo, Indexador, Lote, Posicao, AtivoEnriquecido
from typing import List, Dict, Any, Optional
from decimal import Decimal


def get_overview_data(
    db: Session, 
    enriched: bool = False,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    indexador: Optional[str] = None,
    codigo_ativo: Optional[str] = None
) -> Dict[str, Any]:
    """Busca dados do overview geral"""
    from datetime import datetime
    
    # Construir query base com joins necessários
    base_query = db.query(Ativo).join(Posicao, Ativo.id_ativo == Posicao.id_ativo).join(Indexador, Ativo.id_indexador == Indexador.id_indexador)
    
    # Aplicar filtros
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            base_query = base_query.filter(Posicao.dt_posicao >= date_from_obj)
        except ValueError:
            pass  # Ignorar data inválida
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            base_query = base_query.filter(Posicao.dt_posicao <= date_to_obj)
        except ValueError:
            pass  # Ignorar data inválida
    
    if indexador:
        base_query = base_query.filter(Indexador.cd_indexador == indexador)
    
    if codigo_ativo:
        base_query = base_query.filter(Ativo.cd_ativo.ilike(f'%{codigo_ativo}%'))
    
    # Total de ativos (com filtros aplicados)
    total_ativos = base_query.count()
    
    # Total de indexadores únicos (com filtros aplicados)
    total_indexadores = base_query.with_entities(Indexador.id_indexador).distinct().count()
    
    # Valor total (soma das posições com filtros aplicados)
    valor_total = base_query.with_entities(func.sum(Posicao.vl_principal)).scalar() or 0
    
    # Indexadores com contagem (aplicar filtros)
    indexadores_query = base_query.with_entities(
        Indexador.cd_indexador,
        func.count(Ativo.id_ativo).label('quantidade')
    ).group_by(Indexador.cd_indexador)
    indexadores_stats = indexadores_query.all()
    
    # Top 5 ativos por valor (aplicar filtros)
    if enriched:
        top_ativos_query = base_query.with_entities(
            Ativo.cd_ativo,
            Posicao.vl_principal,
            Indexador.cd_indexador,
            AtivoEnriquecido.serie,
            AtivoEnriquecido.emissao,
            AtivoEnriquecido.devedor,
            AtivoEnriquecido.securitizadora,
            AtivoEnriquecido.resgate_antecipado,
            AtivoEnriquecido.agente_fiduciario
        ).outerjoin(AtivoEnriquecido, Ativo.id_ativo == AtivoEnriquecido.id_ativo).order_by(desc(Posicao.vl_principal)).limit(5)
        top_ativos = top_ativos_query.all()
    else:
        top_ativos_query = base_query.with_entities(
            Ativo.cd_ativo,
            Posicao.vl_principal,
            Indexador.cd_indexador
        ).order_by(desc(Posicao.vl_principal)).limit(5)
        top_ativos = top_ativos_query.all()
    
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
    enriched: bool = False,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    codigo_ativo: Optional[str] = None
) -> Dict[str, Any]:
    """Busca dados dos ativos com filtros"""
    from datetime import datetime
    
    if enriched:
        enriched_query = db.query(Ativo, Posicao, Indexador, AtivoEnriquecido).select_from(Ativo).join(Posicao, Ativo.id_ativo == Posicao.id_ativo).join(Indexador, Ativo.id_indexador == Indexador.id_indexador).outerjoin(AtivoEnriquecido, Ativo.id_ativo == AtivoEnriquecido.id_ativo)
        
        # Aplicar filtros
        if indexador:
            enriched_query = enriched_query.filter(Indexador.cd_indexador == indexador)
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                enriched_query = enriched_query.filter(Posicao.dt_posicao >= date_from_obj)
            except ValueError:
                pass
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
                enriched_query = enriched_query.filter(Posicao.dt_posicao <= date_to_obj)
            except ValueError:
                pass
        if codigo_ativo:
            enriched_query = enriched_query.filter(Ativo.cd_ativo.ilike(f'%{codigo_ativo}%'))
            
        ativos_enriched = enriched_query.offset(offset).limit(limit).all()
        total = enriched_query.count()
    else:
        simple_query = db.query(Ativo, Posicao, Indexador).select_from(Ativo).join(Posicao, Ativo.id_ativo == Posicao.id_ativo).join(Indexador, Ativo.id_indexador == Indexador.id_indexador)
        
        # Aplicar filtros
        if indexador:
            simple_query = simple_query.filter(Indexador.cd_indexador == indexador)
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                simple_query = simple_query.filter(Posicao.dt_posicao >= date_from_obj)
            except ValueError:
                pass
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
                simple_query = simple_query.filter(Posicao.dt_posicao <= date_to_obj)
            except ValueError:
                pass
        if codigo_ativo:
            simple_query = simple_query.filter(Ativo.cd_ativo.ilike(f'%{codigo_ativo}%'))
            
        ativos_simple = simple_query.offset(offset).limit(limit).all()
        total = simple_query.count()
    
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
                for ativo, posicao, indexador, ativo_enriquecido in ativos_enriched
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
                for ativo, posicao, indexador in ativos_simple
            ],
            "total": total,
            "limit": limit,
            "offset": offset
        }


def get_evolucao_mensal_data(
    db: Session, 
    ano: Optional[int] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    indexador: Optional[str] = None,
    codigo_ativo: Optional[str] = None
) -> Dict[str, Any]:
    """Busca dados da evolução mensal"""
    from datetime import datetime
    
    # Construir query base com joins necessários
    query = db.query(
        func.extract('month', Lote.dt_operacao).label('mes'),
        func.count(Ativo.id_ativo).label('quantidade'),
        func.sum(Posicao.vl_principal).label('valor_total')
    ).select_from(Ativo).join(Posicao, Ativo.id_ativo == Posicao.id_ativo).join(Lote, Ativo.id_lote == Lote.id_lote).join(Indexador, Ativo.id_indexador == Indexador.id_indexador).group_by(
        func.extract('month', Lote.dt_operacao)
    )
    
    # Aplicar filtros
    if ano:
        query = query.filter(func.extract('year', Lote.dt_operacao) == ano)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(Posicao.dt_posicao >= date_from_obj)
        except ValueError:
            pass  # Ignorar data inválida
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(Posicao.dt_posicao <= date_to_obj)
        except ValueError:
            pass  # Ignorar data inválida
    
    if indexador:
        query = query.filter(Indexador.cd_indexador == indexador)
    
    if codigo_ativo:
        query = query.filter(Ativo.cd_ativo.ilike(f'%{codigo_ativo}%'))
    
    evolucao = query.all()
    
    # Mapeamento de números para nomes dos meses
    meses_nomes = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    
    return {
        "evolucao": [
            {
                "mes": meses_nomes.get(int(item.mes), f"Mês {int(item.mes)}"),
                "quantidade": item.quantidade,
                "valor_total": float(item.valor_total or 0)
            }
            for item in evolucao
        ]
    }
