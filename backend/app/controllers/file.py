# app/controllers/xml_controller.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from logging_config import logger
from app.services.file import XmlService

file_routes = APIRouter(prefix="/xml", tags=["XML"])
service = XmlService()

@file_routes.post("/read")
async def read_many_xml(files: List[UploadFile] = File(...)):
    """
    Recebe N arquivos XML (campo 'files') e retorna um resumo de cada um:
    - root_tag e contagem de <titprivado>, + tamanho em bytes
    - sem salvar nada no banco por enquanto
    """
    if not files:
        raise HTTPException(status_code=400, detail="Envie pelo menos um arquivo XML.")

    logger.info(f"[XML] Recebidos {len(files)} arquivo(s) para leitura.")  # logger já existe:contentReference[oaicite:2]{index=2}
    result = await service.analyze_many(files)
    logger.info(f"[XML] Processados {result['processed']}/{result['received']}.")
    return result
