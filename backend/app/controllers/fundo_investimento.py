from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.config import get_db
from app.services.fundo_investimento import FundoInvestimentoService
from app.schemas.fundo_investimento import (
    FundoInvestimentoResponse,
    FundoDetalhesResponse,
    UploadFundoResponse,
    FundoListResponse
)
from app.utils import FileLoader

logger = logging.getLogger(__name__)

fundo_routes = APIRouter(prefix="/fundo", tags=["Fundo de Investimento"])

@fundo_routes.post("/upload", response_model=UploadFundoResponse)
async def upload_arquivo_fundo(
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload de arquivo XML para criar um fundo de investimento
    """
    try:
        # Validar tipo de arquivo
        if not arquivo.filename.endswith('.xml'):
            raise HTTPException(status_code=400, detail="Apenas arquivos XML são aceitos")
        
        # Carregar conteúdo do arquivo
        loader = FileLoader()
        conteudo = await loader.load_text(arquivo)
        
        # Processar upload
        service = FundoInvestimentoService()
        resultado = await service.processar_upload_arquivo(db, arquivo, conteudo)
        
        if not resultado.sucesso:
            if resultado.arquivo_duplicado:
                raise HTTPException(
                    status_code=409, 
                    detail=resultado.mensagem,
                    headers={"X-Fundo-Existente": str(resultado.fundo_existente.id_fundo_investimento) if resultado.fundo_existente else ""}
                )
            else:
                raise HTTPException(status_code=400, detail=resultado.mensagem)
        
        return resultado
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no upload do arquivo: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@fundo_routes.get("/", response_model=FundoListResponse)
async def listar_fundos(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=100, description="Limite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginação")
):
    """
    Lista todos os fundos de investimento
    """
    try:
        service = FundoInvestimentoService()
        return service.get_lista_fundos(db, limit, offset)
    except Exception as e:
        logger.error(f"Erro ao listar fundos: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@fundo_routes.get("/{fundo_id}", response_model=FundoDetalhesResponse)
async def get_fundo_detalhes(
    fundo_id: int,
    db: Session = Depends(get_db)
):
    """
    Busca detalhes de um fundo específico
    """
    try:
        service = FundoInvestimentoService()
        fundo = service.get_fundo_detalhes(db, fundo_id)
        
        if not fundo:
            raise HTTPException(status_code=404, detail="Fundo não encontrado")
        
        return fundo
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar fundo {fundo_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@fundo_routes.delete("/{fundo_id}")
async def deletar_fundo(
    fundo_id: int,
    db: Session = Depends(get_db)
):
    """
    Deleta um fundo de investimento e todos os seus dados
    """
    try:
        from app.persiste.util.fundo_investimento import get_fundo_by_id
        
        fundo = get_fundo_by_id(db, fundo_id)
        if not fundo:
            raise HTTPException(status_code=404, detail="Fundo não encontrado")
        
        # Deletar fundo (cascade deletará ativos, posições, etc.)
        db.delete(fundo)
        db.commit()
        
        logger.info(f"Fundo {fundo_id} deletado com sucesso")
        return {"mensagem": "Fundo deletado com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar fundo {fundo_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

