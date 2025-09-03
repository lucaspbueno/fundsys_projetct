from fastapi import APIRouter, UploadFile, File, Depends, status, HTTPException
from app.utils import FileLoader, Parser
from app.provider import get_file_loader, get_file_parser
from app.services import upload_files_service
from app.schemas import UploadFilesResponse
from sqlalchemy.orm import Session
from app.config import get_db
from logging_config import logger

file_routes = APIRouter(prefix="/file", tags=["Arquivos"])

@file_routes.post(
    "/upload_files",
    response_model = UploadFilesResponse,
    status_code    = status.HTTP_201_CREATED,
    summary        = "Recebe n arquivos xml com informações de uma posição de um fundo de investimentos e insere no banco de dados",
)
async def upload_files_route(
    ls_files: list[UploadFile] = File(...),
    db      : Session          = Depends(get_db),
    loader  : FileLoader       = Depends(get_file_loader),
    parser  : Parser           = Depends(get_file_parser)
):
    try:
        bundles = await upload_files_service(ls_files=ls_files, db=db, loader=loader, parser=parser)
        return UploadFilesResponse(
            str_message="Arquivos processados com sucesso!",
            qtd_arquivos_processados=len(ls_files),
            data=bundles,
        )
    except ValueError as e:
        logger.warning(f"Erro de validação: {e}")
        # erros previstos de entrada/regra → 400
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # erro inesperado → 500 genérico
        logger.error(f"Erro inesperado ao processar arquivos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar arquivos")
