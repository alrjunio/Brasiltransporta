from dataclasses import dataclass

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
    def __init__(self, advertisements, stores, vehicles):
        self._advertisements = advertisements
        self._stores = stores
        self._vehicles = vehicles

    def execute(self, data: CreateAdvertisementInput) -> CreateAdvertisementOutput:
        # Simulação - em produção validaria store e vehicle
        from brasiltransporta.domain.entities.advertisement import Advertisement
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
