#!/usr/bin/env python3
"""
Script de teste para o sistema de enriquecimento ANBIMA
"""

import asyncio
import sys
import os

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.anbima_enrichment import AnbimaEnrichmentService

async def test_anbima_enrichment():
    """Testa o serviço de enriquecimento da ANBIMA"""
    print("🧪 Testando serviço de enriquecimento ANBIMA...")
    
    service = AnbimaEnrichmentService()
    
    # Teste com um código de ativo fictício
    test_cod_ativo = "CRA02300FFL"  # Exemplo de código CRA
    
    print(f"📡 Testando enriquecimento para ativo: {test_cod_ativo}")
    
    try:
        resultado = service.enrich_ativo(test_cod_ativo)
        
        if resultado:
            print("✅ Dados obtidos com sucesso!")
            print(f"📊 Resultado: {resultado}")
        else:
            print("⚠️  Nenhum dado encontrado (pode ser normal se o ativo não existir na ANBIMA)")
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
    
    print("\n🔍 Testando múltiplos ativos...")
    
    # Teste com múltiplos ativos
    cod_ativos_teste = ["CRA02300FFL", "CRA02400FFL", "CRA02500FFL"]
    
    try:
        resultados = service.enrich_multiple_ativos(cod_ativos_teste, delay=0.5)
        
        print(f"📈 Resultados para {len(cod_ativos_teste)} ativos:")
        for cod_ativo, resultado in resultados.items():
            status = "✅" if resultado and not resultado.get('erro') else "❌"
            print(f"  {status} {cod_ativo}: {resultado}")
            
    except Exception as e:
        print(f"❌ Erro durante teste múltiplo: {e}")

def test_imports():
    """Testa se todos os módulos podem ser importados"""
    print("🔧 Testando imports...")
    
    try:
        from app.models.ativo_enriquecido import AtivoEnriquecido
        from app.DTOs.ativo_enriquecido import AtivoEnriquecidoDTO
        from app.services.enrichment_service import EnrichmentService
        from app.controllers.enrichment import enrichment_routes
        from app.schemas.enrichment import EnrichmentStatusResponse
        
        print("✅ Todos os módulos importados com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao importar módulos: {e}")
        return False

async def main():
    """Função principal de teste"""
    print("🚀 Iniciando testes do sistema de enriquecimento ANBIMA")
    print("=" * 60)
    
    # Teste 1: Imports
    if not test_imports():
        print("❌ Falha nos imports. Verifique as dependências.")
        return
    
    print("\n" + "=" * 60)
    
    # Teste 2: Serviço ANBIMA
    await test_anbima_enrichment()
    
    print("\n" + "=" * 60)
    print("✅ Testes concluídos!")
    print("\n📋 Próximos passos:")
    print("1. Execute a migração: poetry run alembic upgrade head")
    print("2. Inicie o servidor: poetry run python main.py")
    print("3. Acesse o frontend e teste o toggle de dados enriquecidos")

if __name__ == "__main__":
    asyncio.run(main())

