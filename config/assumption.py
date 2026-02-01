from dataclasses import dataclass


@dataclass(frozen=True)
class CarCostAssumptions:
    annual_insurance_aed: float = 3000.0
    annual_parking_aed: float = 800.0
    expected_life_mileage_km: float = 275000.0
    average_fuel_price_per_liter_aed: float = 2.3
    toll_per_crossing_aed: float = 4.0


@dataclass(frozen=True)
class OwnedCarCostAssumptions:
    annual_insurance_aed: float = 2000.0
    annual_parking_aed: float = 800.0
    average_fuel_price_per_liter_aed: float = 2.3
    expected_life_mileage_km: float = 300000.0
    toll_per_crossing_aed: float = 4.0
    maintenance_year_1_aed: float = 0.0
    maintenance_year_2_5_aed: float = 0.0
    maintenance_year_6_10_aed: float = 1000.0
