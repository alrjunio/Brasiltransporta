from typing import Optional

from brasiltransporta.domain.repositories.user_repository import UserRepository
from .get_user_by_id import GetUserByIdOutput  # Reaproveita o mesmo DTO de saída


class GetUserByEmailUseCase:
    def __init__(self, users: UserRepository):
        self._users = users

    def execute(self, email: str) -> Optional[GetUserByIdOutput]:
        user = self._users.get_by_email(email)
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
