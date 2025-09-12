from sqlalchemy.orm import Session
from fastapi import UploadFile
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime

from app.models import FundoInvestimento, ArquivoOriginal
from app.DTOs.fundo_investimento import FundoInvestimentoDTO, ArquivoOriginalDTO, FundoComArquivoDTO
from app.services.file import upload_files_service
from app.utils import FileLoader, Parser
from app.persiste.util.fundo_investimento import (
    insert_fundo_investimento,
    insert_arquivo_original,
    get_fundo_by_id,
    get_fundo_by_hash_arquivo,
    get_all_fundos,
    count_fundos,
    get_arquivo_by_hash
)
from app.schemas.fundo_investimento import (
    FundoInvestimentoResponse,
    FundoDetalhesResponse,
    UploadFundoResponse,
    FundoListResponse,
    ArquivoDuplicadoResponse
)

logger = logging.getLogger(__name__)

class FundoInvestimentoService:
    """
    Serviço principal para gerenciamento de fundos de investimento
    """
    
    def __init__(self):
        pass
    
    async def processar_upload_arquivo(
        self,
        db: Session,
        arquivo: UploadFile,
        conteudo_arquivo: str
    ) -> UploadFundoResponse:
        """
        Processa o upload de um arquivo XML e cria um fundo de investimento
        
        Args:
            db: Sessão do banco de dados
            arquivo: Arquivo enviado
            conteudo_arquivo: Conteúdo do arquivo como string
            
        Returns:
            Resposta do upload
        """
        try:
            # Calcular hash do arquivo
            hash_arquivo = ArquivoOriginal.calcular_hash(conteudo_arquivo)
            
            # Verificar se arquivo já existe
            arquivo_existente = get_arquivo_by_hash(db, hash_arquivo)
            if arquivo_existente:
                logger.warning(f"Arquivo duplicado detectado: {arquivo.filename}")
                
                # Buscar fundo associado
                fundo_existente = get_fundo_by_id(db, arquivo_existente.id_fundo_investimento)
                
                return UploadFundoResponse(
                    sucesso=False,
                    mensagem="Este arquivo já foi analisado pela plataforma",
                    arquivo_duplicado=True,
                    fundo_existente=self._formatar_fundo_response(fundo_existente) if fundo_existente else None
                )
            
            # Criar novo fundo
            proximo_numero = count_fundos(db) + 1
            nome_fundo = f"fundo_de_investimento_{proximo_numero}"
            
            fundo = FundoInvestimento(
                nm_fundo_investimento=nome_fundo,
                ds_fundo_investimento=f"Fundo de investimento criado a partir do arquivo {arquivo.filename}",
                id_orgao_financeiro=None
            )
            
            # Persistir fundo
            fundo_persistido = insert_fundo_investimento(db, fundo, commit=True)
            
            # Criar registro do arquivo original
            arquivo_original = ArquivoOriginal(
                id_fundo_investimento=fundo_persistido.id_fundo_investimento,
                nm_arquivo=arquivo.filename,
                nm_arquivo_original=arquivo.filename,
                conteudo_arquivo=conteudo_arquivo,
                hash_arquivo=hash_arquivo,
                tamanho_arquivo=len(conteudo_arquivo),
                fl_processado=False
            )
            
            # Persistir arquivo
            arquivo_persistido = insert_arquivo_original(db, arquivo_original, commit=True)
            
            # Processar o XML para extrair dados (ativos, posições, indexadores)
            try:
                logger.info(f"Iniciando processamento do XML para o arquivo {arquivo.filename}")
                loader = FileLoader()
                parser = Parser()
                
                # Resetar o ponteiro do arquivo para o início
                await arquivo.seek(0)
                logger.info(f"Ponteiro do arquivo resetado para o início")
                
                # Criar uma lista com o arquivo para o serviço de upload
                arquivo_lista = [arquivo]
                
                # Processar o arquivo XML
                logger.info(f"Chamando upload_files_service com fundo_id: {fundo_persistido.id_fundo_investimento}")
                bundles = await upload_files_service(arquivo_lista, db, loader, parser, fundo_persistido.id_fundo_investimento)
                
                # Marcar arquivo como processado
                arquivo_persistido.fl_processado = True
                db.commit()
                
                logger.info(f"Arquivo XML processado com sucesso: {len(bundles)} bundles extraídos")
                
            except Exception as e:
                logger.error(f"Erro ao processar XML do arquivo {arquivo.filename}: {e}")
                logger.error(f"Tipo do erro: {type(e).__name__}")
                import traceback
                logger.error(f"Stack trace: {traceback.format_exc()}")
                # Não falha o upload, apenas registra o erro
                arquivo_persistido.fl_processado = False
                arquivo_persistido.ds_erro_processamento = str(e)
                db.commit()
            
            logger.info(f"Fundo criado com sucesso: {nome_fundo} (ID: {fundo_persistido.id_fundo_investimento})")
            
            return UploadFundoResponse(
                sucesso=True,
                mensagem="Arquivo processado com sucesso",
                fundo_id=fundo_persistido.id_fundo_investimento,
                arquivo_duplicado=False
            )
            
        except Exception as e:
            logger.error(f"Erro ao processar upload do arquivo {arquivo.filename}: {e}")
            return UploadFundoResponse(
                sucesso=False,
                mensagem=f"Erro ao processar arquivo: {str(e)}",
                arquivo_duplicado=False
            )
    
    def get_fundo_detalhes(
        self,
        db: Session,
        fundo_id: int
    ) -> Optional[FundoDetalhesResponse]:
        """
        Busca detalhes de um fundo específico
        
        Args:
            db: Sessão do banco de dados
            fundo_id: ID do fundo
            
        Returns:
            Detalhes do fundo ou None se não encontrado
        """
        try:
            fundo = get_fundo_by_id(db, fundo_id)
            if not fundo:
                return None
            
            # Buscar estatísticas do fundo
            from app.persiste.queries.fundo_analytics import get_fundo_analytics_data
            analytics = get_fundo_analytics_data(db, fundo_id, False, None, None, None, None)
            
            # Buscar arquivos do fundo
            arquivos = [
                {
                    "id": arq.id_arquivo_original,
                    "nome": arq.nm_arquivo,
                    "tamanho": arq.tamanho_arquivo,
                    "data_upload": arq.created_at.isoformat(),
                    "processado": arq.fl_processado
                }
                for arq in fundo.arquivos_originais
            ]
            
            return FundoDetalhesResponse(
                id_fundo_investimento=fundo.id_fundo_investimento,
                nm_fundo_investimento=fundo.nm_fundo_investimento,
                ds_fundo_investimento=fundo.ds_fundo_investimento,
                total_ativos=analytics.get('total_ativos', 0),
                valor_total=analytics.get('valor_total', 0.0),
                total_indexadores=analytics.get('total_indexadores', 0),
                data_criacao=fundo.created_at,
                ultima_atualizacao=fundo.updated_at,
                arquivos=arquivos
            )
            
        except Exception as e:
            logger.error(f"Erro ao buscar detalhes do fundo {fundo_id}: {e}")
            return None
    
    def get_lista_fundos(
        self,
        db: Session,
        limit: int = 50,
        offset: int = 0
    ) -> FundoListResponse:
        """
        Busca lista de fundos com paginação
        
        Args:
            db: Sessão do banco de dados
            limit: Limite de resultados
            offset: Offset para paginação
            
        Returns:
            Lista de fundos
        """
        try:
            fundos = get_all_fundos(db, limit, offset)
            total = count_fundos(db)
            
            fundos_response = [
                self._formatar_fundo_response(fundo) for fundo in fundos
            ]
            
            return FundoListResponse(
                fundos=fundos_response,
                total=total
            )
            
        except Exception as e:
            logger.error(f"Erro ao buscar lista de fundos: {e}")
            return FundoListResponse(fundos=[], total=0)
    
    def _formatar_fundo_response(self, fundo: FundoInvestimento) -> FundoInvestimentoResponse:
        """
        Formata um fundo para resposta da API
        
        Args:
            fundo: Instância do FundoInvestimento
            
        Returns:
            FundoInvestimentoResponse formatado
        """
        # Calcular estatísticas básicas
        total_ativos = len(fundo.ativos) if fundo.ativos else 0
        
        # Calcular valor total (soma das posições)
        valor_total = 0.0
        if fundo.ativos:
            for ativo in fundo.ativos:
                if ativo.posicoes:
                    for posicao in ativo.posicoes:
                        valor_total += float(posicao.vl_principal)
        
        return FundoInvestimentoResponse(
            id_fundo_investimento=fundo.id_fundo_investimento,
            nm_fundo_investimento=fundo.nm_fundo_investimento,
            ds_fundo_investimento=fundo.ds_fundo_investimento,
            total_ativos=total_ativos,
            valor_total=valor_total,
            data_criacao=fundo.created_at,
            ultima_atualizacao=fundo.updated_at or fundo.created_at
        )
