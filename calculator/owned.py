from config import OwnedCarCostAssumptions
from model import CarSpec, CommuteProfile


class CarOwnershipCostCalculator:
    def __init__(self, assumptions: OwnedCarCostAssumptions | None = None) -> None:
        self._assumptions = assumptions or OwnedCarCostAssumptions()

    def _monthly_distance(self, commute: CommuteProfile) -> float:
        return commute.monthly_commute_distance_km()

    def _expected_life_months(self, vehicle: CarSpec, monthly_distance: float) -> int:
        expected_life_mileage = max(self._assumptions.expected_life_mileage_km - vehicle.mileage_km, 1.0)
        return int(expected_life_mileage / monthly_distance)

    def _fixed_monthly_cost(self, vehicle: CarSpec, commute: CommuteProfile, monthly_distance: float) -> float:
        monthly_fuel_cost = (
            monthly_distance / vehicle.fuel_economy_km_per_liter * self._assumptions.average_fuel_price_per_liter_aed
        )
        toll_fee = (
            self._assumptions.toll_per_crossing_aed * commute.round_trips_per_day * commute.working_days_per_month
        )
        monthly_insurance_fee = self._assumptions.annual_insurance_aed / commute.months_per_year
        monthly_parking_fee = self._assumptions.annual_parking_aed / commute.months_per_year
        return monthly_fuel_cost + monthly_insurance_fee + monthly_parking_fee + toll_fee

    def _monthly_payment(
        self, vehicle: CarSpec, down_payment_rate: float, interest_rate: float, loan_term_years: int
    ) -> tuple[float, int]:
        down_payment = down_payment_rate / 100 * vehicle.price_aed
        loan_months = loan_term_years * 12
        loan_amount = vehicle.price_aed - down_payment
        if loan_months == 0:
            return 0.0, 0
        monthly_rate = interest_rate / 100 / 12
        if monthly_rate == 0:
            return loan_amount / loan_months, loan_months
        monthly_payment = ((loan_amount * monthly_rate) * (1 + monthly_rate) ** loan_months) / (
            (1 + monthly_rate) ** loan_months - 1
        )
        return monthly_payment, loan_months

    def _payment_series(
        self, down_payment: float, monthly_payment: float, loan_months: int, expected_life_months: int
    ) -> list[float]:
        payments = [down_payment]
        if loan_months > 1:
            payments.extend([monthly_payment] * (loan_months - 1))
        if expected_life_months + 1 > len(payments):
            payments.extend([0.0] * (expected_life_months + 1 - len(payments)))
        return payments[: expected_life_months + 1]

    def _maintenance_for_month(self, month_index: int) -> float:
        if month_index < 12:
            return self._assumptions.maintenance_year_1_aed / 12
        if month_index < 60:
            return self._assumptions.maintenance_year_2_5_aed / 12
        return self._assumptions.maintenance_year_6_10_aed / 12

    def calculate_monthly_cost_series(
        self,
        vehicle: CarSpec,
        commute: CommuteProfile,
        down_payment_rate: float,
        interest_rate: float,
        loan_term_years: int,
    ) -> tuple[list[float], int]:
        monthly_distance = self._monthly_distance(commute)
        expected_life_months = self._expected_life_months(vehicle, monthly_distance)
        fixed_monthly_cost = self._fixed_monthly_cost(vehicle, commute, monthly_distance)
        down_payment = down_payment_rate / 100 * vehicle.price_aed
        monthly_payment, loan_months = self._monthly_payment(
            vehicle,
            down_payment_rate=down_payment_rate,
            interest_rate=interest_rate,
            loan_term_years=loan_term_years,
        )
        monthly_payments = self._payment_series(down_payment, monthly_payment, loan_months, expected_life_months)

        total_monthly_costs = [
            payment + self._maintenance_for_month(month_index) + fixed_monthly_cost
            for month_index, payment in enumerate(monthly_payments)
        ]
        return total_monthly_costs, expected_life_months
