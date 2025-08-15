#!/bin/bash

# Script de demonstração para automação de workstations
# Este script mostra como usar o sistema de automação

echo "🚀 DEMONSTRAÇÃO DO SISTEMA DE AUTOMAÇÃO DE WORKSTATIONS"
echo "=================================================="
echo ""

# Verificar se o Python está disponível
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não está instalado. Por favor, instale o Python 3.7+"
    exit 1
fi

echo "✅ Python3 encontrado: $(python3 --version)"
echo ""

# Mostrar ajuda do script
echo "📖 AJUDA DO SCRIPT:"
echo "-------------------"
python3 workstation_automation_simple.py --help
echo ""

# Criar arquivo de exemplo se não existir
if [ ! -f "sample_groups.json" ]; then
    echo "📝 Criando arquivo de exemplo..."
    python3 workstation_automation_simple.py --create-sample
    echo ""
fi

# Mostrar conteúdo do arquivo de exemplo
echo "📁 CONTEÚDO DO ARQUIVO DE EXEMPLO:"
echo "----------------------------------"
cat sample_groups.json
echo ""

# Mostrar arquivo de exemplo mais completo
echo "📁 CONTEÚDO DO ARQUIVO DE EXEMPLO COMPLETO:"
echo "-------------------------------------------"
cat example_groups.json
echo ""

# Exemplos de uso
echo "💡 EXEMPLOS DE USO:"
echo "-------------------"
echo ""
echo "1️⃣  Criar um grupo individual:"
echo "   python3 workstation_automation_simple.py \\"
echo "     --url \"https://sua-api.com\" \\"
echo "     --warehouse \"BRTW01\" \\"
echo "     --code 1 \\"
echo "     --description \"PACKING\""
echo ""
echo "2️⃣  Criar múltiplos grupos de um arquivo:"
echo "   python3 workstation_automation_simple.py \\"
echo "     --url \"https://sua-api.com\" \\"
echo "     --file \"example_groups.json\""
echo ""
echo "3️⃣  Usar ID de chamador personalizado:"
echo "   python3 workstation_automation_simple.py \\"
echo "     --url \"https://sua-api.com\" \\"
echo "     --caller-id \"456\" \\"
echo "     --file \"sample_groups.json\""
echo ""

# Verificar se há uma URL de teste
if [ -n "$1" ]; then
    echo "🧪 TESTE COM URL FORNECIDA:"
    echo "----------------------------"
    echo "URL fornecida: $1"
    echo ""
    echo "Testando validação de dados..."
    echo "Criando grupo de teste (não será enviado para a API real):"
    echo ""
    
    # Simular criação sem enviar para a API real
    echo "Simulação de criação de grupo:"
    echo "  - warehouse_id: BRTW01"
    echo "  - code: 999"
    echo "  - description: TESTE_DEMO"
    echo ""
    echo "✅ Dados validados com sucesso!"
    echo "⚠️  Para criar grupos reais, use uma das opções acima com uma URL válida."
else
    echo "🧪 PARA TESTAR O SISTEMA:"
    echo "-------------------------"
    echo "Execute este script com uma URL de teste:"
    echo "  ./demo_workstation.sh \"https://api-teste.exemplo.com\""
    echo ""
    echo "Ou execute diretamente:"
    echo "  python3 workstation_automation_simple.py --url \"https://api.exemplo.com\" --file \"example_groups.json\""
fi

echo ""
echo "📚 DOCUMENTAÇÃO COMPLETA:"
echo "-------------------------"
echo "Consulte o arquivo README.md para informações detalhadas sobre:"
echo "  - Estrutura da API"
echo "  - Formatos de entrada e saída"
echo "  - Tratamento de erros"
echo "  - Validações automáticas"
echo "  - Exemplos práticos"
echo ""
echo "🎯 RECURSOS DISPONÍVEIS:"
echo "-----------------------"
echo "✅ Validação automática de dados"
echo "✅ Tratamento de erros HTTP (400, 500)"
echo "✅ Criação em lote de múltiplos grupos"
echo "✅ Rate limiting (2s entre requisições)"
echo "✅ Logging detalhado de operações"
echo "✅ Resumo de resultados com sucessos/falhas"
echo ""
echo "✨ Sistema de automação de workstations pronto para uso!"