from abc import ABC, abstractmethod
from enum import StrEnum

from pydantic import BaseModel


class VehicleType(StrEnum):
    CAR = "car"
    USED_CAR = "used_car"
    TAXI = "taxi"
    BUS = "bus"


class VehicleBase(BaseModel, ABC):
    name: str

    @property
    @abstractmethod
    def vehicle_type(self) -> VehicleType:
        raise NotImplementedError


class CarSpec(VehicleBase):
    brand: str
    model: str
    energy_type: str
    fuel_economy_km_per_liter: float
    price_aed: float
    maintenance_aed_per_km: float
    mileage_km: float = 0.0

    @property
    def vehicle_type(self) -> VehicleType:
        return VehicleType.CAR


class UsedCarSpec(CarSpec):
    manufacture_year: int

    @property
    def vehicle_type(self) -> VehicleType:
        return VehicleType.USED_CAR


class TaxiSpec(VehicleBase):
    flagfall_aed: float = 5.0
    price_per_km_aed: float = 1.82
    waiting_fee_per_min_aed: float = 0.5
    call_fee_aed: float = 4.0

    @property
    def vehicle_type(self) -> VehicleType:
        return VehicleType.TAXI


class BusSpec(VehicleBase):
    boarding_fee_aed: float = 2.0
    price_per_km_aed: float = 0.05

    @property
    def vehicle_type(self) -> VehicleType:
        return VehicleType.BUS
