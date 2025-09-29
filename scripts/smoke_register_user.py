from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.user_repository import SQLAlchemyUserRepository
from brasiltransporta.infrastructure.security.password_hasher import BcryptPasswordHasher
from brasiltransporta.application.users.use_cases.register_user import RegisterUserUseCase, RegisterUserInput

def main():
    s = get_session()
    try:
        repo = SQLAlchemyUserRepository(s)
        hasher = BcryptPasswordHasher()
        uc = RegisterUserUseCase(users=repo, hasher=hasher)
        out = uc.execute(RegisterUserInput(
            name="Ana",
            email="ana@example.com",
            password="segredo123",
            region="Sudeste",
        ))
        print("OK user_id:", out.user_id)
    finally:
        s.close()

if __name__ == "__main__":
    main()
