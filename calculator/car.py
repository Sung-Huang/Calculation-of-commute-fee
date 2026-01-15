from config import CarCostAssumptions
from model import CarSpec, CommuteProfile


class CarCommuteCostCalculator:
    def __init__(self, assumptions: CarCostAssumptions | None = None) -> None:
        self._assumptions = assumptions or CarCostAssumptions()

    def calculate_monthly_cost(self, vehicle: CarSpec, commute: CommuteProfile) -> float:
        remaining_life_mileage = max(self._assumptions.expected_life_mileage_km - vehicle.mileage_km, 1.0)
        monthly_distance = commute.monthly_commute_distance_km()
        monthly_fuel_cost = (
            monthly_distance / vehicle.fuel_economy_km_per_liter * self._assumptions.average_fuel_price_per_liter_aed
        )
        depreciation = vehicle.price_aed / remaining_life_mileage * monthly_distance
        monthly_maintenance_fee = vehicle.maintenance_aed_per_km * monthly_distance
        monthly_insurance_fee = self._assumptions.annual_insurance_aed / commute.months_per_year
        monthly_parking_fee = self._assumptions.annual_parking_aed / commute.months_per_year
        toll_fee = (
            self._assumptions.toll_per_crossing_aed * commute.round_trips_per_day * commute.working_days_per_month
        )
        return (
            monthly_fuel_cost
            + depreciation
            + monthly_maintenance_fee
            + monthly_insurance_fee
            + monthly_parking_fee
            + toll_fee
        )


class UsedCarCommuteCostCalculator(CarCommuteCostCalculator):
    def calculate_monthly_cost(self, vehicle: CarSpec, commute: CommuteProfile) -> float:
        return super().calculate_monthly_cost(vehicle, commute)
