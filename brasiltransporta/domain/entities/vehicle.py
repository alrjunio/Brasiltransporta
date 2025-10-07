# brasiltransporta/domain/entities/vehicle.py
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import uuid4

from brasiltransporta.domain.entities.enums import VehicleBrand, VehicleType, VehicleCondition, ImplementSegment


@dataclass
class Vehicle:
    """Entidade Veículo adaptada para veículos pesados com categorias específicas"""
    
    # ✅ CAMPOS SEM VALOR PADRÃO PRIMEIRO
    id: str
    store_id: str
    brand: VehicleBrand
    model: str
    year: int
    plate: str
    vehicle_type: VehicleType
    condition: VehicleCondition
    price: Decimal
    
    # ✅ CAMPOS COM VALOR PADRÃO DEPOIS
    implement_segment: Optional[ImplementSegment] = None
    description: Optional[str] = None
    mileage: Optional[int] = None
    color: Optional[str] = None
    engine_power: Optional[str] = None
    axle_configuration: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    @classmethod
    def create(cls, store_id: str, brand: VehicleBrand, model: str,
               year: int, plate: str, vehicle_type: VehicleType, 
               condition: VehicleCondition, price: Decimal,
               implement_segment: Optional[ImplementSegment] = None,
               description: Optional[str] = None, mileage: Optional[int] = None,
               color: Optional[str] = None, engine_power: Optional[str] = None,
               axle_configuration: Optional[str] = None) -> "Vehicle":
        """Factory method para criar Vehicle com categorias específicas"""
        
        # VALIDAÇÕES (novas):
        if year < 1900 or year > datetime.now().year + 1:
            raise ValueError("Invalid year")
        if price <= 0:
            raise ValueError("Price must be positive")

        return cls(
            id=str(uuid4()),
            store_id=store_id,
            brand=brand,
            model=model.strip(),
            year=year,
            plate=plate.upper().strip(),
            vehicle_type=vehicle_type,
            condition=condition,
            price=price,
            implement_segment=implement_segment,
            description=description.strip() if description else None,
            mileage=mileage,
            color=color.strip() if color else None,
            engine_power=engine_power,
            axle_configuration=axle_configuration
        )

    def update_price(self, new_price: Decimal) -> None:
        """Atualiza o preço do veículo"""
        if new_price <= 0:
            raise ValueError("Price must be positive")
        self.price = new_price
        self.updated_at = datetime.utcnow()

    def update_mileage(self, new_mileage: int) -> None:
        """Atualiza a quilometragem"""
        if new_mileage < 0:
            raise ValueError("Mileage cannot be negative")
        self.mileage = new_mileage
        self.updated_at = datetime.utcnow()

    def is_implement(self) -> bool:
        """Verifica se é um implemento"""
        return self.implement_segment is not None

    def get_full_description(self) -> str:
        """Retorna descrição completa do veículo"""
        base = f"{self.brand.value} {self.model} {self.year}"
        if self.axle_configuration:
            base += f" {self.axle_configuration}"
        if self.engine_power:
            base += f" {self.engine_power}"
        return base