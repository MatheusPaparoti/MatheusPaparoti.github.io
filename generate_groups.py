#!/usr/bin/env python3
"""
Script para gerar automaticamente arquivos de grupos de workstation
baseado na configuração e tipos comuns
"""

import json
import argparse
from typing import List, Dict


def load_config(config_file: str = "config.json") -> Dict:
    """Carrega o arquivo de configuração"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Arquivo de configuração não encontrado: {config_file}")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao decodificar configuração: {e}")
        return {}


def generate_groups_for_warehouse(warehouse_id: str, group_types: List[Dict], 
                                start_code: int = 1) -> List[Dict]:
    """Gera grupos para um warehouse específico"""
    groups = []
    
    for i, group_type in enumerate(group_types):
        groups.append({
            "warehouse_id": warehouse_id,
            "code": start_code + i,
            "description": group_type["description"]
        })
    
    return groups


def generate_all_groups(config: Dict, output_file: str = None) -> List[Dict]:
    """Gera todos os grupos baseado na configuração"""
    all_groups = []
    
    warehouses = config.get("default_warehouses", [])
    group_types = config.get("common_group_types", [])
    
    if not warehouses:
        print("⚠️  Nenhum warehouse configurado")
        return []
    
    if not group_types:
        print("⚠️  Nenhum tipo de grupo configurado")
        return []
    
    print(f"🏭 Gerando grupos para {len(warehouses)} warehouses...")
    print(f"📋 Usando {len(group_types)} tipos de grupos")
    
    for warehouse in warehouses:
        print(f"  - {warehouse}: {len(group_types)} grupos")
        warehouse_groups = generate_groups_for_warehouse(warehouse, group_types)
        all_groups.extend(warehouse_groups)
    
    print(f"✅ Total de {len(all_groups)} grupos gerados")
    
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_groups, f, indent=2, ensure_ascii=False)
            print(f"💾 Grupos salvos em: {output_file}")
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo: {e}")
    
    return all_groups


def generate_warehouse_specific_groups(config: Dict, warehouse_id: str, 
                                     output_file: str = None) -> List[Dict]:
    """Gera grupos para um warehouse específico"""
    group_types = config.get("common_group_types", [])
    
    if not group_types:
        print("⚠️  Nenhum tipo de grupo configurado")
        return []
    
    print(f"🏭 Gerando grupos para warehouse: {warehouse_id}")
    print(f"📋 Usando {len(group_types)} tipos de grupos")
    
    groups = generate_groups_for_warehouse(warehouse_id, group_types)
    
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(groups, f, indent=2, ensure_ascii=False)
            print(f"💾 Grupos salvos em: {output_file}")
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo: {e}")
    
    return groups


def generate_custom_groups(warehouse_id: str, descriptions: List[str], 
                          start_code: int = 1, output_file: str = None) -> List[Dict]:
    """Gera grupos customizados"""
    groups = []
    
    print(f"🏭 Gerando {len(descriptions)} grupos customizados para {warehouse_id}")
    
    for i, description in enumerate(descriptions):
        groups.append({
            "warehouse_id": warehouse_id,
            "code": start_code + i,
            "description": description
        })
    
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(groups, f, indent=2, ensure_ascii=False)
            print(f"💾 Grupos salvos em: {output_file}")
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo: {e}")
    
    return groups


def show_config_summary(config: Dict):
    """Mostra um resumo da configuração"""
    print("📋 RESUMO DA CONFIGURAÇÃO")
    print("=" * 40)
    
    # APIs configuradas
    api_configs = config.get("api_configs", {})
    print(f"🌐 APIs configuradas: {len(api_configs)}")
    for env, api_config in api_configs.items():
        print(f"  - {env}: {api_config['base_url']} (ID: {api_config['caller_id']})")
    
    # Warehouses
    warehouses = config.get("default_warehouses", [])
    print(f"\n🏭 Warehouses padrão: {len(warehouses)}")
    for warehouse in warehouses:
        print(f"  - {warehouse}")
    
    # Tipos de grupos
    group_types = config.get("common_group_types", [])
    print(f"\n📋 Tipos de grupos: {len(group_types)}")
    for group_type in group_types:
        print(f"  - {group_type['code']}: {group_type['description']} ({group_type['description_pt']})")
    
    # Configurações de validação
    validation = config.get("validation", {})
    print(f"\n✅ Validações:")
    print(f"  - Código: {validation.get('min_code_value', 1)} a {validation.get('max_code_value', 999)}")
    print(f"  - Descrição: máx {validation.get('max_description_length', 50)} chars")
    print(f"  - Warehouse ID: máx {validation.get('max_warehouse_id_length', 10)} chars")


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="Gerador automático de grupos de workstation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  # Gerar todos os grupos baseado na configuração
  python generate_groups.py --all --output "all_groups.json"
  
  # Gerar grupos para um warehouse específico
  python generate_groups.py --warehouse "BRTW01" --output "brtw01_groups.json"
  
  # Gerar grupos customizados
  python generate_groups.py --warehouse "BRTW01" --descriptions "PACKING,PICKING,RECEIVING" --output "custom_groups.json"
  
  # Mostrar resumo da configuração
  python generate_groups.py --show-config
        """
    )
    
    parser.add_argument('--config', default='config.json', help='Arquivo de configuração')
    parser.add_argument('--all', action='store_true', help='Gerar todos os grupos')
    parser.add_argument('--warehouse', help='Warehouse específico')
    parser.add_argument('--descriptions', help='Lista de descrições separadas por vírgula')
    parser.add_argument('--start-code', type=int, default=1, help='Código inicial (padrão: 1)')
    parser.add_argument('--output', help='Arquivo de saída')
    parser.add_argument('--show-config', action='store_true', help='Mostrar resumo da configuração')
    
    args = parser.parse_args()
    
    # Carregar configuração
    config = load_config(args.config)
    if not config:
        return
    
    # Mostrar configuração se solicitado
    if args.show_config:
        show_config_summary(config)
        return
    
    # Gerar grupos baseado nos argumentos
    if args.all:
        generate_all_groups(config, args.output)
    elif args.warehouse and args.descriptions:
        descriptions = [d.strip() for d in args.descriptions.split(',')]
        generate_custom_groups(args.warehouse, descriptions, args.start_code, args.output)
    elif args.warehouse:
        generate_warehouse_specific_groups(config, args.warehouse, args.output)
    else:
        print("❌ Especifique uma opção: --all, --warehouse, ou --warehouse + --descriptions")
        print("Use --help para ver as opções disponíveis")


if __name__ == "__main__":
    main()