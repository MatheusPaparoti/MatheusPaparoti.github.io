#!/usr/bin/env python3
"""
Script para automatizar criação de workstations
Baseado na documentação da API fbm-wms-workstation-api
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import argparse
import sys


class WorkstationAutomation:
    """Classe para automatizar operações de workstation"""
    
    def __init__(self, base_url: str, caller_id: str = "123"):
        """
        Inicializa a classe de automação
        
        Args:
            base_url: URL base da API
            caller_id: ID do chamador para a API
        """
        self.base_url = base_url.rstrip('/')
        self.caller_id = caller_id
        self.session = requests.Session()
        
        # Configurar headers padrão
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def create_workstation_group(self, warehouse_id: str, code: int, description: str) -> Dict:
        """
        Cria um grupo de workstation seguindo a documentação da API
        
        Args:
            warehouse_id: ID do warehouse (ex: "BRTW01")
            code: Código numérico do grupo
            description: Descrição do grupo (ex: "PACKING")
            
        Returns:
            Dict com a resposta da API
        """
        endpoint = f"{self.base_url}/wms/workstation/group"
        params = {'caller.id': self.caller_id}
        
        payload = {
            "warehouse_id": warehouse_id,
            "code": code,
            "description": description
        }
        
        try:
            print(f"Criando grupo de workstation: {description}")
            print(f"Endpoint: {endpoint}")
            print(f"Payload: {json.dumps(payload, indent=2)}")
            
            response = self.session.post(endpoint, params=params, json=payload)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Grupo criado com sucesso!")
                print(f"Resposta: {json.dumps(result, indent=2)}")
                return result
            elif response.status_code == 400:
                print("❌ Bad Request - Verifique os parâmetros enviados")
                print(f"Erro: {response.text}")
                return {"error": "Bad Request", "details": response.text}
            elif response.status_code == 500:
                print("❌ Internal Server Error - Erro no servidor")
                print(f"Erro: {response.text}")
                return {"error": "Internal Server Error", "details": response.text}
            else:
                print(f"❌ Status code inesperado: {response.status_code}")
                print(f"Resposta: {response.text}")
                return {"error": f"Unexpected status: {response.status_code}", "details": response.text}
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na requisição: {e}")
            return {"error": "Request Exception", "details": str(e)}
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao decodificar JSON: {e}")
            return {"error": "JSON Decode Error", "details": str(e)}
    
    def create_multiple_groups(self, groups: List[Dict]) -> List[Dict]:
        """
        Cria múltiplos grupos de workstation
        
        Args:
            groups: Lista de dicionários com os dados dos grupos
            
        Returns:
            Lista com os resultados de cada criação
        """
        results = []
        
        for i, group in enumerate(groups, 1):
            print(f"\n--- Criando grupo {i}/{len(groups)} ---")
            result = self.create_workstation_group(
                warehouse_id=group['warehouse_id'],
                code=group['code'],
                description=group['description']
            )
            results.append(result)
            
            # Aguardar um pouco entre as requisições para não sobrecarregar a API
            if i < len(groups):
                print("Aguardando 2 segundos antes da próxima requisição...")
                time.sleep(2)
        
        return results
    
    def validate_group_data(self, group: Dict) -> bool:
        """
        Valida os dados do grupo antes de enviar para a API
        
        Args:
            group: Dicionário com os dados do grupo
            
        Returns:
            True se os dados são válidos, False caso contrário
        """
        required_fields = ['warehouse_id', 'code', 'description']
        
        for field in required_fields:
            if field not in group:
                print(f"❌ Campo obrigatório ausente: {field}")
                return False
        
        if not isinstance(group['warehouse_id'], str) or not group['warehouse_id']:
            print("❌ warehouse_id deve ser uma string não vazia")
            return False
        
        if not isinstance(group['code'], int) or group['code'] <= 0:
            print("❌ code deve ser um número inteiro positivo")
            return False
        
        if not isinstance(group['description'], str) or not group['description']:
            print("❌ description deve ser uma string não vazia")
            return False
        
        return True


def load_groups_from_file(filename: str) -> List[Dict]:
    """
    Carrega grupos de workstation de um arquivo JSON
    
    Args:
        filename: Nome do arquivo JSON
        
    Returns:
        Lista de grupos
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if not isinstance(data, list):
            raise ValueError("O arquivo deve conter uma lista de grupos")
            
        return data
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {filename}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao decodificar JSON: {e}")
        return []
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return []


