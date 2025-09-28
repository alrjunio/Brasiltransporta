# Script de setup do projeto BrasilTransporta

Write-Host "🚚 Configurando BrasilTransporta..." -ForegroundColor Cyan

# Verificar Python
Write-Host "🐍 Verificando Python..."
$pythonVersion = python --version
if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Python não encontrado. Instale Python 3.11+"
    exit 1
}
Write-Host "✅ Python: $pythonVersion"

# Verificar Docker
Write-Host "🐳 Verificando Docker..."
$dockerVersion = docker --version
if ($LASTEXITCODE -ne 0) {
    Write-Warning "⚠️  Docker não encontrado. CI/CD pode não funcionar totalmente"
} else {
    Write-Host "✅ Docker: $dockerVersion"
}

# Criar .env se não existir
if (-not (Test-Path ".env")) {
    Write-Host "📄 Criando .env a partir de .env.example..."
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ Arquivo .env criado. Configure as variáveis necessárias."
    } else {
        Write-Warning "⚠️  .env.example não encontrado"
    }
}

# Instalar dependências
Write-Host "📦 Instalando dependências Python..."
pip install -r requirements.txt

Write-Host "✅ Setup completado!" -ForegroundColor Green
Write-Host "🎯 Próximos passos:"
Write-Host "   1. Configure o .env com suas variáveis"
Write-Host "   2. Execute: docker-compose up --build"
Write-Host "   3. Teste: scripts/test-local.ps1"
