from dataclasses import dataclass
from brasiltransporta.domain.errors import ValidationError

# Sequências obviamente inválidas (14 dígitos iguais)
_INVALID_SEQUENCES = {str(d) * 14 for d in range(10)}

def _calc_digit(nums: str) -> int:
    # Cálculo de dígito verificador do CNPJ
    # Para o 1º DV usamos pesos 5..2 + 9..2; para o 2º DV, 6..2 + 9..2
    def dv(payload: str, first: bool) -> int:
        weights = ([5,4,3,2,9,8,7,6,5,4,3,2] if first
                   else [6,5,4,3,2,9,8,7,6,5,4,3,2])
        s = sum(int(d) * w for d, w in zip(payload, weights))
        r = s % 11
        return 0 if r < 2 else 11 - r
    dv1 = dv(nums[:12], True)
    dv2 = dv(nums[:12] + str(dv1), False)
    return dv1, dv2

@dataclass(frozen=True)
class CNPJ:
    value: str

    def __post_init__(self):
        digits = "".join(filter(str.isdigit, self.value))

        if len(digits) != 14:
            raise ValidationError("CNPJ deve ter 14 dígitos.")

        if digits in _INVALID_SEQUENCES:
            raise ValidationError("CNPJ inválido.")

        dv1, dv2 = _calc_digit(digits)
        if digits[-2:] != f"{dv1}{dv2}":
            raise ValidationError("CNPJ inválido (dígitos verificadores).")

        object.__setattr__(self, "value", digits)

    def __str__(self) -> str:
        return self.value

    def formatted(self) -> str:
        # 12.345.678/0001-99
        v = self.value
        return f"{v[0:2]}.{v[2:5]}.{v[5:8]}/{v[8:12]}-{v[12:14]}"
