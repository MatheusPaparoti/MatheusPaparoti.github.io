# Script de Automação de Workstations

Este script automatiza a criação de grupos de workstation seguindo a documentação da API `fbm-wms-workstation-api`.

## 📋 Pré-requisitos

- Python 3.7 ou superior
- Biblioteca `requests` instalada

## 🚀 Instalação

1. Clone ou baixe os arquivos para seu diretório de trabalho
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## 📖 Como usar

### 1. Criar um grupo individual

```bash
python workstation_automation.py \
  --url "https://sua-api.com" \
  --warehouse "BRTW01" \
  --code 1 \
  --description "PACKING"
```

### 2. Criar múltiplos grupos de um arquivo JSON

Primeiro, crie um arquivo JSON com os grupos:

```json
[
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
  }
]
```

Depois execute:

```bash
python workstation_automation.py \
  --url "https://sua-api.com" \
  --file "meus_grupos.json"
```

### 3. Criar arquivo de exemplo

```bash
python workstation_automation.py --create-sample
```

Isso criará um arquivo `sample_groups.json` com exemplos de grupos.

### 4. Usar ID de chamador personalizado

```bash
python workstation_automation.py \
  --url "https://sua-api.com" \
  --caller-id "456" \
  --file "grupos.json"
```

## 🔧 Parâmetros disponíveis

| Parâmetro | Descrição | Obrigatório | Padrão |
|-----------|-----------|-------------|---------|
| `--url` | URL base da API | ✅ | - |
| `--caller-id` | ID do chamador | ❌ | "123" |
| `--warehouse` | ID do warehouse | ❌* | - |
| `--code` | Código do grupo | ❌* | - |
| `--description` | Descrição do grupo | ❌* | - |
| `--file` | Arquivo JSON com grupos | ❌* | - |
| `--create-sample` | Criar arquivo de exemplo | ❌ | - |

*Pelo menos um dos grupos de parâmetros deve ser fornecido: individual (`--warehouse`, `--code`, `--description`) ou em lote (`--file`)

## 📊 Estrutura da API

O script segue exatamente a documentação da API:

- **Endpoint**: `/wms/workstation/group`
- **Método**: `POST`
- **Parâmetros de query**: `caller.id`
- **Headers**: `Content-Type: application/json`

### Payload de requisição

```json
{
  "warehouse_id": "BRTW01",
  "code": 1,
  "description": "PACKING"
}
```

### Resposta de sucesso (200 OK)

```json
{
  "warehouse_id": "BRTW01",
  "code": 1,
  "description": "PACKING",
  "status": "ACTIVE",
  "created_by": 1212,
  "created_at": "2025-01-23T12:18:44.964346-03:00",
  "last_updated_by": 1212,
  "last_updated_at": "2025-01-23T12:17:32.010934-03:00"
}
```

## 🛡️ Validações

O script valida automaticamente:

- ✅ Campos obrigatórios presentes
- ✅ Tipos de dados corretos
- ✅ Valores válidos (código positivo, strings não vazias)
- ✅ Respostas da API (200, 400, 500)

## 📝 Exemplos práticos

### Exemplo 1: Criação em lote para múltiplos warehouses

```json
[
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
    "warehouse_id": "BRTW02",
    "code": 1,
    "description": "PACKING"
  },
  {
    "warehouse_id": "BRTW02",
    "code": 2,
    "description": "PICKING"
  }
]
```

### Exemplo 2: Grupos especializados

```json
[
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
    "warehouse_id": "BRTW01",
    "code": 4,
    "description": "SHIPPING"
  },
  {
    "warehouse_id": "BRTW01",
    "code": 5,
    "description": "INVENTORY"
  }
]
```

## 🚨 Tratamento de erros

O script trata automaticamente:

- **400 Bad Request**: Parâmetros inválidos
- **500 Internal Server Error**: Erro no servidor
- **Erros de rede**: Timeouts, conexões recusadas
- **Erros de JSON**: Respostas malformadas
- **Validação de dados**: Campos obrigatórios ausentes

## 📈 Monitoramento

O script fornece feedback em tempo real:

- ✅ Progresso de criação
- ✅ Status de cada requisição
- ✅ Resumo final com sucessos e falhas
- ✅ Detalhes de erros para debugging

## 🔄 Recursos adicionais

- **Rate limiting**: Aguarda 2 segundos entre requisições
- **Sessão persistente**: Reutiliza conexões HTTP
- **Logging detalhado**: Mostra payloads e respostas
- **Validação prévia**: Verifica dados antes de enviar

## 🆘 Ajuda

Para ver todas as opções disponíveis:

```bash
python workstation_automation.py --help
```

## 📄 Licença

Este script foi criado para automatizar a criação de workstations seguindo a documentação oficial da API.