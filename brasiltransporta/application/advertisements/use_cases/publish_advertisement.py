# brasiltransporta/application/advertisements/use_cases/publish_advertisement.py
from dataclasses import dataclass
from typing import Optional

try:
    from brasiltransporta.domain.errors.errors import ValidationError
except Exception:
    class ValidationError(Exception):
        pass

@dataclass(frozen=True)
class PublishAdvertisementInput:
    advertisement_id: str

@dataclass(frozen=True)
class PublishAdvertisementOutput:
    advertisement_id: str
    success: bool = True

class PublishAdvertisementUseCase:
    def __init__(self, repository):
        """
        repository precisa expor: get_by_id(id) -> entidade | None
                                   update(entidade) -> None
        """
        self._repo = repository

    def execute(self, input_data: PublishAdvertisementInput) -> PublishAdvertisementOutput:
        ad = self._repo.get_by_id(input_data.advertisement_id)
        if not ad:
            raise ValidationError("Anúncio não encontrado")

        # se a entidade tiver método publish(), use-o; senão ajuste o status manualmente
        if hasattr(ad, "publish") and callable(getattr(ad, "publish")):
            ad.publish()
        else:
            # fallback simples
            setattr(ad, "status", "published")

        self._repo.update(ad)
        return PublishAdvertisementOutput(advertisement_id=getattr(ad, "id"))
