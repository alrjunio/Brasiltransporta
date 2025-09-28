# Script: scripts/test-local.ps1
# Testes locais antes do push

Write-Host "🧪 Executando testes locais..." -ForegroundColor Cyan

# Verificar se requirements.txt existe
if (-not (Test-Path "requirements.txt")) {
    Write-Error "❌ requirements.txt não encontrado"
    exit 1
}

# Instalar/atualizar dependências
Write-Host "📦 Instalando dependências..."
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-asyncio black flake8

# Verificar formatação
Write-Host "📝 Verificando formatação..."
black --check backend/
if ($LASTEXITCODE -ne 0) {
    Write-Warning "⚠️  Código precisa de formatação. Execute: black backend/"
}

# Verificar qualidade
Write-Host "🔍 Verificando qualidade..."
flake8 backend/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Executar testes
Write-Host "🎯 Executando testes..."
$env:DATABASE_URL = "sqlite:///./test.db"
$env:SECRET_KEY = "test-key"
python -m pytest backend/tests/ -v

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Todos os testes passaram! Pode fazer push." -ForegroundColor Green
} else {
    Write-Error "❌ Testes falharam. Corrija antes do push."
    exit 1
}
