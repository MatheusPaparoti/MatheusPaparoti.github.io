# 📋 Instruções de Uso - Sistema de Automação de Workstations

## 🎯 Visão Geral

Este sistema automatiza a criação de grupos de workstation seguindo exatamente a documentação da API `fbm-wms-workstation-api`. O sistema foi projetado para ser fácil de usar, robusto e flexível.

## 🚀 Início Rápido

### 1. Verificar o ambiente
```bash
# Verificar se o Python está instalado
python3 --version

# Executar demonstração
./demo_workstation.sh
```

### 2. Criar grupos de exemplo
```bash
# Gerar todos os grupos baseado na configuração
python3 generate_groups.py --all --output "meus_grupos.json"

# Gerar grupos para um warehouse específico
python3 generate_groups.py --warehouse "BRTW01" --output "brtw01_groups.json"
```

### 3. Criar workstations na API
```bash
# Criar um grupo individual
python3 workstation_automation_simple.py \
  --url "https://sua-api.com" \
  --warehouse "BRTW01" \
  --code 1 \
  --description "PACKING"

# Criar múltiplos grupos de um arquivo
python3 workstation_automation_simple.py \
  --url "https://sua-api.com" \
  --file "meus_grupos.json"
```

## 📁 Arquivos do Sistema

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| `workstation_automation_simple.py` | Script principal de automação | Criação de workstations via API |
| `generate_groups.py` | Gerador de arquivos de grupos | Criação automática de configurações |
| `config.json` | Configuração do sistema | APIs, warehouses e tipos de grupos |
| `demo_workstation.sh` | Script de demonstração | Tutorial interativo |
| `example_groups.json` | Exemplo de grupos | Referência de formato |
| `requirements.txt` | Dependências Python | Instalação (versão completa) |

## 🔧 Configuração

### Arquivo de Configuração (`config.json`)

O sistema usa um arquivo de configuração central que define:

- **APIs**: URLs e IDs de chamador para diferentes ambientes
- **Warehouses**: Lista de warehouses disponíveis
- **Tipos de Grupos**: Códigos e descrições padrão
- **Validações**: Regras de validação de dados
- **Rate Limiting**: Controle de velocidade das requisições

### Personalizar Configuração

1. **Editar `config.json`**:
   ```json
   {
     "api_configs": {
       "production": {
         "base_url": "https://sua-api-producao.com",
         "caller_id": "seu_id_aqui"
       }
     }
   }
   ```

2. **Adicionar novos warehouses**:
   ```json
   "default_warehouses": [
     "BRTW01",
     "BRTW02",
     "BRTW03",
     "SEU_WAREHOUSE"
   ]
   ```

3. **Criar tipos de grupos personalizados**:
   ```json
   "common_group_types": [
     {
       "code": 1,
       "description": "SEU_TIPO",
       "description_pt": "SUA_DESCRIÇÃO"
     }
   ]
   ```

## 📊 Estrutura da API

### Endpoint
```
POST /wms/workstation/group?caller.id={id}
```

### Payload de Requisição
```json
{
  "warehouse_id": "BRTW01",
  "code": 1,
  "description": "PACKING"
}
```

### Resposta de Sucesso (200 OK)
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

## 🛠️ Casos de Uso

### 1. Criação Individual de Grupos
```bash
# Para criar um grupo específico
python3 workstation_automation_simple.py \
  --url "https://api.exemplo.com" \
  --warehouse "BRTW01" \
  --code 1 \
  --description "PACKING"
```

**Quando usar**: Criação pontual de grupos, testes, correções.

### 2. Criação em Lote
```bash
# Gerar arquivo de grupos
python3 generate_groups.py --all --output "grupos_completos.json"

# Criar todos os grupos via API
python3 workstation_automation_simple.py \
  --url "https://api.exemplo.com" \
  --file "grupos_completos.json"
```

**Quando usar**: Setup inicial de warehouses, migração de dados, criação de novos ambientes.

