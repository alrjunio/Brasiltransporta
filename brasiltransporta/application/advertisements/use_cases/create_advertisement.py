from dataclasses import dataclass
from typing import Optional

from brasiltransporta.domain.entities.advertisement import Advertisement
from brasiltransporta.domain.value_objects.price import Price
from brasiltransporta.domain.repositories.vehicle_repository import VehicleRepository
from brasiltransporta.domain.repositories.advertisement_repository import AdvertisementRepository
from brasiltransporta.domain.errors import ValidationError


@dataclass(frozen=True)
class CreateAdvertisementInput:
    vehicle_id: str
    price: float
    title: Optional[str] = None


@dataclass(frozen=True)
class CreateAdvertisementOutput:
    advertisement_id: str
    status: str  # esperado: "draft"


class CreateAdvertisementUseCase:
    def __init__(
        self,
        vehicles: VehicleRepository,
        advertisements: AdvertisementRepository,
    ):
        self._vehicles = vehicles
        self._ads = advertisements

    def execute(self, data: CreateAdvertisementInput) -> CreateAdvertisementOutput:
        # 1) garantir que o veículo existe
        vehicle = self._vehicles.get_by_id(data.vehicle_id)
        if not vehicle:
            raise ValidationError("Veículo não encontrado para criar anúncio.")

        # 2) construir VO do preço
        price_vo = Price(data.price)

        # 3) criar entidade de anúncio (status inicial: draft)
        ad = Advertisement.create(
            vehicle=vehicle,
            price=price_vo,
            title=(data.title or "").strip(),
        )

        # 4) persistir via contrato
        self._ads.add(ad)

        # 5) retorno
        return CreateAdvertisementOutput(advertisement_id=ad.id, status=ad.status)
