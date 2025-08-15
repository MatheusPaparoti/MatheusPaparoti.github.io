#!/usr/bin/env python3
"""
Script para automação de criação de workstations
Baseado na documentação do Grupo de Workstation
"""

import requests
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('workstation_automation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class WorkstationAutomation:
    """Classe para automatizar a criação de workstations"""
    
    def __init__(self, base_url: str, caller_id: str = "123"):
        """
        Inicializa a classe de automação
        
        Args:
            base_url: URL base da API (ex: https://api.example.com)
            caller_id: ID do caller para as requisições
        """
        self.base_url = base_url.rstrip('/')
        self.caller_id = caller_id
        self.session = requests.Session()
        
    def create_workstation_group(self, warehouse_id: str, code: int, description: str) -> Dict[str, Any]:
        """
        Cria um grupo de workstation
        
        Args:
            warehouse_id: ID do warehouse (ex: "MKTM01")
            code: Código numérico da workstation
            description: Descrição da workstation (ex: "PACKING")
            
        Returns:
            Dict com a resposta da API
        """
        endpoint = f"{self.base_url}/wms/workstation/group"
        params = {"caller_id": self.caller_id}
        
        payload = {
            "warehouse_id": warehouse_id,
            "code": code,
            "description": description
        }
        
        logger.info(f"Criando grupo de workstation: {warehouse_id} - {description}")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = self.session.post(
                endpoint,
                params=params,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            # Log da resposta
            logger.info(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                logger.info("✅ Grupo de workstation criado com sucesso!")
                response_data = response.json()
                logger.info(f"Resposta: {json.dumps(response_data, indent=2)}")
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": response_data
                }
                
            elif response.status_code == 400:
                logger.error("❌ Bad Request - Dados inválidos na requisição")
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": "Bad Request",
                    "message": "Verifique os dados enviados na requisição"
                }
                
            elif response.status_code == 500:
                logger.error("❌ Internal Server Error - Erro interno do servidor")
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": "Internal Server Error",
                    "message": "Erro interno do servidor. Tente novamente mais tarde."
                }
                
            else:
                logger.warning(f"⚠️ Status code não esperado: {response.status_code}")
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": "Unexpected Status Code",
                    "message": f"Recebido status code: {response.status_code}"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erro na requisição: {str(e)}")
            return {
                "success": False,
                "error": "Request Exception",
                "message": str(e)
            }
    
    def create_multiple_workstations(self, workstations: list) -> Dict[str, Any]:
        """
        Cria múltiplas workstations
        
        Args:
            workstations: Lista de dicionários com dados das workstations
                Formato: [{"warehouse_id": "MKTM01", "code": 1, "description": "PACKING"}, ...]
        
        Returns:
            Dict com resultado consolidado
        """
        results = []
        success_count = 0
        error_count = 0
        
        logger.info(f"Iniciando criação de {len(workstations)} workstations...")
        
        for i, workstation in enumerate(workstations, 1):
            logger.info(f"Processando workstation {i}/{len(workstations)}")
            
            result = self.create_workstation_group(
                warehouse_id=workstation["warehouse_id"],
                code=workstation["code"],
                description=workstation["description"]
            )
            
            results.append({
                "workstation": workstation,
                "result": result
            })
            
            if result["success"]:
                success_count += 1
            else:
                error_count += 1
        
        logger.info(f"Processo concluído: {success_count} sucessos, {error_count} erros")
        
        return {
            "total": len(workstations),
            "success_count": success_count,
            "error_count": error_count,
            "results": results
        }

def main():
    """Função principal - exemplo de uso"""
    
    # Configurações da API
    BASE_URL = "https://your-api-domain.com"  # Substitua pela URL real
    CALLER_ID = "123"
    
    # Inicializar automação
    automation = WorkstationAutomation(BASE_URL, CALLER_ID)
    
    # Exemplo 1: Criar uma workstation individual
    print("=== Criando workstation individual ===")
    result = automation.create_workstation_group(
        warehouse_id="MKTM01",
        code=1,
        description="PACKING"
    )
    print(f"Resultado: {result}")
    
    print("\n" + "="*50 + "\n")
    
    # Exemplo 2: Criar múltiplas workstations
    print("=== Criando múltiplas workstations ===")
    workstations_to_create = [
        {"warehouse_id": "MKTM01", "code": 1, "description": "PACKING"},
        {"warehouse_id": "MKTM01", "code": 2, "description": "PICKING"},
        {"warehouse_id": "MKTM02", "code": 1, "description": "SHIPPING"},
        {"warehouse_id": "MKTM02", "code": 2, "description": "RECEIVING"}
    ]
    
    batch_result = automation.create_multiple_workstations(workstations_to_create)
    print(f"Resultado do lote: {batch_result}")

if __name__ == "__main__":
    main()