### 3. Criação para Warehouse Específico
```bash
# Gerar grupos para um warehouse
python3 generate_groups.py \
  --warehouse "BRTW01" \
  --output "brtw01_groups.json"

# Criar grupos na API
python3 workstation_automation_simple.py \
  --url "https://api.exemplo.com" \
  --file "brtw01_groups.json"
```

**Quando usar**: Expansão de warehouses existentes, adição de novos tipos de grupos.

### 4. Grupos Customizados
```bash
# Criar grupos com descrições específicas
python3 generate_groups.py \
  --warehouse "BRTW01" \
  --descriptions "PACKING,PICKING,RECEIVING,SHIPPING" \
  --output "grupos_customizados.json"
```

**Quando usar**: Workflows específicos, integração com sistemas externos.

## 🔍 Monitoramento e Debugging

### Logs em Tempo Real
O sistema fornece feedback detalhado:
- ✅ Progresso de criação
- 📊 Status de cada requisição
- ❌ Detalhes de erros
- 📈 Resumo final com estatísticas

### Tratamento de Erros
- **400 Bad Request**: Validação de parâmetros
- **500 Internal Server Error**: Erro no servidor
- **Erros de rede**: Timeouts, conexões recusadas
- **Validação de dados**: Campos obrigatórios e tipos

### Rate Limiting
- Aguarda 2 segundos entre requisições
- Evita sobrecarga da API
- Configurável via `config.json`

## 🚨 Solução de Problemas

### Problema: "URL da API é obrigatória"
**Solução**: Use o parâmetro `--url` para especificar a URL da API.

### Problema: "Campo obrigatório ausente"
**Solução**: Verifique se todos os campos estão presentes no arquivo JSON.

### Problema: "Erro na requisição"
**Solução**: 
1. Verifique se a URL está correta
2. Confirme se a API está acessível
3. Verifique se o `caller.id` é válido

### Problema: "Status code inesperado"
**Solução**: 
1. Verifique os logs para detalhes do erro
2. Confirme se o payload está correto
3. Verifique se a API está funcionando

## 📈 Melhores Práticas

### 1. Organização de Arquivos
```
projeto/
├── config.json              # Configuração central
├── grupos/                  # Pasta para arquivos de grupos
│   ├── brtw01_groups.json
│   ├── brtw02_groups.json
│   └── all_groups.json
├── logs/                    # Pasta para logs (se necessário)
└── scripts/                 # Scripts de automação
```

### 2. Nomenclatura
- Use códigos sequenciais (1, 2, 3...)
- Descrições claras e consistentes
- Warehouse IDs padronizados

### 3. Validação
- Sempre valide dados antes de enviar
- Use o sistema de validação automática
- Teste com pequenos conjuntos primeiro

### 4. Backup
- Mantenha backups dos arquivos de configuração
- Documente mudanças na configuração
- Use controle de versão para arquivos importantes

## 🔄 Automação Avançada

### Scripts de Cron
```bash
# Executar criação automática diária
0 2 * * * /usr/bin/python3 /caminho/para/workstation_automation_simple.py \
  --url "https://api.exemplo.com" \
  --file "/caminho/para/grupos.json"
```

### Integração com CI/CD
```yaml
# Exemplo para GitHub Actions
- name: Criar Workstations
  run: |
    python3 generate_groups.py --all --output "grupos.json"
    python3 workstation_automation_simple.py \
      --url "${{ secrets.API_URL }}" \
      --file "grupos.json"
```

### Monitoramento
- Logs estruturados para análise
- Métricas de sucesso/falha
- Alertas para erros críticos

## 📞 Suporte

### Recursos Disponíveis
- ✅ Documentação completa no README.md
- ✅ Script de demonstração interativo
- ✅ Exemplos práticos
- ✅ Validação automática de dados
- ✅ Tratamento robusto de erros

### Para Ajuda
1. Execute `./demo_workstation.sh` para tutorial
2. Use `--help` em qualquer script
3. Consulte o README.md
4. Verifique os logs de erro

---

**✨ Sistema pronto para uso em produção!**

Este sistema foi projetado seguindo as melhores práticas de automação e pode ser usado com confiança para gerenciar workstations em ambientes de produção.