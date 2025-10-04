from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "BRL"

    def __post_init__(self):
        # validação simples
        if self.amount is None or float(self.amount) <= 0:
            raise ValueError("Valor da transação deve ser maior que zero")
        if not isinstance(self.currency, str) or not self.currency:
            raise ValueError("Moeda inválida")
