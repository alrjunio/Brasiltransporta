# application/advertisements/use_cases/create_advertisement.py
from dataclasses import dataclass
from brasiltransporta.domain.repositories.advertisement_repository import AdvertisementRepository
from brasiltransporta.domain.repositories.store_repository import StoreRepository
from brasiltransporta.domain.repositories.vehicle_repository import VehicleRepository
from brasiltransporta.domain.entities.advertisement import Advertisement
from brasiltransporta.domain.errors import ValidationError

@dataclass(frozen=True)
class CreateAdvertisementInput:
    store_id: str
    vehicle_id: str
    title: str
    description: str
    price_amount: float
    price_currency: str = "BRL"

@dataclass(frozen=True)
class CreateAdvertisementOutput:
    advertisement_id: str

class CreateAdvertisementUseCase:
    def __init__(
        self, 
        advertisements: AdvertisementRepository,
        stores: StoreRepository,
        vehicles: VehicleRepository
    ):
        self._advertisements = advertisements
        self._stores = stores
        self._vehicles = vehicles

    def execute(self, data: CreateAdvertisementInput) -> CreateAdvertisementOutput:
        # Validar se store existe
        store = self._stores.get_by_id(data.store_id)
        if not store:
            raise ValidationError("Loja não encontrada.")

        # Validar se vehicle existe e pertence à store
        vehicle = self._vehicles.get_by_id(data.vehicle_id)
        if not vehicle or vehicle.store_id != data.store_id:
            raise ValidationError("Veículo não encontrado ou não pertence à loja.")

        advertisement = Advertisement.create(
            store_id=data.store_id,
            vehicle_id=data.vehicle_id,
            title=data.title,
            description=data.description,
            price_amount=data.price_amount,
            price_currency=data.price_currency
        )

        self._advertisements.add(advertisement)
        return CreateAdvertisementOutput(advertisement_id=advertisement.id)
