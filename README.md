# Script de Automação para Criação de Workstations

Este projeto automatiza o processo de criação de grupos de workstation conforme especificado na documentação do sistema WMS.

## Funcionalidades

- ✅ Criação automatizada de grupos de workstation via API
- ✅ Suporte para criação individual ou em lote
- ✅ Tratamento completo de códigos de resposta HTTP (200, 400, 500)
- ✅ Sistema de logging detalhado
- ✅ Configuração via arquivo JSON
- ✅ Relatórios de execução com estatísticas

## Estrutura do Projeto

```
/
├── workstation_automation.py      # Script principal
├── workstation_config_example.py  # Exemplo usando configuração
├── config.json                    # Arquivo de configuração
├── requirements.txt               # Dependências Python
└── README.md                      # Esta documentação
```

## Instalação

1. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

2. **Configurar a API:**
   - Edite o arquivo `config.json`
   - Substitua `"https://your-api-domain.com"` pela URL real da sua API
   - Ajuste o `caller_id` se necessário

## Configuração

### Arquivo config.json

```json
{
  "api": {
    "base_url": "https://your-api-domain.com",
    "caller_id": "123",
    "timeout": 30
  },
  "logging": {
    "level": "INFO",
    "file": "workstation_automation.log"
  },
  "workstations": [
    {
      "warehouse_id": "MKTM01",
      "code": 1,
      "description": "PACKING"
    }
  ]
}
```

### Parâmetros da API

Baseado na documentação fornecida:

- **Endpoint:** `/wms/workstation/group?caller_id=123`
- **Método:** POST
- **Content-Type:** application/json

**Payload:**
```json
{
  "warehouse_id": "MKTM01",
  "code": 1,
  "description": "PACKING"
}
```

**Códigos de Resposta:**
- `200 OK`: Workstation criada com sucesso
- `400 Bad Request`: Dados inválidos na requisição
- `500 Internal Server Error`: Erro interno do servidor

## Uso

### 1. Uso Básico (Script Principal)

```python
from workstation_automation import WorkstationAutomation

# Inicializar
automation = WorkstationAutomation("https://your-api.com", "123")

# Criar uma workstation
result = automation.create_workstation_group(
    warehouse_id="MKTM01",
    code=1,
    description="PACKING"
)

print(result)
```

### 2. Execução via Linha de Comando

```bash
# Usando o script principal
python workstation_automation.py

# Usando configuração
python workstation_config_example.py
```

### 3. Criação em Lote

```python
workstations = [
    {"warehouse_id": "MKTM01", "code": 1, "description": "PACKING"},
    {"warehouse_id": "MKTM01", "code": 2, "description": "PICKING"},
    {"warehouse_id": "MKTM02", "code": 1, "description": "SHIPPING"}
]

result = automation.create_multiple_workstations(workstations)
```

## Exemplos de Resposta

### Sucesso (200)
```json
{
  "success": true,
  "status_code": 200,
  "data": {
    "warehouse_id": "MKTM01",
    "code": 1,
    "description": "PACKING",
    "status": "ACTIVE",
    "created_by": "123",
    "last_updated_by": "123"
  }
}
```

### Erro (400/500)
```json
{
  "success": false,
  "status_code": 400,
  "error": "Bad Request",
  "message": "Verifique os dados enviados na requisição"
}
```

## Logging

O sistema gera logs detalhados em dois locais:
- **Console:** Para acompanhamento em tempo real
- **Arquivo:** `workstation_automation.log`

Exemplo de log:
```
2024-01-15 10:30:15 - INFO - Criando grupo de workstation: MKTM01 - PACKING
2024-01-15 10:30:16 - INFO - Status Code: 200
2024-01-15 10:30:16 - INFO - ✅ Grupo de workstation criado com sucesso!
```

## Tratamento de Erros

O script trata automaticamente:

- **Erros de Conectividade:** Timeout, DNS, etc.
- **Códigos HTTP:** 400 (Bad Request), 500 (Internal Server Error)
- **Erros de Configuração:** Arquivo não encontrado, JSON inválido
- **Validação de Dados:** Parâmetros obrigatórios

## Personalização

### Adicionando Novos Campos

Para adicionar novos campos ao payload, edite a função `create_workstation_group`:

```python
payload = {
    "warehouse_id": warehouse_id,
    "code": code,
    "description": description,
    "novo_campo": valor  # Adicione aqui
}
```

### Configurando Timeout

Ajuste o timeout nas requisições:

```python
response = self.session.post(
    endpoint,
    params=params,
    json=payload,
    headers={"Content-Type": "application/json"},
    timeout=30  # Timeout em segundos
)
```

## Monitoramento

### Estatísticas de Execução

O script fornece relatórios detalhados:
- Total de workstations processadas
- Número de sucessos
- Número de erros
- Detalhes específicos de cada erro

### Logs de Auditoria

Todos os logs incluem timestamps e são mantidos para auditoria:
- Tentativas de criação
- Respostas da API
- Erros e exceções

## Contribuição

Para contribuir com melhorias:

1. Faça fork do projeto
2. Crie uma branch para sua feature
3. Implemente as mudanças
4. Adicione testes se necessário
5. Submeta um pull request

## Suporte

Para dúvidas ou problemas:
- Verifique os logs em `workstation_automation.log`
- Confirme a configuração da API
- Teste a conectividade com o endpoint

## Licença

Este projeto é fornecido como está, para uso interno conforme especificações do sistema WMS.