from sqlalchemy.orm import DeclarativeBase, declared_attr

class Base(DeclarativeBase):
    """Base declarativa para todos os modelos SQLAlchemy (2.x)."""

    # prefixo de schema/tabela se você quiser padronizar (opcional)
    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore[override]
        # nome da tabela em snake_case simples a partir do nome da classe
        return cls.__name__.replace("Model", "").lower()
