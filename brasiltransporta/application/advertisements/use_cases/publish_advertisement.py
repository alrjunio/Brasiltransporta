from dataclasses import dataclass
from brasiltransporta.domain.errors import ValidationError

@dataclass
class PublishAdvertisementInput:
    advertisement_id: str

@dataclass
class PublishAdvertisementOutput:
    advertisement_id: str
    status: str

class PublishAdvertisementUseCase:
    def __init__(self, ad_repo):
        self._ads = ad_repo

    def execute(self, data: PublishAdvertisementInput) -> PublishAdvertisementOutput:
        ad = self._ads.get_by_id(data.advertisement_id)
        if not ad:
            raise ValidationError("Anúncio não encontrado.")
        ad.publish()  # valida 'draft' internamente
        if hasattr(self._ads, "update"):
            self._ads.update(ad)
        return PublishAdvertisementOutput(advertisement_id=ad.id, status=ad.status)
