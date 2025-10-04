<# setup-tests.ps1
   Organiza a estrutura de testes e (opcional) cria/ajusta entidades de dominio.
   Uso:
     .\setup-tests.ps1
     .\setup-tests.ps1 -WithDomainFix
     .\setup-tests.ps1 -WithDomainFix -ForceOverwrite
#>

[CmdletBinding()]
param(
  [switch]$WithDomainFix,
  [switch]$ForceOverwrite
)

$ErrorActionPreference = "Stop"

function New-BackupFolder {
  param([string]$Root)
  $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
  $dir = Join-Path $Root ".backup-$stamp"
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  return $dir
}

function Ensure-Dir {
  param([string]$Path)
  if (-not (Test-Path $Path)) {
    New-Item -ItemType Directory -Force -Path $Path | Out-Null
  }
}

function Write-TextFile {
  param(
    [string]$Path,
    [string]$Content,
    [switch]$Overwrite,
    [string]$BackupDir
  )
  if ((Test-Path $Path) -and -not $Overwrite) { return }
  if ((Test-Path $Path) -and $Overwrite -and $BackupDir) {
    $rel = $Path -replace "[:\\\/]", "_"
    Copy-Item $Path (Join-Path $BackupDir $rel) -Force
  }
  $folder = Split-Path $Path -Parent
  Ensure-Dir $folder
  Set-Content -Path $Path -Value $Content -Encoding UTF8
}

function Move-IfExists {
  param([string]$Src,[string]$Dst,[string]$BackupDir)
  if (Test-Path $Src) {
    Ensure-Dir (Split-Path $Dst -Parent)
    if (Test-Path $Dst) {
      $srcInfo = Get-Item $Src
      $dstInfo = Get-Item $Dst
      $legacyDir = Join-Path (Split-Path $Dst -Parent) "_legacy"
      Ensure-Dir $legacyDir
      if ($srcInfo.LastWriteTime -gt $dstInfo.LastWriteTime) {
        Move-Item $Dst (Join-Path $legacyDir ([IO.Path]::GetFileName($Dst))) -Force
        Move-Item $Src $Dst -Force
      } else {
        Move-Item $Src (Join-Path $legacyDir ([IO.Path]::GetFileName($Src))) -Force
      }
    } else {
      Move-Item $Src $Dst -Force
    }
  }
}

$root = (Get-Location).Path
$backup = New-BackupFolder -Root $root
Write-Host "Root: $root"
Write-Host "Backup: $backup"

# 1) Estrutura de diretorios
$paths = @(
  "tests",
  "tests\domain\entities",
  "tests\application\advertisements",
  "tests\application\plans",
  "tests\application\transactions",
  "tests\application\users",
  "tests\presentation\api"
)
$paths | ForEach-Object { Ensure-Dir (Join-Path $root $_) }

# 2) Mover/Unificar arquivos de teste
Move-IfExists -Src (Join-Path $root "test_advertisement.py")   -Dst (Join-Path $root "tests\domain\entities\test_advertisement.py") -BackupDir $backup
Move-IfExists -Src (Join-Path $root "test_plan.py")             -Dst (Join-Path $root "tests\domain\entities\test_plan.py")           -BackupDir $backup
Move-IfExists -Src (Join-Path $root "test_transaction.py")      -Dst (Join-Path $root "tests\domain\entities\test_transaction.py")    -BackupDir $backup

# nomes no plural (segundo lote)
Move-IfExists -Src (Join-Path $root "test_advertisements.py")   -Dst (Join-Path $root "tests\domain\entities\test_advertisement.py")  -BackupDir $backup
Move-IfExists -Src (Join-Path $root "test_plans.py")            -Dst (Join-Path $root "tests\domain\entities\test_plan.py")           -BackupDir $backup
Move-IfExists -Src (Join-Path $root "test_transactions.py")     -Dst (Join-Path $root "tests\domain\entities\test_transaction.py")    -BackupDir $backup

# application
Move-IfExists -Src (Join-Path $root "test_advertisement_use_cases.py") -Dst (Join-Path $root "tests\application\advertisements\test_use_cases.py") -BackupDir $backup
Move-IfExists -Src (Join-Path $root "test_plan_use_cases.py")          -Dst (Join-Path $root "tests\application\plans\test_use_cases.py")          -BackupDir $backup
Move-IfExists -Src (Join-Path $root "test_transaction_use_cases.py")   -Dst (Join-Path $root "tests\application\transactions\test_use_cases.py")   -BackupDir $backup
Move-IfExists -Src (Join-Path $root "test_register_user_use_case.py")  -Dst (Join-Path $root "tests\application\users\test_register_user_use_case.py") -BackupDir $backup
Move-IfExists -Src (Join-Path $root "test_get_user_use_cases.py")      -Dst (Join-Path $root "tests\application\users\test_get_user_use_cases.py")     -BackupDir $backup

