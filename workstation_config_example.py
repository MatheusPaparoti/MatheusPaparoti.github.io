#!/usr/bin/env python3
"""
Exemplo de uso do script de automação com arquivo de configuração
"""

import json
import os
from workstation_automation import WorkstationAutomation

def load_config(config_file: str = "config.json") -> dict:
    """Carrega configurações do arquivo JSON"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Arquivo de configuração '{config_file}' não encontrado!")
        return None
    except json.JSONDecodeError:
        print(f"❌ Erro ao decodificar o arquivo '{config_file}'. Verifique a sintaxe JSON.")
        return None

def main():
    """Função principal usando configuração"""
    
    # Carregar configurações
    config = load_config()
    if not config:
        return
    
    # Extrair configurações da API
    api_config = config.get("api", {})
    base_url = api_config.get("base_url")
    caller_id = api_config.get("caller_id", "123")
    
    if not base_url:
        print("❌ URL base da API não configurada!")
        return
    
    # Inicializar automação
    automation = WorkstationAutomation(base_url, caller_id)
    
    # Obter lista de workstations da configuração
    workstations = config.get("workstations", [])
    
    if not workstations:
        print("⚠️ Nenhuma workstation configurada!")
        return
    
    print(f"📋 Processando {len(workstations)} workstations da configuração...")
    print("=" * 60)
    
    # Criar workstations em lote
    result = automation.create_multiple_workstations(workstations)
    
    # Exibir resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DA EXECUÇÃO")
    print("=" * 60)
    print(f"Total de workstations: {result['total']}")
    print(f"✅ Criadas com sucesso: {result['success_count']}")
    print(f"❌ Erros: {result['error_count']}")
    
    # Exibir detalhes dos erros, se houver
    if result['error_count'] > 0:
        print("\n🔍 DETALHES DOS ERROS:")
        print("-" * 40)
        for item in result['results']:
            if not item['result']['success']:
                ws = item['workstation']
                error = item['result']
                print(f"❌ {ws['warehouse_id']} - {ws['description']}")
                print(f"   Erro: {error.get('error', 'Desconhecido')}")
                print(f"   Mensagem: {error.get('message', 'N/A')}")
                print()

if __name__ == "__main__":
    main()