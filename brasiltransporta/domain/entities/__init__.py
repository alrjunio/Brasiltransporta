# brasiltransporta/domain/entities/__init__.py
from .address import Address
from .enums import VehicleType, VehicleCondition, StoreCategory, AdvertisementStatus, VehicleBrand, ImplementSegment
from .store import Store
from .vehicle import Vehicle
from .advertisement import Advertisement
from .user import User
from .plan import Plan
from .transaction import Transaction
from .phone_verification import PhoneVerification

__all__ = [
    "Address",
    "VehicleType", 
    "VehicleCondition",
    "StoreCategory", 
    "AdvertisementStatus",
    "Store",
    "Vehicle",
    "Advertisement", 
    "User",
    "Plan",
    "Transaction",
    "PhoneVerification",
    "VehicleBrand",
    "ImplementSegment"
]