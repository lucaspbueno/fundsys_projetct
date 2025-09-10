from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.config import get_db
from app.models import Ativo, Indexador, Lote, Posicao
from typing import Optional
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

analytics_routes = APIRouter(tags=["Analytics"])

@analytics_routes.get("/overview")
async def get_overview(db: Session = Depends(get_db)):
    """Retorna visão geral dos dados do fundo"""
    try:
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
        ).join(Ativo).group_by(Indexador.cd_indexador).all()
        
        # Top 5 ativos por valor
        top_ativos = db.query(
            Ativo.cd_ativo,
            Posicao.vl_principal,
            Indexador.cd_indexador
        ).join(Posicao).join(Indexador).order_by(desc(Posicao.vl_principal)).limit(5).all()
        
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
                    "codigo": item.cd_ativo,
                    "valor": float(item.vl_principal),
                    "indexador": item.cd_indexador
                }
                for item in top_ativos
            ]
        }
    except Exception as e:
        logger.error(f"Erro ao buscar overview: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@analytics_routes.get("/ativos")
async def get_ativos(
    db: Session = Depends(get_db),
    indexador: Optional[str] = Query(None, description="Filtrar por indexador"),
    limit: int = Query(100, description="Limite de resultados"),
    offset: int = Query(0, description="Offset para paginação")
):
    """Retorna lista de ativos com filtros"""
    try:
        query = db.query(
            Ativo.cd_ativo,
            Ativo.cd_isin,
            Posicao.vl_principal,
            Indexador.cd_indexador,
            Lote.dt_operacao
        ).join(Posicao).join(Indexador).join(Lote)
        
        if indexador:
            query = query.filter(Indexador.cd_indexador == indexador)
        
        ativos = query.offset(offset).limit(limit).all()
        
        return {
            "ativos": [
                {
                    "codigo": ativo.cd_ativo,
                    "isin": ativo.cd_isin,
                    "valor": float(ativo.vl_principal),
                    "indexador": ativo.cd_indexador,
                    "data_operacao": ativo.dt_operacao.isoformat() if ativo.dt_operacao else None
                }
                for ativo in ativos
            ],
            "total": query.count(),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Erro ao buscar ativos: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@analytics_routes.get("/indexadores")
async def get_indexadores(db: Session = Depends(get_db)):
    """Retorna estatísticas dos indexadores"""
    try:
        indexadores = db.query(
            Indexador.cd_indexador,
            Indexador.sgl_indexador,
            func.count(Ativo.id_ativo).label('quantidade'),
            func.sum(Posicao.vl_principal).label('valor_total')
        ).join(Ativo).join(Posicao).group_by(
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
    except Exception as e:
        logger.error(f"Erro ao buscar indexadores: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@analytics_routes.get("/evolucao-mensal")
async def get_evolucao_mensal(
    db: Session = Depends(get_db),
    ano: Optional[int] = Query(None, description="Ano para filtrar")
):
    """Retorna evolução mensal dos ativos"""
    try:
        query = db.query(
            func.extract('month', Lote.dt_operacao).label('mes'),
            func.count(Ativo.id_ativo).label('quantidade'),
            func.sum(Posicao.vl_principal).label('valor_total')
        ).join(Posicao).join(Lote).group_by(
            func.extract('month', Lote.dt_operacao)
        )
        
        if ano:
            query = query.filter(func.extract('year', Lote.dt_operacao) == ano)
        
        evolucao = query.all()
        
        meses = {
            1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
            7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
        }
        
        return {
            "evolucao": [
                {
                    "mes": meses.get(int(item.mes), f"Mês {int(item.mes)}"),
                    "quantidade": item.quantidade,
                    "valor": float(item.valor_total or 0)
                }
                for item in evolucao
            ]
        }
    except Exception as e:
        logger.error(f"Erro ao buscar evolução mensal: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
