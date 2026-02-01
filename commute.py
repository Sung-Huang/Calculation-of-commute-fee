from pathlib import Path

import matplotlib.pyplot as plt

from calculator import (
    BusCommuteCostCalculator,
    CarCommuteCostCalculator,
    CarOwnershipCostCalculator,
    TaxiCommuteCostCalculator,
)
from model import BusSpec, CommuteProfile, TaxiSpec, load_car_specs


def main() -> None:
    commute = CommuteProfile(one_way_distance_km=40, leisure_daily_distance_km=6)

    taxi = TaxiSpec(name="Taxi")
    bus = BusSpec(name="Bus")
    taxi_calculator = TaxiCommuteCostCalculator()
    bus_calculator = BusCommuteCostCalculator()

    print(f"Taxi single trip: {taxi_calculator.calculate_single_trip_cost(taxi, commute):.2f} AED")
    print(f"Taxi monthly: {taxi_calculator.calculate_monthly_cost(taxi, commute):.2f} AED")
    print(f"Bus single trip: {bus_calculator.calculate_single_trip_cost(bus, commute):.2f} AED")
    print(f"Bus monthly: {bus_calculator.calculate_monthly_cost(bus, commute):.2f} AED")

    car_specs = load_car_specs(Path(__file__).resolve().parent / "data" / "cars.json")
    car = car_specs["TOYOTA YARIS SEDAN 2024 E"]
    car_calculator = CarCommuteCostCalculator()
    print(f"{car.brand} {car.model} monthly: {car_calculator.calculate_monthly_cost(car, commute):.2f} AED")

    ownership_calculator = CarOwnershipCostCalculator()
    monthly_costs, expected_life_months = ownership_calculator.calculate_monthly_cost_series(
        car,
        commute,
        down_payment_rate=30,
        interest_rate=2.9,
        loan_term_years=5,
    )
    plt.bar([x for x in range(1, expected_life_months + 2)], monthly_costs)
    plt.title(f"Real monthly cost of {car.brand} {car.model} {car.energy_type} by month")
    plt.xlabel("Month")
    plt.ylabel("Price in AED")
    plt.show()


if __name__ == "__main__":
    main()