# presentation/api
Move-IfExists -Src (Join-Path $root "test_routes.py")     -Dst (Join-Path $root "tests\presentation\api\test_routes.py")      -BackupDir $backup
Move-IfExists -Src (Join-Path $root "test_users_api.py")  -Dst (Join-Path $root "tests\presentation\api\test_users_api.py")   -BackupDir $backup

# conftest na pasta tests
if (Test-Path (Join-Path $root "conftest.py")) {
  Move-IfExists -Src (Join-Path $root "conftest.py") -Dst (Join-Path $root "tests\conftest.py") -BackupDir $backup
}

# 3) pytest.ini (sem BOM)
$pytestIni = @"
[pytest]
testpaths = tests
addopts = -q
filterwarnings =
    ignore::DeprecationWarning
"@
Write-TextFile -Path (Join-Path $root "pytest.ini") -Content $pytestIni -Overwrite -BackupDir $backup
$p = Get-Content -Raw (Join-Path $root "pytest.ini")
[IO.File]::WriteAllText((Resolve-Path (Join-Path $root "pytest.ini")), $p, (New-Object System.Text.UTF8Encoding($false)))

# 4) conftest unificado
$conftestContent = @"
import os
import pathlib
import tempfile
import pytest

try:
    from fastapi.testclient import TestClient
    from brasiltransporta.presentation.api.app import app
    HAS_API = True
except Exception:
    HAS_API = False
    app = None
    TestClient = None

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from brasiltransporta.infrastructure.persistence.sqlalchemy.models.base import Base
    HAS_DB = True
except Exception:
    HAS_DB = False

@pytest.fixture(scope="session")
def sqlite_engine_tmp():
    if not HAS_DB:
        pytest.skip("Infra DB nao disponivel neste projeto (pular fixtures DB).")
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    url = f"sqlite:///{db_path}"
    engine = create_engine(url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    try:
        yield engine
    finally:
        engine.dispose()
        pathlib.Path(db_path).unlink(missing_ok=True)

@pytest.fixture(scope="function")
def client(sqlite_engine_tmp, monkeypatch):
    if not HAS_API:
        pytest.skip("App FastAPI nao disponivel (pular testes de API).")
    try:
        from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session as _get_session
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine_tmp)
        def _test_session():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()
        monkeypatch.setattr(
            "brasiltransporta.infrastructure.persistence.sqlalchemy.session.get_session",
            _test_session,
            raising=True,
        )
    except Exception:
        pass
    return TestClient(app) if HAS_API else None
"@
Write-TextFile -Path (Join-Path $root "tests\conftest.py") -Content $conftestContent -Overwrite -BackupDir $backup

