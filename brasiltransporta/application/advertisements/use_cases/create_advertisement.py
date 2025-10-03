from dataclasses import dataclass
from typing import Optional
from brasiltransporta.domain.entities.advertisement import Advertisement
from brasiltransporta.domain.errors import ValidationError

@dataclass
class CreateAdvertisementInput:
    store_id: str
    vehicle_id: str
    title: str
    description: Optional[str] = ""
    price_amount: float = 0.0

@dataclass
class CreateAdvertisementOutput:
    advertisement_id: str

class CreateAdvertisementUseCase:
    def __init__(self, ad_repo, store_repo, vehicle_repo):
        self._ads = ad_repo
        self._stores = store_repo
        self._vehicles = vehicle_repo

    def execute(self, inp: CreateAdvertisementInput) -> CreateAdvertisementOutput:
        store = self._stores.get_by_id(inp.store_id) if hasattr(self._stores, "get_by_id") else None
        if store is None:
            raise ValidationError("Loja não encontrada")

        vehicle = self._vehicles.get_by_id(inp.vehicle_id) if hasattr(self._vehicles, "get_by_id") else None
        if vehicle is None:
            raise ValidationError("Veículo não encontrado")

        ad = Advertisement.create(
            store_id=inp.store_id,
            vehicle_id=inp.vehicle_id,
            title=inp.title,
            description=inp.description or "",
            price_amount=inp.price_amount,
        )
        if hasattr(self._ads, "add"):
            self._ads.add(ad)
        return CreateAdvertisementOutput(advertisement_id=ad.id)
