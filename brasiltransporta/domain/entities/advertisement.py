# ... imports existentes ...
from brasiltransporta.domain.errors import ValidationError

# ... classe Advertisement já existente ...
class Advertisement:
    # campos e create(...) já definidos

    def publish(self) -> None:
        if self.status != "draft":
            raise ValidationError("Somente anúncios em 'draft' podem ser publicados.")
        self.status = "published"
