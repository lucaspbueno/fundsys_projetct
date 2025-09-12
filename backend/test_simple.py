#!/usr/bin/env python3
"""
Teste simples do serviço de enriquecimento ANBIMA
"""

import requests
from bs4 import BeautifulSoup

def test_anbima_connection():
    """Testa a conexão com a ANBIMA"""
    print("🧪 Testando conexão com ANBIMA...")
    
    # URL de teste
    test_url = "https://data.anbima.com.br/certificado-de-recebiveis/CRA02300FFL/caracteristicas"
    
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        print(f"📡 Fazendo requisição para: {test_url}")
        response = session.get(test_url, timeout=30)
        
        print(f"📊 Status da resposta: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Conexão estabelecida com sucesso!")
            
            # Testar parsing
            soup = BeautifulSoup(response.content, 'html.parser')
            print(f"📄 Tamanho do HTML: {len(response.content)} bytes")
            print(f"🔍 Título da página: {soup.title.string if soup.title else 'N/A'}")
            
            # Procurar por tabelas
            tables = soup.find_all('table')
            print(f"📋 Tabelas encontradas: {len(tables)}")
            
            # Procurar por divs com informações
            divs = soup.find_all('div')
            print(f"📦 Divs encontradas: {len(divs)}")
            
            return True
        else:
            print(f"❌ Erro na requisição: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_imports():
    """Testa imports básicos"""
    print("🔧 Testando imports básicos...")
    
    try:
        import requests
        import bs4
        print("✅ requests e beautifulsoup4 importados com sucesso!")
        return True
    except ImportError as e:
        print(f"❌ Erro ao importar: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Teste do Sistema de Enriquecimento ANBIMA")
    print("=" * 50)
    
    # Teste 1: Imports
    if not test_imports():
        print("❌ Falha nos imports básicos")
        return
    
    print("\n" + "=" * 50)
    
    # Teste 2: Conexão ANBIMA
    if test_anbima_connection():
        print("\n✅ Sistema de enriquecimento está funcionando!")
        print("\n📋 Para usar o sistema completo:")
        print("1. Configure as variáveis de ambiente do banco")
        print("2. Execute: poetry run alembic upgrade head")
        print("3. Execute: poetry run python main.py")
    else:
        print("\n❌ Problemas na conexão com ANBIMA")
        print("💡 Verifique sua conexão com a internet")

if __name__ == "__main__":
    main()

