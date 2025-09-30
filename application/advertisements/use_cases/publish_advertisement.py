# application/advertisements/use_cases/publish_advertisement.py
from dataclasses import dataclass
from brasiltransporta.domain.repositories.advertisement_repository import AdvertisementRepository
from brasiltransporta.domain.errors import ValidationError

@dataclass(frozen=True)
class PublishAdvertisementInput:
    advertisement_id: str

@dataclass(frozen=True)
class PublishAdvertisementOutput:
    success: bool

class PublishAdvertisementUseCase:
    def __init__(self, advertisements: AdvertisementRepository):
        self._advertisements = advertisements

    def execute(self, data: PublishAdvertisementInput) -> PublishAdvertisementOutput:
        advertisement = self._advertisements.get_by_id(data.advertisement_id)
        if not advertisement:
            raise ValidationError("Anúncio não encontrado.")

        advertisement.publish()
        self._advertisements.update(advertisement)
        
        return PublishAdvertisementOutput(success=True)
