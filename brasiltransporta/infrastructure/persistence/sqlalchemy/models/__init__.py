from .base import Base  # mantém o Base visível

# IMPORTS EXPLÍCITOS — isso registra as tabelas no Base.metadata
from .user import UserModel              # noqa: F401
from .store import StoreModel            # noqa: F401
from .vehicle import VehicleModel        # noqa: F401
from .advertisement import AdvertisementModel  # noqa: F401
from .plan import PlanModel              # noqa: F401
from .transaction import TransactionModel  # noqa: F401
