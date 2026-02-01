import json
from pathlib import Path

from model.vehicle import BusSpec, CarSpec, TaxiSpec, UsedCarSpec, VehicleBase, VehicleType


class VehicleFactory:
    _registry: dict[VehicleType, type[VehicleBase]] = {}

    @classmethod
    def register(cls, vehicle_type: VehicleType, model: type[VehicleBase]) -> None:
        if vehicle_type in cls._registry:
            raise ValueError(f"Vehicle type already registered: {vehicle_type.value}")
        cls._registry[vehicle_type] = model

    @classmethod
    def create(cls, payload: dict) -> VehicleBase:
        vehicle_type_value = payload.get("vehicle_type")
        if vehicle_type_value is None:
            raise ValueError("Missing vehicle_type in payload")
        vehicle_type = VehicleType(vehicle_type_value)
        model = cls._registry.get(vehicle_type)
        if model is None:
            raise ValueError(f"Unsupported vehicle type: {vehicle_type.value}")
        data = {key: value for key, value in payload.items() if key != "vehicle_type"}
        return model(**data)


VehicleFactory.register(VehicleType.CAR, CarSpec)
VehicleFactory.register(VehicleType.USED_CAR, UsedCarSpec)
VehicleFactory.register(VehicleType.TAXI, TaxiSpec)
VehicleFactory.register(VehicleType.BUS, BusSpec)


def load_vehicle_specs(path: Path) -> dict[str, VehicleBase]:
    # This is actually a data layer function

    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)

    vehicles: dict[str, VehicleBase] = {}
    for item in data:
        vehicle = VehicleFactory.create(item)
        if vehicle.name in vehicles:
            raise ValueError(f"Duplicate vehicle name: {vehicle.name}")
        vehicles[vehicle.name] = vehicle
    return vehicles


def load_car_specs(path: Path) -> dict[str, CarSpec]:
    # This is actually a data layer function
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)

    cars: dict[str, CarSpec] = {}
    for item in data:
        car = CarSpec(**item)
        if car.name in cars:
            raise ValueError(f"Duplicate car name: {car.name}")
        cars[car.name] = car
    return cars
