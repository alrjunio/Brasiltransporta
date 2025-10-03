from dataclasses import dataclass
from typing import Optional

from brasiltransporta.domain.repositories.user_repository import UserRepository


@dataclass(frozen=True)
class GetUserByIdOutput:
    id: str
    name: str
    email: str
    phone: Optional[str]
    birth_date: Optional[str]
    profession: Optional[str]
    region: Optional[str]


class GetUserByIdUseCase:
    def __init__(self, users: UserRepository):
        self._users = users

    def execute(self, user_id: str) -> Optional[GetUserByIdOutput]:
        user = self._users.get_by_id(user_id)
        if not user:
            return None
        return GetUserByIdOutput(
            id=user.id,
            name=user.name,
            email=str(user.email),
            phone=str(user.phone) if user.phone else None,
            birth_date=user.birth_date,
            profession=user.profession,
            region=user.region,
        )
