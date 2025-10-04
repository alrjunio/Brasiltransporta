from pydantic import BaseModel, Field

class CreateAdvertisementRequest(BaseModel):
    store_id: str = Field(..., description="ID da loja")
    vehicle_id: str = Field(..., description="ID do veículo")
    title: str = Field(..., min_length=5, max_length=200, description="Título do anúncio")
    description: str = Field(..., min_length=10, description="Descrição do anúncio")
    price_amount: float = Field(..., gt=0, description="Preço do veículo")
    price_currency: str = Field("BRL", description="Moeda (padrão: BRL)")