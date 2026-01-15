from typing import Protocol

from model import CommuteProfile, VehicleBase


class ICommuteCostCalculator(Protocol):
    def calculate_monthly_cost(self, vehicle: VehicleBase, commute: CommuteProfile) -> float: ...