def create_sample_groups_file(filename: str = "sample_groups.json"):
    """
    Cria um arquivo de exemplo com grupos de workstation
    
    Args:
        filename: Nome do arquivo a ser criado
    """
    sample_groups = [
        {
            "warehouse_id": "BRTW01",
            "code": 1,
            "description": "PACKING"
        },
        {
            "warehouse_id": "BRTW01",
            "code": 2,
            "description": "PICKING"
        },
        {
            "warehouse_id": "BRTW01",
            "code": 3,
            "description": "RECEIVING"
        },
        {
            "warehouse_id": "BRTW02",
            "code": 1,
            "description": "PACKING"
        }
    ]
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(sample_groups, f, indent=2, ensure_ascii=False)
        print(f"✅ Arquivo de exemplo criado: {filename}")
    except Exception as e:
        print(f"❌ Erro ao criar arquivo de exemplo: {e}")


def main():
    """Função principal do script"""
    parser = argparse.ArgumentParser(
        description="Script para automatizar criação de workstations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  # Criar um grupo específico
  python workstation_automation.py --url "https://api.example.com" --warehouse "BRTW01" --code 1 --description "PACKING"
  
  # Criar múltiplos grupos de um arquivo
  python workstation_automation.py --url "https://api.example.com" --file "groups.json"
  
  # Criar arquivo de exemplo
  python workstation_automation.py --create-sample
  
  # Usar ID de chamador personalizado
  python workstation_automation.py --url "https://api.example.com" --caller-id "456" --file "groups.json"
        """
    )
    
    parser.add_argument('--url', help='URL base da API')
    parser.add_argument('--caller-id', default='123', help='ID do chamador (padrão: 123)')
    parser.add_argument('--warehouse', help='ID do warehouse')
    parser.add_argument('--code', type=int, help='Código do grupo')
    parser.add_argument('--description', help='Descrição do grupo')
    parser.add_argument('--file', help='Arquivo JSON com múltiplos grupos')
    parser.add_argument('--create-sample', action='store_true', help='Criar arquivo de exemplo')
    
    args = parser.parse_args()
    
    # Criar arquivo de exemplo se solicitado
    if args.create_sample:
        create_sample_groups_file()
        return
    
    # Verificar se foi fornecida uma URL
    if not args.url:
        print("❌ URL da API é obrigatória. Use --url para especificar.")
        print("Use --help para ver as opções disponíveis.")
        return
    
    # Inicializar automação
    automation = WorkstationAutomation(args.url, args.caller_id)
    
    # Criar um grupo específico
    if args.warehouse and args.code and args.description:
        group = {
            'warehouse_id': args.warehouse,
            'code': args.code,
            'description': args.description
        }
        
        if automation.validate_group_data(group):
            automation.create_workstation_group(
                warehouse_id=group['warehouse_id'],
                code=group['code'],
                description=group['description']
            )
        else:
            print("❌ Dados do grupo inválidos")
            sys.exit(1)
    
    # Criar múltiplos grupos de um arquivo
    elif args.file:
        groups = load_groups_from_file(args.file)
        
        if not groups:
            print("❌ Nenhum grupo válido encontrado no arquivo")
            sys.exit(1)
        
        print(f"📁 Carregados {len(groups)} grupos do arquivo: {args.file}")
        
        # Validar todos os grupos antes de enviar
        valid_groups = []
        for group in groups:
            if automation.validate_group_data(group):
                valid_groups.append(group)
            else:
                print(f"⚠️  Grupo ignorado devido a dados inválidos: {group}")
        
        if not valid_groups:
            print("❌ Nenhum grupo válido encontrado")
            sys.exit(1)
        
        print(f"✅ {len(valid_groups)} grupos válidos encontrados")
        
        # Criar os grupos
        results = automation.create_multiple_groups(valid_groups)
        
        # Resumo dos resultados
        print("\n" + "="*50)
        print("RESUMO DOS RESULTADOS")
        print("="*50)
        
        successful = sum(1 for r in results if 'error' not in r)
        failed = len(results) - successful
        
        print(f"✅ Grupos criados com sucesso: {successful}")
        print(f"❌ Falhas: {failed}")
        
        if failed > 0:
            print("\nDetalhes das falhas:")
            for i, result in enumerate(results):
                if 'error' in result:
                    print(f"  Grupo {i+1}: {result['error']} - {result.get('details', 'N/A')}")
    
    else:
        print("❌ Especifique um grupo individual (--warehouse, --code, --description) ou um arquivo (--file)")
        print("Use --help para ver as opções disponíveis.")


if __name__ == "__main__":
    main()