# 5) Dominio opcional
if ($WithDomainFix) {
  Write-Host "Aplicando ajustes de dominio."
  $domainRoot = Join-Path $root "brasiltransporta\domain"
  $entitiesDir = Join-Path $domainRoot "entities"
  $voDir = Join-Path $domainRoot "value_objects"
  $errorsDir = Join-Path $domainRoot "errors"
  Ensure-Dir $entitiesDir; Ensure-Dir $voDir; Ensure-Dir $errorsDir

  $errorsPy = Join-Path $errorsDir "errors.py"
  $errorsContent = @"
class ValidationError(Exception):
    pass
"@
  if (-not (Test-Path $errorsPy)) { Write-TextFile -Path $errorsPy -Content $errorsContent -Overwrite -BackupDir $backup }

  $moneyPy = Join-Path $voDir "money.py"
  $moneyContent = @"
from dataclasses import dataclass
@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "BRL"
"@
  if (-not (Test-Path $moneyPy) -or $ForceOverwrite) {
    Write-TextFile -Path $moneyPy -Content $moneyContent -Overwrite:$ForceOverwrite -BackupDir $backup
  }

  $adPy = Join-Path $entitiesDir "advertisement.py"
  $adContent = @"
from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4
from typing import Optional

class AdvertisementStatus(Enum):
    DRAFT = 'draft'
    ACTIVE = 'active'
    SOLD = 'sold'

@dataclass
class Advertisement:
    id: str
    store_id: str
    vehicle_id: str
    title: str
    description: Optional[str]
    price_amount: float
    status: AdvertisementStatus = field(default=AdvertisementStatus.DRAFT)
    views: int = field(default=0)
    is_featured: bool = field(default=False)

    @classmethod
    def create(cls, store_id: str, vehicle_id: str, title: str, description: Optional[str], price_amount: float):
        if title is None or len(title.strip()) < 5:
            raise ValueError("Titulo deve ter pelo menos 5 caracteres")
        return cls(
            id=str(uuid4()),
            store_id=store_id,
            vehicle_id=vehicle_id,
            title=title.strip(),
            description=description,
            price_amount=float(price_amount),
        )

    def publish(self):
        self.status = AdvertisementStatus.ACTIVE

    def mark_as_sold(self):
        self.status = AdvertisementStatus.SOLD

    def increment_views(self):
        self.views += 1
"@
  Write-TextFile -Path $adPy -Content $adContent -Overwrite:$ForceOverwrite -BackupDir $backup

  $planPy = Join-Path $entitiesDir "plan.py"
  $planContent = @"
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from uuid import uuid4

class PlanType(Enum):
    BASIC = 'basic'

class BillingCycle(Enum):
    MONTHLY = 'monthly'

@dataclass
class Plan:
    id: str
    name: str
    description: Optional[str]
    plan_type: PlanType
    billing_cycle: BillingCycle
    price_amount: float
    is_active: bool = field(default=True)
    max_ads: Optional[int] = None
    max_featured_ads: Optional[int] = None
    features: Optional[List[str]] = None

    @classmethod
    def create(cls, name: str, description: Optional[str], plan_type: PlanType, billing_cycle: BillingCycle,
               price_amount: float, max_ads: Optional[int]=None, max_featured_ads: Optional[int]=None,
               features: Optional[List[str]]=None):
        if name is None or len(name.strip()) < 3:
            raise ValueError("Nome do plano deve ter pelo menos 3 caracteres")
        return cls(
            id=str(uuid4()),
            name=name.strip(),
            description=description,
            plan_type=plan_type,
            billing_cycle=billing_cycle,
            price_amount=float(price_amount),
            max_ads=max_ads,
            max_featured_ads=max_featured_ads,
            features=features
        )

    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True
"@
  Write-TextFile -Path $planPy -Content $planContent -Overwrite:$ForceOverwrite -BackupDir $backup

  $txPy = Join-Path $entitiesDir "transaction.py"
  $txContent = @"
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any
from uuid import uuid4
from brasiltransporta.domain.value_objects.money import Money
from brasiltransporta.domain.errors.errors import ValidationError

class TransactionStatus(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'

class PaymentMethod(Enum):
    CREDIT_CARD = 'credit_card'

@dataclass
class Transaction:
    id: str
    user_id: str
    plan_id: str
    amount: Money
    payment_method: PaymentMethod
    status: TransactionStatus = field(default=TransactionStatus.PENDING)
    external_payment_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def create(cls, user_id: str, plan_id: str, amount: float, payment_method: PaymentMethod, metadata: Optional[Dict[str, Any]]=None):
        if amount is None or float(amount) <= 0:
            raise ValidationError("Valor da transacao deve ser maior que zero")
        return cls(
            id=str(uuid4()),
            user_id=user_id,
            plan_id=plan_id,
            amount=Money(float(amount)),
            payment_method=payment_method,
            metadata=metadata
        )

    def mark_completed(self, external_id: str):
        self.status = TransactionStatus.COMPLETED
        self.external_payment_id = external_id

    def mark_failed(self):
        self.status = TransactionStatus.FAILED

    def refund(self):
        if self.status != TransactionStatus.COMPLETED:
            raise ValidationError("Apenas transacoes completadas podem ser reembolsadas")
        self.status = TransactionStatus.REFUNDED
"@
  Write-TextFile -Path $txPy -Content $txContent -Overwrite:$ForceOverwrite -BackupDir $backup
}

Write-Host ""
Write-Host "Done."
Write-Host "Estrutura consolidada em .\tests"
Write-Host "pytest.ini salvo sem BOM"
if ($WithDomainFix) {
  if ($ForceOverwrite) { Write-Host "Entidades reescritas (backup: $backup)" }
  else { Write-Host "Entidades criadas/ajustadas (backup: $backup)" }
}
Write-Host "Para rodar: pytest -q"