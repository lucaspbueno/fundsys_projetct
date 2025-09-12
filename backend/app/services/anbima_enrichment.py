import requests
from bs4 import BeautifulSoup
import logging
from typing import Optional, Dict, Any
from datetime import date
import time
import re

logger = logging.getLogger(__name__)

class AnbimaEnrichmentService:
    """
    Serviço para enriquecer dados de ativos com informações da ANBIMA Data
    """
    
    BASE_URL = "https://data.anbima.com.br/certificado-de-recebiveis/{cod_ativo}/caracteristicas"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def enrich_ativo(self, cod_ativo: str) -> Optional[Dict[str, Any]]:
        """
        Enriquece um ativo com dados da ANBIMA
        
        Args:
            cod_ativo: Código do ativo para buscar na ANBIMA
            
        Returns:
            Dict com os dados enriquecidos ou None se houver erro
        """
        try:
            url = self.BASE_URL.format(cod_ativo=cod_ativo)
            logger.info(f"Buscando dados para ativo {cod_ativo} na URL: {url}")
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrair dados da página
            dados = self._extract_data_from_page(soup, cod_ativo)
            
            if dados:
                logger.info(f"Dados enriquecidos obtidos para ativo {cod_ativo}: {dados}")
            else:
                logger.warning(f"Nenhum dado encontrado para ativo {cod_ativo}")
                
            return dados
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição para ativo {cod_ativo}: {e}")
            return {
                'erro': True,
                'mensagem': f"Erro na requisição: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Erro inesperado ao enriquecer ativo {cod_ativo}: {e}")
            return {
                'erro': True,
                'mensagem': f"Erro inesperado: {str(e)}"
            }
    
    def _extract_data_from_page(self, soup: BeautifulSoup, cod_ativo: str) -> Optional[Dict[str, Any]]:
        """
        Extrai dados específicos da página da ANBIMA
        
        Args:
            soup: Objeto BeautifulSoup da página
            cod_ativo: Código do ativo
            
        Returns:
            Dict com os dados extraídos ou None
        """
        try:
            dados = {
                'serie': None,
                'emissao': None,
                'devedor': None,
                'securitizadora': None,
                'resgate_antecipado': None,
                'agente_fiduciario': None,
                'dt_ultimo_enriquecimento': None
            }
            
            # Procurar por tabelas ou divs com os dados
            # A estrutura da página pode variar, então vamos tentar diferentes seletores
            
            # Tentar encontrar dados em tabelas
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        label = cells[0].get_text(strip=True).lower()
                        value = cells[1].get_text(strip=True)
                        
                        if 'série' in label or 'serie' in label:
                            dados['serie'] = value
                        elif 'emissão' in label or 'emissao' in label:
                            dados['emissao'] = value
                        elif 'devedor' in label:
                            dados['devedor'] = value
                        elif 'securitizadora' in label:
                            dados['securitizadora'] = value
                        elif 'resgate' in label and 'antecipado' in label:
                            dados['resgate_antecipado'] = self._parse_boolean(value)
                        elif 'agente' in label and 'fiduciário' in label:
                            dados['agente_fiduciario'] = value
            
            # Tentar encontrar dados em divs com classes específicas
            divs = soup.find_all('div', class_=re.compile(r'(info|data|field)', re.I))
            for div in divs:
                text = div.get_text(strip=True)
                if ':' in text:
                    parts = text.split(':', 1)
                    if len(parts) == 2:
                        label = parts[0].strip().lower()
                        value = parts[1].strip()
                        
                        if 'série' in label or 'serie' in label:
                            dados['serie'] = value
                        elif 'emissão' in label or 'emissao' in label:
                            dados['emissao'] = value
                        elif 'devedor' in label:
                            dados['devedor'] = value
                        elif 'securitizadora' in label:
                            dados['securitizadora'] = value
                        elif 'resgate' in label and 'antecipado' in label:
                            dados['resgate_antecipado'] = self._parse_boolean(value)
                        elif 'agente' in label and 'fiduciário' in label:
                            dados['agente_fiduciario'] = value
            
            # Verificar se encontramos pelo menos um dado
            if any(dados.values()):
                dados['dt_ultimo_enriquecimento'] = date.today()
                return dados
            else:
                logger.warning(f"Nenhum dado estruturado encontrado para ativo {cod_ativo}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao extrair dados da página para ativo {cod_ativo}: {e}")
            return None
    
    def _parse_boolean(self, value: str) -> Optional[bool]:
        """
        Converte string para boolean
        
        Args:
            value: String a ser convertida
            
        Returns:
            Boolean ou None se não conseguir converter
        """
        if not value:
            return None
            
        value_lower = value.lower().strip()
        if value_lower in ['sim', 'yes', 'true', '1', 's']:
            return True
        elif value_lower in ['não', 'nao', 'no', 'false', '0', 'n']:
            return False
        else:
            return None
    
    def enrich_multiple_ativos(self, cod_ativos: list[str], delay: float = 1.0) -> Dict[str, Dict[str, Any]]:
        """
        Enriquece múltiplos ativos com delay entre requisições
        
        Args:
            cod_ativos: Lista de códigos de ativos
            delay: Delay em segundos entre requisições
            
        Returns:
            Dict com códigos de ativos como chaves e dados como valores
        """
        resultados = {}
        
        for i, cod_ativo in enumerate(cod_ativos):
            logger.info(f"Enriquecendo ativo {i+1}/{len(cod_ativos)}: {cod_ativo}")
            
            resultado = self.enrich_ativo(cod_ativo)
            resultados[cod_ativo] = resultado
            
            # Delay entre requisições para não sobrecarregar o servidor
            if i < len(cod_ativos) - 1:
                time.sleep(delay)
        
        return resultados
