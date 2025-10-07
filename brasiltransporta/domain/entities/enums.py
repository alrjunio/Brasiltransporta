# brasiltransporta/domain/entities/enums.py
from enum import Enum

class VehicleType(Enum):
    """Tipos de veículos pesados"""
    HEAVY_TRUCK = "caminhao_pesado"
    SEMI_TRUCK = "caminhao_semi_pesado"
    TRUCK = "caminhao"  # ← ADICIONADO
    TRACTOR_TRUCK = "caminhao_trator"
    IMPLEMENT = "implemento"
    BUS = "onibus"
    VAN = "van"
    PICKUP = "caminhonete"

class VehicleBrand(Enum):
    """Marcas de veículos pesados"""
    VOLVO = "volvo"
    SCANIA = "scania"
    MERCEDES_BENZ = "mercedes_benz"
    VOLKSWAGEN = "volkswagen"
    FORD = "ford"
    IVECO = "iveco"
    DAIMLER = "daimler"
    MAN = "man"
    AGCO = "agco"
    CASE = "case"
    JOHN_DEERE = "john_deere"

class VehicleCondition(Enum):
    """Condição do veículo"""
    NEW = "novo"
    USED = "usado"
    REFURBISHED = "reformado"

class ImplementSegment(Enum):
    """Segmentos de implementos rodoviários"""
    SEMI_TRAILER = "semi_reboque"
    TRAILER = "reboque"
    TANK_TRUCK = "caminhao_tanque"
    DUMP_TRUCK = "caminhao_basculante"
    BODY_TRUCK = "caminhao_carroceria"

class StoreCategory(Enum):
    """Categorias de lojas"""
    TRUCK_DEALER = "concessionaria_caminhoes"
    PARTS_STORE = "loja_pecas"
    REPAIR_SHOP = "oficina_mecanica"
    TIRE_SHOP = "loja_pneus"
    BODY_SHOP = "funilaria_pintura"
    AUCTION_HOUSE = "leilao"
    RENTAL_COMPANY = "locadora"

class AdvertisementStatus(Enum):
    """Status do anúncio"""
    DRAFT = "rascunho"
    ACTIVE = "ativo"
    PAUSED = "pausado"
    SOLD = "vendido"
    EXPIRED = "expirado"
    DELETED = "excluido"

class UserRole(Enum):
    """Papéis de usuário"""
    ADMIN = "admin"
    STORE_OWNER = "store_owner"
    BUYER = "buyer"
    SELLER = "seller"
    BASIC = "basic"

class TransactionStatus(Enum):
    """Status da transação"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PlanType(Enum):
    """Tipos de plano"""
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"