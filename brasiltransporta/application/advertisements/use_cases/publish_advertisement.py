from dataclasses import dataclass
from brasiltransporta.domain.repositories.advertisement_repository import AdvertisementRepository
from brasiltransporta.domain.errors import ValidationError


@dataclass(frozen=True)
class PublishAdvertisementInput:
    advertisement_id: str


@dataclass(frozen=True)
class PublishAdvertisementOutput:
    advertisement_id: str
    status: str


class PublishAdvertisementUseCase:
    def __init__(self, ads: AdvertisementRepository):
        self._ads = ads

    def execute(self, data: PublishAdvertisementInput) -> PublishAdvertisementOutput:
        # 1) buscar o anúncio
        ad = self._ads.get_by_id(data.advertisement_id)
        if not ad:
            raise ValidationError("Anúncio não encontrado.")

        # 2) verificar status atual
        if ad.status != "draft":
            raise ValidationError("Somente anúncios em 'draft' podem ser publicados.")

        # 3) mudar status no domínio
        ad.publish()

        # 4) persistir mudança
        self._ads.update(ad)

        # 5) retornar saída
        return PublishAdvertisementOutput(
            advertisement_id=ad.id,
            status=ad.status,
        )
