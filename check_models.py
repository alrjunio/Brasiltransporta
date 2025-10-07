# check_models.py
try:
    # Testar imports
    from brasiltransporta.infrastructure.persistence.sqlalchemy.models.advertisement import AdvertisementModel
    from brasiltransporta.infrastructure.persistence.sqlalchemy.models.vehicle import VehicleModel
    from brasiltransporta.infrastructure.persistence.sqlalchemy.models.store import StoreModel
    print("✅ Model imports: OK")
    
    # Testar entidades
    from brasiltransporta.domain.entities.advertisement import Advertisement
    from brasiltransporta.domain.entities.vehicle import Vehicle
    from brasiltransporta.domain.entities.store import Store
    from brasiltransporta.domain.entities.enums import AdvertisementStatus, VehicleBrand, VehicleType, VehicleCondition, StoreCategory, ImplementSegment
    from brasiltransporta.domain.entities.address import Address
    
    print("📋 Enums disponíveis:")
    print(f"  VehicleType: {[e.name for e in VehicleType]}")
    print(f"  VehicleBrand: {[e.name for e in VehicleBrand]}")
    print(f"  VehicleCondition: {[e.name for e in VehicleCondition]}")
    
    # Testar criação de Advertisement (com título e descrição válidos)
    ad = Advertisement.create(
        "store123", 
        "vehicle456", 
        "Volvo FH 540 2023 - Excelente Estado",  # ← Título > 5 chars
        "Caminhão Volvo FH 540 ano 2023 em perfeito estado de conservação",  # ← Descrição > 10 chars
        350000.00
    )
    print("✅ Advertisement entity: OK")
    
    # Testar criação de Vehicle
    vehicle = Vehicle.create(
        "store123", 
        VehicleBrand.VOLVO, 
        "FH 540", 
        2023, 
        "ABC1D23",
        VehicleType.HEAVY_TRUCK,  # ← VALOR REAL
        VehicleCondition.NEW,     # ← VALOR REAL  
        350000.00
    )
    print("✅ Vehicle entity: OK")
    print(f"  Descrição completa: {vehicle.get_full_description()}")
    
    # Testar criação de Store
    address = Address("Avenida Paulista", "São Paulo", "SP", "01310-100")
    store = Store.create(
        "Loja de Caminhões SP", 
        "owner123", 
        "Especializada em veículos pesados Volvo e Scania", 
        address,
        [StoreCategory.VENDA_VEICULOS], 
        "+5511999999999"
    )
    print("✅ Store entity: OK")
    print(f"  Categorias: {[c.value for c in store.categories]}")
    
    # Testar funcionalidades avançadas
    print("\n🎯 Testando funcionalidades:")
    
    # Advertisement
    ad.publish()
    print(f"  Advertisement status após publicar: {ad.status.value}")
    ad.add_image("https://example.com/volvo1.jpg")
    print(f"  Advertisement tem mídia: {ad.has_media}")
    
    # Vehicle
    vehicle.update_price(320000.00)
    print(f"  Vehicle preço atualizado: {vehicle.price}")
    
    # Store  
    store.add_category(StoreCategory.AUTO_PECAS)
    print(f"  Store categorias atualizadas: {[c.value for c in store.categories]}")
    
    print("\n🎉 TODAS AS ENTIDADES E FUNCIONALIDADES FUNCIONANDO PERFEITAMENTE!")
    print("🚛 Sistema pronto para veículos pesados!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()